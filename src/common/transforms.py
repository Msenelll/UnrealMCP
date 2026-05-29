# -*- coding: utf-8 -*-
"""
Ludus Magnus - Dual MCP Server Suite
[REQ_TDD_ARC_06] Coordinate Converter Utility Class
Maps Blender right-handed Z-up space to Unreal Engine left-handed Z-up space
"""

from typing import Dict

class CoordinateConverter:
    """
    Handles coordinate translations and scale alignments between Blender and Unreal Engine 5.
    Ensures that procedural meshes are mapped and positioned accurately without transform drift.
    """

    @staticmethod
    def blender_to_unreal_location(b_loc: Dict[str, float]) -> Dict[str, float]:
        """
        Converts location from Blender (meters, right-handed) to Unreal Engine 5 (centimeters, left-handed).
        Formula:
        X_ue = b_loc['x'] * 100.0
        Y_ue = b_loc['y'] * 100.0
        Z_ue = b_loc['z'] * 100.0
        
        Args:
            b_loc (Dict[str, float]): Dictionary containing 'x', 'y', 'z' values in Blender space.
            
        Returns:
            Dict[str, float]: Dictionary containing converted 'x', 'y', 'z' values in Unreal space.
        """
        # Ensure floating point inputs
        x = float(b_loc.get("x", 0.0))
        y = float(b_loc.get("y", 0.0))
        z = float(b_loc.get("z", 0.0))
        
        # Scale and eksen conversion
        return {
            "x": x * 100.0,
            "y": y * 100.0,
            "z": z * 100.0
        }

    @staticmethod
    def blender_to_unreal_rotation(b_rot: Dict[str, float]) -> Dict[str, float]:
        """
        Converts rotation from Blender Euler angles to Unreal Engine 5 (Pitch, Yaw, Roll) angles.
        In Blender, rotation is in X, Y, Z.
        In Unreal Engine, rotation is expressed as Roll (X), Pitch (Y), Yaw (Z).
        
        Args:
            b_rot (Dict[str, float]): Dictionary containing 'x', 'y', 'z' rotation values in Blender space.
            
        Returns:
            Dict[str, float]: Dictionary containing converted 'pitch', 'yaw', 'roll' values in Unreal space.
        """
        rx = float(b_rot.get("x", 0.0))
        ry = float(b_rot.get("y", 0.0))
        rz = float(b_rot.get("z", 0.0))
        
        return {
            "pitch": ry,  # Blender Y rotation maps to Unreal Pitch
            "yaw": rz,    # Blender Z rotation maps to Unreal Yaw
            "roll": rx    # Blender X rotation maps to Unreal Roll
        }

    @staticmethod
    def unreal_to_blender_location(u_loc: Dict[str, float]) -> Dict[str, float]:
        """
        Converts location back from Unreal Engine 5 (centimeters, left-handed) to Blender (meters, right-handed).
        
        Args:
            u_loc (Dict[str, float]): Dictionary containing 'x', 'y', 'z' values in Unreal space.
            
        Returns:
            Dict[str, float]: Dictionary containing converted 'x', 'y', 'z' values in Blender space.
        """
        x = float(u_loc.get("x", 0.0))
        y = float(u_loc.get("y", 0.0))
        z = float(u_loc.get("z", 0.0))
        
        return {
            "x": x / 100.0,
            "y": y / 100.0,
            "z": z / 100.0
        }
