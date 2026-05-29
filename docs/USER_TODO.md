# KULLANICI YAPILACAKLAR LİSTESİ (USER TODO - RUN GUIDE)

**Proje Kodu:** LUDUS_MCP_2026  
**Sürüm:** v1.0:0  
**Sistem Durumu:** KULLANIMA HAZIR  

Bu dokümanda, "Ludus Magnus" Dual MCP Server Suite'i bölünmüş ekran otonom çalışma alanınızda (Cursor, Claude Desktop veya Antigravity Arayüzü) hemen kullanmaya başlamak için yapmanız gereken birkaç manuel editör/konfigürasyon adımı açıklanmıştır.

---

### ADIM 1: Unreal Engine Editör Ayarları ve Hazırlık

Sunucumuzun Unreal Engine ile asenkron konuşabilmesi için editörünüzde şu ayarların yapılması gerekir:

1. **Remote Control Web Server Aktivasyonu:**
   * Unreal Editor'ü açın.
   * `Edit > Plugins` menüsünden **Remote Control API** eklentisinin aktif (Enabled) olduğunu doğrulayın. (Değilse aktif edip editörü yeniden başlatın).
   * Eklenti aktif olduğunda, editör arka planda otomatik olarak `http://localhost:30010` portundan bir web sunucusu ayağa kaldıracaktır.

2. **Master Materyal Oluşturma (`MM_Otonom_Master`):**
   * Editör içerisindeki `Content` tarayıcısında `/Game/ProceduralAssets/Materials/` klasör yolunu oluşturun.
   * Bu klasörün içine **`MM_Otonom_Master`** adında yeni bir Materyal (Material) ekleyin.
   * Materyal graph'ını açarak şu parametreleri tanımlayın ve PBR Master Node'una bağlayın:
     * **`Base Color`** (Vector Parameter) -> Varsayılan Değer: Gri `(0.7, 0.7, 0.7, 1.0)`
     * **`Metallic`** (Scalar Parameter) -> Varsayılan Değer: `0.0`
     * **`Roughness`** (Scalar Parameter) -> Varsayılan Değer: `0.5`
   * Kaydedip kapatın. Otonom olarak üretilen tüm materyaller bu Master Materyal parametrelerini kullanarak otomatik türetilecektir.

---

### ADIM 2: Blender PATH Yapılandırması

* Prosedürel 3D mesh üretiminin headless (sessiz arka plan) çalışabilmesi için bilgisayarınızda **Blender 4.0+** kurulu olmalıdır.
* Blender'ın yerleşik kurulum yolu `C:\Program Files\Blender Foundation\Blender 4.X\blender.exe` şeklinde ise sistemimiz bunu otomatik olarak algılayacaktır. Farklı bir kurulum yolu kullanıyorsanız, Blender çalıştırılabilir dosyasının Windows ortam değişkenlerindeki `PATH` listesine eklendiğinden emin olun.

---

### ADIM 3: Ajan/Cursor/Claude Desktop Entegrasyonu

Geliştirici arayüzünüzün (Cursor veya Claude Desktop) bu araçları kullanabilmesi için, kullandığınız platformun `mcp_config.json` dosyasına (Cursor için `Settings > Features > MCP` altından) aşağıdaki konfigürasyon bloklarını eklemeniz yeterlidir:

```json
{
  "mcpServers": {
    "unreal-mcp-server": {
      "command": "C:/repo/2_UnrealMCP/.venv/Scripts/python.exe",
      "args": ["-m", "src.unreal_server.server"],
      "env": {
        "PYTHONPATH": "C:/repo/2_UnrealMCP"
      }
    },
    "blender-mcp-server": {
      "command": "C:/repo/2_UnrealMCP/.venv/Scripts/python.exe",
      "args": ["-m", "src.blender_server.server"],
      "env": {
        "PYTHONPATH": "C:/repo/2_UnrealMCP"
      }
    }
  }
}
```

Bu eklemeyi yaptıktan sonra ajanınız (Antigravity 2) bölünmüş ekranın solunda sizinle konuşurken, sağ taraftaki Unreal Engine ve Blender sahnenizi otonom olarak kontrol etmeye, C++ kodlarınızı derlemeye ve 3D varlık ithal etmeye anında başlayabilecektir!
