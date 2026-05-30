# -*- coding: utf-8 -*-
"""
Ludus Magnus - Dual MCP Server Suite
Temple Run Gameplay Mechanics Engine
Injects auto-running, 90-degree turning, obstacle collision, coin collection, and a HUD into the active PIE session.
"""

import unreal
import time

class TempleRunGameEngine:
    def __init__(self):
        self.score = 0
        self.distance = 0.0
        self.is_game_over = False
        self.start_time = 0.0
        
        # Input tracking
        self.prev_left_down = False
        self.prev_right_down = False
        self.prev_jump_down = False
        
        # Game state caching
        self.coins = []
        self.obstacles = []
        self.last_cache_time = 0.0
        
        self.tick_handle = None
        self.is_registered = False

    def cache_actors(self, world):
        """
        Caches coins and hurdles in the active world to optimize real-time distance checks.
        """
        current_time = time.time()
        if current_time - self.last_cache_time < 2.0:
            return
            
        self.last_cache_time = current_time
        
        # Find all level actors
        actor_subsystem = unreal.EditorActorSubsystem()
        all_actors = actor_subsystem.get_all_level_actors()
        
        self.coins = []
        self.obstacles = []
        
        for actor in all_actors:
            label = actor.get_actor_label()
            if "TempleRun_Coin_" in label:
                self.coins.append(actor)
            elif "TempleRun_Hurdle_" in label or "TempleRun_Wall_" in label or "TempleRun_Arch_" in label:
                self.obstacles.append(actor)
                
    def reset_game(self, pawn):
        """
        Resets player coordinates, score, and state when they crash.
        """
        print("TEMPLE RUN: Resetting game...")
        pawn.set_actor_location(unreal.Vector(-200, 0, 100), False, False)
        pawn.set_actor_rotation(unreal.Rotator(0, 0, 0), False)
        
        self.score = 0
        self.distance = 0.0
        self.is_game_over = False
        self.start_time = time.time()
        
        # Stop character movement physics
        char_move = pawn.character_movement
        if char_move:
            char_move.velocity = unreal.Vector(0, 0, 0)

    def tick(self, delta_time):
        """
        Post-Tick callback executed every frame by the Slate Renderer during PIE.
        """
        # Ensure we can resolve the active game world (only runs during active PIE gameplay)
        world = unreal.EditorLevelLibrary.get_game_world()
        if not world:
            return
            
        pawn = unreal.GameplayStatics.get_player_pawn(world, 0)
        if not pawn:
            return
            
        # Initialize start time if needed
        if self.start_time == 0.0:
            self.start_time = time.time()
            
        # 1. Cache level actors
        self.cache_actors(world)
        
        # 2. Game HUD rendering
        hud_text = f"=== TEMPLE RUN LIVE ===\nCOINS: {self.score} / 15\nDISTANCE: {int(self.distance)}m"
        if self.is_game_over:
            hud_text += "\n\n!!! CRASH! GAME OVER !!!\nResetting in 2 seconds..."
            
        # Draw HUD to screen
        unreal.SystemLibrary.print_string(
            world,
            hud_text,
            True, # Print to Screen
            False, # Print to Log (prevent clutter)
            unreal.LinearColor(1.0, 0.8, 0.0, 1.0), # Amber Gold
            0.05 # Duration matching delta_time
        )
        
        if self.is_game_over:
            return
            
        # 3. Auto-Running logic: move player forward along their forward vector
        forward_vector = pawn.get_actor_forward_vector()
        pawn_location = pawn.get_actor_location()
        
        run_speed = 950.0 # Speed in cm/s
        new_location = pawn_location + forward_vector * (run_speed * delta_time)
        
        # Sweep=True forces collision bounds detection against boundaries and hurdles
        pawn.set_actor_location(new_location, True)
        
        # Increment distance score
        self.distance += (run_speed * delta_time) / 100.0 # meters
        
        # 4. Handle Winding Controls: Keyboard Input Detection (edge-triggered)
        pc = unreal.GameplayStatics.get_player_controller(world, 0)
        if pc:
            # Query Left / Turn Left key
            left_down = pc.is_input_key_down(unreal.Key("A")) or pc.is_input_key_down(unreal.Key("Left"))
            if left_down and not self.prev_left_down:
                # Turn 90 degrees Left
                rot = pawn.get_actor_rotation()
                rot.yaw -= 90.0
                pawn.set_actor_rotation(rot, False)
                print("TEMPLE RUN: Turned Left!")
            self.prev_left_down = left_down
            
            # Query Right / Turn Right key
            right_down = pc.is_input_key_down(unreal.Key("D")) or pc.is_input_key_down(unreal.Key("Right"))
            if right_down and not self.prev_right_down:
                # Turn 90 degrees Right
                rot = pawn.get_actor_rotation()
                rot.yaw += 90.0
                pawn.set_actor_rotation(rot, False)
                print("TEMPLE RUN: Turned Right!")
            self.prev_right_down = right_down
            
            # Query Jump key
            jump_down = pc.is_input_key_down(unreal.Key("Space")) or pc.is_input_key_down(unreal.Key("Up"))
            if jump_down and not self.prev_jump_down:
                # Call Character built-in Jump function
                pawn.jump()
                print("TEMPLE RUN: Jumped!")
            self.prev_jump_down = jump_down

        # 5. Coin Overlap Detection
        pawn_loc = pawn.get_actor_location()
        for coin in list(self.coins):
            if not coin or not coin.is_valid():
                continue
            coin_loc = coin.get_actor_location()
            if pawn_loc.distance(coin_loc) < 140.0:
                # Coin collected!
                coin.destroy_actor()
                self.score += 1
                self.coins.remove(coin)
                # Visual flash
                unreal.SystemLibrary.print_string(world, "+1 Gold Coin!", True, False, unreal.LinearColor(0, 1, 0, 1), 0.8)
                
        # 6. Obstacle / Fall Collision Detection
        # Fall check (if player falls off the suspended runway)
        if pawn_loc.z < -200.0:
            self.trigger_crash(pawn)
            return
            
        # Hurdles collision check
        for obs in self.obstacles:
            if not obs or not obs.is_valid():
                continue
            obs_loc = obs.get_actor_location()
            # If player is extremely close to hurdle or wall centers
            if pawn_loc.distance(obs_loc) < 150.0:
                # Check height offset for jumpable hurdle logs
                if "Hurdle_Log" in obs.get_actor_label() and pawn_loc.z > 160.0:
                    # Player successfully jumped over the log!
                    continue
                self.trigger_crash(pawn)
                return

    def trigger_crash(self, pawn):
        """
        Triggers a game-over crash, waits 2 seconds, and restarts.
        """
        self.is_game_over = True
        print("TEMPLE RUN: CRASH DETECTED!")
        
        # Run asynchronous delayed reset so player can see Game Over screen
        asyncio.create_task(self.delayed_reset(pawn))
        
    async def delayed_reset(self, pawn):
        await asyncio.sleep(2.0)
        self.reset_game(pawn)


# Create global singleton session
if 'tr_engine' not in globals():
    tr_engine = TempleRunGameEngine()

def register_engine():
    # Unregister old post tick callbacks to prevent stacking loops
    if 'tr_tick_handle' in globals():
        try:
            unreal.unregister_slate_post_tick_callback(globals()['tr_tick_handle'])
            print("Cleaned up existing Slate tick callback.")
        except Exception:
            pass

    # Register new tick callback
    handle = unreal.register_slate_post_tick_callback(tr_engine.tick)
    globals()['tr_tick_handle'] = handle
    print("[SUCCESS] Temple Run Gameplay Engine registered to Slate Post-Tick callback!")

register_engine()
