# L2: PRODUCT BACKLOG ITEMS (PBI) & BITTI TANIMI (DoD)

**Proje Kodu:** LUDUS_MCP_2026  
**Doküman Kodu:** PBI_MASTER_01  
**Versiyon:** v0.1:0  
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

### QA & Test Lead Onayı
* **Durum:** L2 Product Backlog Items (PBI) ve Evrensel Bitti Tanımı (DoD) oluşturuldu. Bir sonraki aşama olan L4 QA & Test Planı (QA.md) aşamasına geçmek için kullanıcı onayı bekleniyor.
* **Karar/Onay İmzası:** *Beklemede...*
