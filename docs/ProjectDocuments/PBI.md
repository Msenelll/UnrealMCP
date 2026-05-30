# L2: PRODUCT BACKLOG ITEMS (PBI) & BITTI TANIMI (DoD)

**Proje Kodu:** LUDUS_MCP_2026  
**Doküman Kodu:** PBI_MASTER_01  
**Versiyon:** v0.2:0  
**Doküman Sahibi:** @qa-nexus (System Integrator & QA Lead)  
**Sistem Durumu:** İNCELEMEDE / GATED STEP 5  

---

## 1. Evrensel Bitti Tanımı (Universal Definition of Done - DoD)

"Ludus Magnus" geliştirme hattında üretilen her kod parçası, asset veya entegrasyon görevi, "DONE" (Tamamlandı) durumuna çekilmeden önce aşağıdaki kalite kapılarını tavizsiz şekilde geçmek zorundadır. QA ekibi, bu kriterleri karşılamayan hiçbir işi kabul etmeyecektir:

1. **PEP 8 ve Tip Belirteçleri (Type Hints):** Tüm Python kodları PEP 8 standartlarına %100 uyumlu olmalı ve tüm fonksiyon/sınıf tanımlarında tip belirteçleri eksiksiz kullanılmalıdır.
2. **Sıfır-Bloklama (Non-blocking Asynchronous I/O):** I/O veya CPU yoğun hiçbir operasyon (HTTP istekleri, derleme alt süreçleri vb.) `asyncio` döngüsünü kilitlememelidir.
3. **No-Tick Uyum Sınırı:** Arka planda çalışan hiçbir sürekli döngüsel veri sorgulama (polling/tick) fonksiyonu bulunmamalıdır. Sistem sadece event-driven tetiklenmelidir.
4. **Koordinat Sistemi Uyumu:** Blender'dan UE5'e aktarılan tüm nesneler `CoordinateConverter` eksen çevirisine tabi tutulmuş olmalı ve pivot noktaları **taban-merkez (bottom-center)** konumunda kilitlenmelidir.
5. **Traceability (İzlenebilirlik) Kilidi:** Merge edilecek her feature branch, bir `PBI_[ID]` taşımalı ve o PBI doğrudan `SRD.md` ile `TDD.md` gereksinimlerine bağlı olmalıdır. İlişkisiz ("kaçak") tasarımlar elenecektir.
6. **Sürüm Kontrolü ve Branch Kapısı:** Feature branch, `develop` dalına otomatik testler sonrasında merge edilebilir. `master` branch'ine doğrudan merge yasaktır. Commit mesajları `vA.B:C` formatında sürüm takibi taşımalıdır.
7. **Test Kapsamı:** Yazılan her Python modülü için en az %85 oranında birim test (unit test) kapsamı (`pytest` veya yerleşik mock testleri) oluşturulmuş olmalıdır.

---

## 2. Product Backlog Items (PBI Listesi)

---

### PBI_001: Asenkron Python MCP Sunucu Altyapısının Kurulması

**İzlenebilirlik Linkleri:**
* SRD Link: `[REQ_SRD_INT_02]` (JSON-RPC 2.0 MCP Transport)
* TDD Link: `[REQ_TDD_ARC_01]` (Python `mcp` stdio transport altyapısı)
* L0 Link: `[REQ_VD_TEC_02]` (Asenkron ve kilitsiz mimari)

**Sprint:** Sprint 01  
**Owner (Geliştirici):** @core-arch  
**Status:** Backlog  

#### 1. User Story
* **As a:** Otonom arayüzlerle entegrasyon yapan bir Geliştirici olarak,
* **I want to:** Asenkron çalışan bir Python MCP stdio sunucusu kurmak ve ayağa kaldırmak istiyorum,
* **So that:** Antigravity 2 ajan arayüzü ile sunucu arasında JSON-RPC 2.0 protokolüyle kilitlenmeyen bir stdio haberleşme hattı kurabilmek için.

#### 2. Technical Implementation Notes
* Python `mcp` SDK'sı kullanılarak sunucu başlatılacak.
* Sunucu stdio (`sys.stdin` / `sys.stdout`) kanallarını dinleyecek.
* Sunucunun ana döngüsü asenkron (`asyncio`) mimaride tasarlanacak.
* Hata durumlarında standart JSON-RPC 2.0 hata kodları (`-32603` vb.) dönecek özel bir hata yakalama middleware'i yazılacak.

#### 3. Acceptance Criteria (AC)
* [ ] **AC_01:** Sunucu başlatıldığında stdio üzerinden MCP protokol el sıkışmasını (handshake) başarıyla tamamlamalıdır.
* [ ] **AC_02:** Ajan araç listeleme sorgusu gönderdiğinde (`tools/list`), tanımlanmış `unreal_` ve `blender_` araç şablonları hatasız listelenmelidir.
* [ ] **AC_03:** Hatalı veya bulunamayan bir araç çağrıldığında, standartlara uygun JSON-RPC hata formatı ve açıklayıcı hata mesajı dönmelidir.

---

### PBI_002: Unreal Engine Remote Control API Entegrasyonu (Telemetry & Spawning)

**İzlenebilirlik Linkleri:**
* SRD Link: `[REQ_SRD_UE5_01]`, `[REQ_SRD_UE5_02]`, `[REQ_SRD_UE5_03]`
* TDD Link: `[REQ_TDD_ARC_02]` (aiohttp Remote Control Client)
* L0 Link: `[REQ_VD_TEC_01]` (Local Latency < 50ms), `[REQ_VD_SCP_01]` (MVP aktörleri)

**Sprint:** Sprint 01  
**Owner (Geliştirici):** @core-arch  
**Status:** Backlog  

#### 1. User Story
* **As a:** Bölünmüş ekranda çalışan bir Otonom Geliştirici Ajan olarak,
* **I want to:** Unreal Engine editör kamerasının telemetry verilerini okumak, aktör spawn etmek ve transformasyonlarını değiştirmek istiyorum,
* **So that:** Unreal sahnesini gerçek zamanlı ve milisaniyeler içerisinde otonom olarak manipüle edebilmek için.

#### 2. Technical Implementation Notes
* `aiohttp.ClientSession` asenkron bağlantısı üzerinden Unreal Remote Control API'ye (`http://localhost:30010/api/v1/object/property`) POST istekleri atılacak.
* `unreal_get_viewport_telemetry` aracıyla aktif editör kamerası transformu ve seçili aktör listesi çekilecek.
* `unreal_spawn_actor` aracıyla `StaticMeshActor`, `PointLight`, `DirectionalLight` tipleri spawn edilecek.
* `unreal_set_actor_transform` aracıyla aktörlerin transformasyon matrisleri güncellenecek.

#### 3. Acceptance Criteria (AC)
* [ ] **AC_01:** `unreal_get_viewport_telemetry` çağrısı, Unreal Editor'den kamera lokasyonunu (X, Y, Z) ve rotasyonunu hatasız getirmelidir.
* [ ] **AC_02:** `unreal_spawn_actor` çağrıldığında, belirtilen koordinatlarda aktör spawn olmalı ve Unreal Editor viewport'unda anında görselleşmelidir.
* [ ] **AC_03:** Aktörlerin lokasyon, rotasyon veya ölçek güncellemeleri local ağ üzerinden tetiklendiğinde istek-yanıt süresi **50ms altında** kalmalıdır.

---

### PBI_003: Çift Katmanlı Asenkron Derleme ve Paketleme Motoru

**İzlenebilirlik Linkleri:**
* SRD Link: `[REQ_SRD_UE5_04]` (Live Coding), `[REQ_SRD_UE5_05]` (RunUAT Paketleme)
* TDD Link: `[REQ_TDD_ARC_03]` (LC Subprocess), `[REQ_TDD_ARC_04]` (RunUAT Subprocess)
* L0 Link: `[REQ_VD_TEC_03]` (LC Safety), `[REQ_VD_TEC_04]` (RunUAT Isolation)

**Sprint:** Sprint 02  
**Owner (Geliştirici):** @core-arch  
**Status:** Backlog  

#### 1. User Story
* **As a:** C++ Geliştiricisi olarak,
* **I want to:** Açık Unreal editöründe Live Coding derlemelerini tetiklemek ve arka planda paketleme testlerini (RunUAT) asenkron alt süreçler olarak çalıştırmak istiyorum,
* **So that:** Derleme ve paketleme işlemleri sırasında Python sunucusunun ve editörün kilitlenmesini engellemek için.

#### 2. Technical Implementation Notes
* `asyncio.create_subprocess_exec` kullanılarak Windows arka plan alt süreçleri yönetilecek.
* Live Coding tetiklenmeden önce Remote Control API sorgusuyla editörün PIE modunda olup olmadığı teyit edilecek.
* RunUAT tetiklendiğinde `RunUAT.bat BuildCookRun` komut dizisi parametrik asenkron çalıştırılacak ve log çıktıları (`stdout`) anlık okunup stream edilecek.

#### 3. Acceptance Criteria (AC)
* [ ] **AC_01:** Editör PIE modunda aktif çalışırken `unreal_live_coding_trigger` tetiklenirse, istek derhal güvenli bir hata mesajıyla reddedilmelidir.
* [ ] **AC_02:** Live Coding veya paketleme işlemi asenkron arka planda çalışırken, Python MCP sunucusu stdio üzerinden ajanla konuşmaya devam etmeli, bağlantı tıkkanmamalıdır.
* [ ] **AC_03:** Paketleme (RunUAT) bittiğinde süreç düzgün kapatılmalı, bellek sızıntıları önlenmeli ve exit koduna göre başarı/hata durumu tespit edilmelidir.

---

### PBI_004: Blender Prosedürel Mesh ve Materyal Üretim Hattı

**İzlenebilirlik Linkleri:**
* SRD Link: `[REQ_SRD_BLN_01]` (Mesh Generation), `[REQ_SRD_BLN_02]` (PBR Materials)
* TDD Link: `[REQ_TDD_ARC_05]` (Blender CLI parameter validation)
* L0 Link: `[REQ_VD_ART_02]` (PBR Materyal Standartları)

**Sprint:** Sprint 02  
**Owner (Tech Artist):** @bridge-virtuoso  
**Status:** Backlog  

#### 1. User Story
* **As a:** 3D Teknik Sanatçısı olarak,
* **I want to:** Blender `bpy` modülünü headless (arka planda sessiz) tetikleyerek otonom mesh ve parametrik materyaller sentezlemek istiyorum,
* **So that:** Manuel 3D modelleme iş yükü olmadan ajanın kararlarıyla dinamik geometriler üretebilmek için.

#### 2. Technical Implementation Notes
* Blender MCP sunucusu, gelen `blender_generate_procedural_mesh` çağrısını parametrelerine (boyut, segment, yükseklik) göre asenkron arka planda `blender.exe --background --python <temp_script.py>` şeklinde çalıştıracaktır.
* `bpy.ops.mesh.primitive_cube_add` vb. standart mesh oluşturma API'leri parametrelerle tetiklenecektir.
* Nesneye parametrik PBR materyal (BaseColor, Metallic, Roughness) ataması yapan Python script şablonu kurgulanacaktır.

#### 3. Acceptance Criteria (AC)
* [ ] **AC_01:** Blender headless worker süreci, hatalı parametre girdilerinde çökmek yerine detaylı JSON hata logu üreterek asenkron olarak sonlanmalıdır.
* [ ] **AC_02:** Üretilen mesh nesnesinde parametrik PBR materyal yapısı ve ataması eksiksiz yapılmalıdır.
* [ ] **AC_03:** Blender süreci en fazla 30 saniye (Timeout) çalışabilmeli, bu süreyi aşarsa süreç sonlandırılmalıdır.

---

### PBI_005: FBX Entegrasyon Köprüsü ve Eksen Dönüşümleri

**İzlenebilirlik Linkleri:**
* SRD Link: `[REQ_SRD_BLN_03]` (FBX Export), `[REQ_SRD_INT_01]` (UE5 Import Bridge)
* TDD Link: `[REQ_TDD_ARC_06]` (Coordinate Converter)
* L0 Link: `[REQ_VD_ART_01]` (FBX Transform Matris Kuralları)

**Sprint:** Sprint 02  
**Owner (Tech Artist):** @bridge-virtuoso  
**Status:** Backlog  

#### 1. User Story
* **As a:** Teknik Entegratör olarak,
* **I want to:** Blender'da prosedürel üretilen 3D varlıkları eksen ve ölçek dönüşümlerini tamamlayıp taban-merkez pivot hizalamasıyla Unreal Engine'e otomatik ithal etmek istiyorum,
* **So that:** Varlıkların Unreal içerisinde ters dönmesini, pivot kaymasını ve boyut hatalarını tamamen otonom olarak engelleyebilmek için.

#### 2. Technical Implementation Notes
* Blender bpy export scripti çalıştırılmadan önce `CoordinateConverter` asenkron sınıfları üzerinden eksen dönüşümleri (Right-to-Left Handed) ve ölçek çevrimi (x100) matrisleri mesh verisine baked (bake) edilecektir.
* Bounding Box koordinatları okunarak pivot noktası taban merkezine (`bottom-center`) hizalanacaktır.
* Üretilen FBX dosyası geçici bir pathten UE5 Remote Control API import komutuyla `/Game/ProceduralAssets/Meshes/` klasörüne sessizce import edilecektir.

#### 3. Acceptance Criteria (AC)
* [ ] **AC_01:** İthal edilen otonom Static Mesh objesinin pivot noktası modelin tam alt taban merkezinde konumlanmış olmalıdır.
* [ ] **AC_02:** Unreal sahnesinde spawn edilen mesh objesi ters dönmüş (flipped) veya eksen kayması yaşamış olmamalıdır. Eksenler UE5 standardında (Z-up, -X Forward) durmalıdır.
* [ ] **AC_03:** FBX ithalat görevi hata almadan tamamlanmalı ve üretilen yeni varlığın Unreal referans adresi (Asset Path) ajana başarılı dönüş sağlamalıdır.

---

### PBI_006: Asenkron Soket-Tabanlı Python Remote Execution Entegrasyonu (Dinamik Kod)

**Gereksinim Linkleri:**
* SRD Link: `[REQ_SRD_UE5_06]` (Dinamik Python Script Çalıştırma Köprüsü)
* TDD Link: `[REQ_TDD_ARC_08]` (Python Remote Execution TCP soket yönetimi)

**Sprint:** Sprint 03 (v2.0)  
**Owner (Geliştirici):** @core-arch  
**Status:** Backlog  

---

#### 1. User Story
* **As a:** Otonom Geliştirici Ajan olarak,
* **I want to:** Unreal Engine editöründe TCP soketi üzerinden dinamik Python kodları koşturmak istiyorum,
* **So that:** REST API ile sınırlı kalmadan, Unreal Python API'sinin sunduğu tüm editör araçlarını dinamik olarak tetikleyebilmek için.

#### 2. Technical Implementation Notes
* Unreal Engine'in `remote_execution.py` modülü `src/unreal_server/` altına dahil edilerek bir wrapper yazılacaktır.
* `unreal_execute_python` adında bir MCP aracı sunularak, ajandan gelen dinamik Python betikleri soket üzerinden editöre gönderilecektir.
* Soket bağlantısı asenkron ve kilitlenmeyen (`asyncio`) yapıda kurulacak, 5 saniyelik timeout sınırı uygulanacaktır.

#### 3. Acceptance Criteria (AC)
* [ ] **AC_01:** `unreal_execute_python` aracıyla basit bir print ifadesi (örn: `print('Hello')`) gönderildiğinde, soket üzerinden Unreal editöründe başarıyla yürütülmeli ve stdout çıktısı ajana dönmelidir.
* [ ] **AC_02:** Hatalı bir Python kodu gönderildiğinde sunucu çökmemeli, soket üzerinden dönen hata (traceback) ajana detaylı hata logu olarak iletilmelidir.
* [ ] **AC_03:** Ağır veya uzun süren betiklerde soket bağlantısı MCP sunucusunun ana stdio döngüsünü kesinlikle bloke etmemelidir.

---

### PBI_007: Genişletilmiş Sahne Hiyerarşisi ve Aktör Sorgu Sistemi

**Gereksinim Linkleri:**
* SRD Link: `[REQ_SRD_UE5_07]` (Genişletilmiş Sahne Hiyerarşisi Sorgusu)
* TDD Link: `[REQ_TDD_ARC_09]` (Hiyerarşik REST RC API sorguları)

**Sprint:** Sprint 03 (v2.0)  
**Owner (Geliştirici):** @core-arch  
**Status:** Backlog  

---

#### 1. User Story
* **As a:** Bölünmüş ekranda çalışan bir Yapay Zeka Tasarımcısı olarak,
* **I want to:** Sahnedeki tüm aktörleri ve bu aktörlerin üzerindeki bileşenleri hiyerarşik olarak sorgulamak istiyorum,
* **So that:** Sahne ağacını tam olarak görebilmek ve aktörlerin detaylı parametrelerini (Collider, Light, Mesh özellikleri vb.) otonom değiştirebilmek için.

#### 2. Technical Implementation Notes
* `UnrealClient` sınıfına `get_scene_hierarchy` ve `get_actor_components` fonksiyonları eklenecektir.
* `unreal_get_scene_hierarchy` aracıyla sahnede aktif tüm aktörlerin listesi ve sınıf yolları (`Default__EditorActorSubsystem` çağrısıyla) çekilecektir.
* `unreal_get_actor_components` aracıyla seçilen aktörün alt bileşenleri sorgulanacaktır.

#### 3. Acceptance Criteria (AC)
* [ ] **AC_01:** `unreal_get_scene_hierarchy` çağrısı, aktif level içindeki tüm aktör nesnelerini sınıf ve object path bilgileriyle birlikte JSON listesi olarak hatasız getirmelidir.
* [ ] **AC_02:** `unreal_get_actor_components` çağrısı, belirtilen bir aktörün tüm bileşen sınıflarını (Component Class) listelemelidir.
* [ ] **AC_03:** Sahne sorguları local ağ gecikmesi kurallarına uyarak **50ms altında** yanıt vermelidir.

---

### PBI_008: Dinamik Blueprint ve Prefab Spawning Sistemi

**Gereksinim Linkleri:**
* SRD Link: `[REQ_SRD_UE5_08]` (Özel Blueprint ve Varlık Spawning)
* TDD Link: `[REQ_TDD_ARC_10]` (Blueprint class yollarının dinamik yansıma ile çözümlenmesi)

**Sprint:** Sprint 03 (v2.0)  
**Owner (Geliştirici):** @core-arch  
**Status:** Backlog  

---

#### 1. User Story
* **As a:** Otonom Oyun Tasarımcısı olarak,
* **I want to:** MVP kapsamındaki 4 temel sınıf dışındaki özel Blueprint ve prefab sınıflarını dinamik yükleyerek sahneye spawn etmek istiyorum,
* **So that:** Projede geliştirilmiş olan düşman, kapı, sandık veya özel nesneleri sahne üzerinde özgürce yerleştirebilmek için.

#### 2. Technical Implementation Notes
* `spawn_actor` aracı, parametrik olarak herhangi bir Blueprint sınıf yolunu (`/Game/Blueprints/BP_Actor.BP_Actor_C`) kabul edecek şekilde genişletilecektir.
* Girilen sınıf yolunun geçerliliği spawn edilmeden önce uzaktan sorgulanacak (Asset Registry kontrolü), geçersiz yollarda işlem reddedilecektir.

#### 3. Acceptance Criteria (AC)
* [ ] **AC_01:** `/Game/` altındaki özel bir Blueprint sınıfı yol gösterildiğinde, `spawn_actor` belirtilen lokasyonda aktörü başarıyla yaratmalı ve sahne referansını dönmelidir.
* [ ] **AC_02:** Geçersiz veya bozuk bir sınıf yolu gönderildiğinde, sistem hata vermeli ve hata mesajında "ASSET_NOT_FOUND" uyarısı verilmelidir.

---

### PBI_009: Editör Undo/Redo & Geri Alma Desteği

**Gereksinim Linkleri:**
* SRD Link: `[REQ_SRD_UE5_09]` (Editör İşlemleri Undo/Redo Kontrolü)
* TDD Link: `[REQ_TDD_ARC_11]` (Unreal `EditorUndo` transaction entegrasyonu)

**Sprint:** Sprint 03 (v2.0)  
**Owner (Geliştirici):** @core-arch  
**Status:** Backlog  

---

#### 1. User Story
* **As a:** Yapay Zeka Ajanı ile pair programming yapan bir Geliştirici olarak,
* **I want to:** Ajanın editörde yaptığı hatalı sahne işlemlerini Undo ve Redo araçlarıyla geri alabilmek veya ileri sarabilmek istiyorum,
* **So that:** Ajanın yaptığı hataları manuel düzeltmekle vakit kaybetmeden tek komutla editör geçmişini yönetebilmek için.

#### 2. Technical Implementation Notes
* `UnrealClient` sınıfına `unreal.EditorUndo` API'sini tetikleyen HTTP/REST Remote Control endpoints eklenecektir.
* `unreal_editor_undo` ve `unreal_editor_redo` araçları MCP sunucusuna eklenecektir.

#### 3. Acceptance Criteria (AC)
* [ ] **AC_01:** `unreal_editor_undo` çağrıldığında, ajanın sahne üzerinde yaptığı son spawn veya transformasyon değişikliği editör geçmişinden başarıyla geri alınmalı (Undo) ve viewport anında güncellenmelidir.
* [ ] **AC_02:** Undo yapılan bir işlem `unreal_editor_redo` ile başarıyla ileri sarılmalıdır (Redo).

---

### QA & Test Lead Onayı
* **Durum:** L2 Product Backlog Items (PBI) ve Evrensel Bitti Tanımı (DoD) oluşturuldu. Bir sonraki aşama olan L4 QA & Test Planı (QA.md) aşamasına geçmek için kullanıcı onayı bekleniyor.
* **Karar/Onay İmzası:** *Beklemede...*
