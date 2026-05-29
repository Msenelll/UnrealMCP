# L1-C: BORUHATTI VE ENTEGRASYON DÖKÜMANI (PIPELINE & INTEGRATION DOCUMENT - PID)

**Proje Kodu:** LUDUS_MCP_2026  
**Doküman Kodu:** PID_MASTER_01  
**Versiyon:** v0.1:0  
**Doküman Sahibi:** @bridge-virtuoso (Tech Art & Audio Director)  
**Sistem Durumu:** İNCELEMEDE / GATED STEP 4  

---

## 1. Varlık Otomasyon Standartları (Asset Automation Standards)

Blender MCP Server ve Unreal Engine 5 arasındaki entegrasyon hattında üretilecek tüm procedural 3D assetler, insan müdahalesi olmadan tamamen otomatik adlandırılmalı, kategorize edilmeli ve ilgili dizinlere yerleştirilmelidir.

### 1.1. İsimlendirme Kuralları (Automated Naming Conventions)
Otonom üretilen ve ithal (import) edilen assetler şu kalıba göre isimlendirilecektir:

* **Static Mesh (Statik Model):** `SM_Proc_[AssetType]_[Timestamp]_[ShortHash]`  
  * *Örnek:* `SM_Proc_Cylinder_20260529_a7c8`
* **Material (Ana Materyal):** `M_Proc_[MaterialType]_[ShortHash]`  
  * *Örnek:* `M_Proc_Chrome_b4d1`
* **Material Instance (Parametrik Örnek):** `MI_Proc_[AssetType]_[Timestamp]_[ShortHash]`  
  * *Örnek:* `MI_Proc_Cylinder_20260529_a7c8`
* **Textures (Dokular):**
  * Base Color / Albedo: `T_Proc_[AssetType]_D`
  * Normal Map: `T_Proc_[AssetType]_N`
  * Ambient Occlusion / Roughness / Metallic (ORM): `T_Proc_[AssetType]_ORM`

### 1.2. Unreal Engine Hedef Klasör Yapısı
Tüm otonom varlıklar, projenin `Content` klasöründe tek bir çatı altında toplanacaktır:
```
/Game/
└── ProceduralAssets/
    ├── Meshes/         # İthal edilen SM_Proc_... fbx dosyaları
    ├── Materials/      # M_Proc_... ve MI_Proc_... materyal yapıları
    └── Textures/       # Üretilen doku dosyaları (.png/.tga)
```

---

## 2. Veri Serileştirme ve FBX Export Matrisleri (FBX Translation Matrix)

Blender (Right-Handed, Z-Up) ile Unreal Engine 5 (Left-Handed, Z-Up) arasındaki koordinat dönüşüm hatası riskini sıfıra indirmek için Blender `bpy` modülü üzerinden yapılan FBX export parametreleri ve pivot hizalama matrisleri bu bölümde kilitlenmiştir.

### 2.1. Eksen ve Ölçek Dönüşüm Matrisi (Blender bpy Seviyesi)
Blender sahnesindeki model dışa aktarılırken, ölçek faktörü (Blender: 1 birim = 1 metre, UE5: 1 birim = 1 santimetre) 100.0 ile çarpılmalı ve eksenler otomatik dönüştürülmelidir.

```python
# Blender bpy export parametre matrisi
FBX_EXPORT_ARGS = {
    "filepath": "C:/Temp/SM_Proc_Mesh.fbx",
    "use_selection": True,
    "global_scale": 1.0,               # Ölçekleme transform matrisiyle çözülecektir
    "apply_unit_scale": True,          # Blender ünite ölçeğini uygula
    "axis_forward": '-Z',              # Blender Forward (-Z) -> Unreal Forward
    "axis_up": 'Y',                    # Blender Up (Y) -> Unreal Up (Z-up için dönüşüm matrisi)
    "bake_space_transform": True,      # Transformasyonları mesh verisine kalıcı olarak yaz (bake)
    "mesh_smooth_groups": True,        # Smoothing gruplarını koru
    "use_mesh_modifiers": True,        # Blender modifier'larını (Bevel, Subsurf vb.) uygula
}
```

### 2.2. Pivot Hizalama Standartı (Pivot Alignment Logic)
Procedural mesh üretildiğinde, modelin dünyadaki pivot noktası (Origin) her zaman **taban-merkez (bottom-center)** konumuna hizalanacaktır. Bu sayede Unreal içerisine spawn edildiğinde aktörün zemine tam oturması sağlanacaktır.

```python
import bpy

def align_pivot_to_bottom_center(obj):
    """
    Seçili objenin pivot noktasını en alt merkezine taşır.
    """
    bpy.context.view_layer.objects.active = obj
    # Objenin bounding box verilerini al
    bbox = [obj.matrix_world @ pygame.Vector3(corner) for corner in obj.bound_box]
    # En alt Z seviyesini ve X-Y merkezini hesapla
    min_z = min(corner.z for corner in bbox)
    center_x = sum(corner.x for corner in bbox) / 8.0
    center_y = sum(corner.y for corner in bbox) / 8.0
    
    # Cursor'ı taban merkezine taşı ve pivotu oraya set et
    bpy.context.scene.cursor.location = (center_x, center_y, min_z)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
```

---

## 3. Otomatik UE5 Varlık İthalat Parametreleri (Automated FBX Import)

Blender'dan çıkan FBX, Unreal Engine Remote Control API aracılığıyla `AssetTools` kütüphanesi kullanılarak sessizce (headless/no-prompt) içeri alınacaktır. İthalat sırasında uygulanacak yapılandırma nesnesi şeması aşağıdadır:

```json
{
  "ImportTask": {
    "Filename": "C:/Temp/SM_Proc_Mesh.fbx",
    "DestinationPath": "/Game/ProceduralAssets/Meshes",
    "bAutomated": true,
    "bReplaceExisting": true,
    "bSave": true,
    "Options": {
      "bImportMesh": true,
      "bImportAsSkeletal": false,
      "bConvertScene": true,
      "bConvertSceneUnit": true,
      "bImportMaterials": true,
      "bImportTextures": true,
      "NormalImportMethod": "FBXNIM_ImportNormalsAndTangents",
      "MaterialImportMethod": "FBXNIM_CreateNewMaterials"
    }
  }
}
```

---

## 4. Görsel Kalite ve Performans Bütçeleri Matrisi (Tech-Art Performance Matrix)

Prosedürel olarak üretilecek 3D varlıkların ve materyallerin, local donanım kaynaklarını aşmaması ve editor performansını düşürmemesi için aşağıdaki bütçe sınırlarına uyması zorunludur:

| Gereksinim ID | Asset Tipi | Maksimum Değer | Açıklama ve Kural |
| :--- | :--- | :--- | :--- |
| **[REQ_PID_AST_01]** | Prosedürel Mesh | Maksimum **15.000 Tris** | Poligon sayısı bu sınırı aşan modeller otomatik olarak Blender seviyesinde *Decimate Modifier* ile seyreltilecektir. |
| **[REQ_PID_AST_02]** | Doku Boyutu | Maksimum **2048 x 2048px** | Gürültü ve bellek tasarrufu amacıyla varsayılan otonom doku boyutu **1024 x 1024px** olarak ayarlanacaktır. |
| **[REQ_PID_AST_03]** | Master Materyal | Maksimum **2 adet Materyal** | Prosedürel üretilen tüm assetler, `MM_Otonom_Master` master materyalinden türetilen *Material Instance* nesnelerini kullanacaktır. |
| **[REQ_PID_AST_04]** | UV Layout | Minimum **1 adet UV Kanalı** | Tüm modellerde çakışmayan (non-overlapping) UV adaları otomatik olarak Blender `smart_project` algoritmasıyla açılacaktır. |

---

## 5. İzlenebilirlik Matrisi (PID Traceability Matrix)

| Pipeline ID | Açıklama | İlişkili SRD ID | İlişkili TDD ID | Bağlı Olduğu L0 Kısıtı |
| :--- | :--- | :--- | :--- | :--- |
| **[REQ_PID_AST_01]** | Otomatik isimlendirme ve Content klasörü yerleşim kurallarının işletilmesi. | `[REQ_SRD_INT_01]` | `[REQ_TDD_ARC_01]` | `[REQ_VD_VAL_01]` |
| **[REQ_PID_AST_02]** | Blender FBX eksen, ölçek dönüşüm ve pivot hizalama kodlarının uygulanması. | `[REQ_SRD_BLN_03]` | `[REQ_TDD_ARC_06]` | `[REQ_VD_ART_01]` |
| **[REQ_PID_AST_03]** | Headless Blender export komut setinin asenkron Python entegrasyonu. | `[REQ_SRD_BLN_03]` | `[REQ_TDD_ARC_05]` | `[REQ_VD_TEC_02]` |
| **[REQ_PID_AST_04]** | Unreal Remote Control API asset import JSON şemasının ve görev tetikleyicisinin yazılması. | `[REQ_SRD_INT_01]` | `[REQ_TDD_ARC_02]` | `[REQ_VD_TEC_01]` |
| **[REQ_PID_AST_05]** | Master Materyal instancing parametrelerinin serileştirilmesi (Serialization). | `[REQ_SRD_BLN_02]` | `[REQ_TDD_ARC_02]` | `[REQ_VD_ART_02]` |

---

### Tech Art Director Onayı
* **Durum:** L1-C Pipeline & Integration Document (PID) oluşturuldu. Bir sonraki aşama olan L2 Product Backlog Item (PBI) aşamasına geçmek için kullanıcı onayı bekleniyor.
* **Karar/Onay İmzası:** *Beklemede...*
