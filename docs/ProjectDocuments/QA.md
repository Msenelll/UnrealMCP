# L4: KALİTE GÜVENCE VE TEST PLANI (QA & TEST PLAN)

**Proje Kodu:** LUDUS_MCP_2026  
**Doküman Kodu:** QA_MASTER_01  
**Versiyon:** v0.1:0  
**Doküman Sahibi:** @qa-nexus (System Integrator & QA Lead)  
**Sistem Durumu:** İNCELEMEDE / GATED STEP 5  

---

## 1. Test Ortamı ve Ön Koşullar (Pre-conditions)

Tüm kalite güvence ve entegrasyon testlerinin hatasız yürütülebilmesi için test makinesinin aşağıdaki konfigürasyona sahip olması zorunludur:

* **İşletim Sistemi:** Windows 10/11 Pro (x64)
* **Unreal Engine Sürümü:** UE 5.3+ (Remote Control API eklentisi aktif, Web Server portu `30010` açık olmalıdır)
* **Blender Sürümü:** Blender 4.0+ (Headless CLI çalıştırılabilir ve sistem PATH değişkenlerine veya sunucu konfigürasyonuna eklenmiş olmalıdır)
* **Python Sürümü:** Python 3.10+ (MCP SDK kurulu, `aiohttp` ve `asyncio` modülleri hazır olmalıdır)

---

## 2. Test Senaryoları Matrisi (Verification Matrix)

---

### TC_QA_INT_PBI001_A: MCP Sunucu Handshake ve stdio Başlangıç Testi

* **İlgili İş Paketi Linki:** `[PBI_001]`  
* **Referans Tasarım Linkleri:** SRD: `[REQ_SRD_INT_02]` | TDD: `[REQ_TDD_ARC_01]`  
* **Test Türü:** Otomasyon (Unit & Transport Automation)  
* **Test Sorumlusu:** @qa-nexus  
* **Test Durumu:** [ ] PASSED / [ ] FAILED / [ ] BLOCKED  

#### 1. Ön Koşullar (Pre-conditions)
* Python terminali ve çalışma alanı `C:\repo\2_UnrealMCP` dizininde olmalıdır.
* Gerekli sanal ortam (`.venv`) aktif edilmiş olmalıdır.

#### 2. Test Adımları ve Doğrulama Protokolü
| Adım No | Yapılacak Eylem (Step) | Beklenen Çıktı (Expected Result) | Durum (Pass/Fail) |
| :--- | :--- | :--- | :--- |
| **01** | Python terminali üzerinden sunucuyu stdio modunda çalıştır: `python -m src.unreal_server.server` | Sunucu çökmeksizin başlar ve stdio transport kanalında input almaya hazır bekler. | [ ] Pass / [ ] Fail |
| **02** | Stdio kanalından MCP el sıkışma JSON-RPC 2.0 initialize request paketi gönder. | Sunucu, initialize response paketini standart şemada geri döner. | [ ] Pass / [ ] Fail |
| **03** | Stdio kanalından `tools/list` isteği gönder. | Sunucu, tanımlı `unreal_get_viewport_telemetry`, `unreal_spawn_actor`, `unreal_live_coding_trigger` araç şablonlarını listeler. | [ ] Pass / [ ] Fail |

---

### TC_QA_UE5_PBI002_A: Remote Control Viewport Telemetry Okuma Testi

* **İlgili İş Paketi Linki:** `[PBI_002]`  
* **Referans Tasarım Linkleri:** SRD: `[REQ_SRD_UE5_01]` | TDD: `[REQ_TDD_ARC_02]`  
* **Test Türü:** Entegrasyon Testi  
* **Test Sorumlusu:** @qa-nexus  
* **Test Durumu:** [ ] PASSED / [ ] FAILED / [ ] BLOCKED  

#### 1. Ön Koşullar (Pre-conditions)
* Unreal Engine 5 Editörü açık olmalı, Remote Control API aktif olmalı ve localhost:30010 üzerinden erişilebilir olmalıdır.

#### 2. Test Adımları ve Doğrulama Protokolü
| Adım No | Yapılacak Eylem (Step) | Beklenen Çıktı (Expected Result) | Durum (Pass/Fail) |
| :--- | :--- | :--- | :--- |
| **01** | Stdio üzerinden `unreal_get_viewport_telemetry` araç çağrısını tetikle. | MCP Sunucu, Unreal Remote Control API'ye HTTP isteği atıp kamera konum ve rotasyon verilerini asenkron okur. | [ ] Pass / [ ] Fail |
| **02** | Unreal editör kamerasını manuel hareket ettir ve aracı tekrar çağır. | Dönen koordinatların değiştiği ve editör kamerasının anlık yeni koordinatlarını tam doğrulukla döndürdüğü doğrulanır. | [ ] Pass / [ ] Fail |
| **03** | Local istek-yanıt süresini ölç. | Telemetry verisinin gelme süresi uçtan uca **50ms altında** olmalıdır (REQ_VD_TEC_01). | [ ] Pass / [ ] Fail |

---

### TC_QA_UE5_PBI002_B: Remote Control Spawn ve Transform Manipülasyon Testi

* **İlgili İş Paketi Linki:** `[PBI_002]`  
* **Referans Tasarım Linkleri:** SRD: `[REQ_SRD_UE5_02]`, `[REQ_SRD_UE5_03]` | TDD: `[REQ_TDD_ARC_02]`  
* **Test Türü:** Entegrasyon / Görsel Doğrulama  
* **Test Sorumlusu:** @qa-nexus  
* **Test Durumu:** [ ] PASSED / [ ] FAILED / [ ] BLOCKED  

#### 1. Ön Koşullar (Pre-conditions)
* Unreal Engine editörü boş bir sahnede (level) hazır durumda olmalıdır.

#### 2. Test Adımları ve Doğrulama Protokolü
| Adım No | Yapılacak Eylem (Step) | Beklenen Çıktı (Expected Result) | Durum (Pass/Fail) |
| :--- | :--- | :--- | :--- |
| **01** | `unreal_spawn_actor` aracıyla, `PointLight` aktör tipini `{"x": 100, "y": 0, "z": 200}` koordinatında spawn et. | Unreal editör viewport'unda yeni bir PointLight aktörünün spawn olduğu ve sahneyi aydınlattığı teyit edilir. | [ ] Pass / [ ] Fail |
| **02** | Spawn edilen aktörün ID'sini alarak `unreal_set_actor_transform` aracıyla rotasyonunu `{"pitch": 45, "yaw": 90, "roll": 0}` olarak set et. | Aktörün rotasyonunun editörde anında görsel olarak güncellendiği doğrulanır. | [ ] Pass / [ ] Fail |

---

### TC_QA_UE5_PBI003_A: Live Coding Tetikleme ve PIE Engelleme Testi

* **İlgili İş Paketi Linki:** `[PBI_003]`  
* **Referans Tasarım Linkleri:** SRD: `[REQ_SRD_UE5_04]` | TDD: `[REQ_TDD_ARC_03]`  
* **Test Türü:** Güvenlik ve Hata Yakalama Testi  
* **Test Sorumlusu:** @qa-nexus  
* **Test Durumu:** [ ] PASSED / [ ] FAILED / [ ] BLOCKED  

#### 1. Ön Koşullar (Pre-conditions)
* Unreal Engine editörü açık ve **PIE (Play In Editor)** modunda aktif çalışıyor olmalıdır.

#### 2. Test Adımları ve Doğrulama Protokolü
| Adım No | Yapılacak Eylem (Step) | Beklenen Çıktı (Expected Result) | Durum (Pass/Fail) |
| :--- | :--- | :--- | :--- |
| **01** | Stdio üzerinden `unreal_live_coding_trigger` komutunu gönder. | MCP sunucu editör durumunun meşgul/PIE olduğunu tespit eder. | [ ] Pass / [ ] Fail |
| **02** | Dönen hata kodunu denetle. | Komut derhal reddedilmeli, derleme asenkron süreci başlatılmamalı ve açıklayıcı bir "PIE_ACTIVE_REJECTED" hatası dönmelidir. | [ ] Pass / [ ] Fail |

---

### TC_QA_UE5_PBI003_B: Asenkron RunUAT Paketleme ve Log Akış Testi

* **İlgili İş Paketi Linki:** `[PBI_003]`  
* **Referans Tasarım Linkleri:** SRD: `[REQ_SRD_UE5_05]` | TDD: `[REQ_TDD_ARC_04]`  
* **Test Türü:** Performans ve Alt Süreç (Subprocess) Testi  
* **Test Sorumlusu:** @qa-nexus  
* **Test Durumu:** [ ] PASSED / [ ] FAILED / [ ] BLOCKED  

#### 1. Ön Koşullar (Pre-conditions)
* Test bilgisayarında paketlenebilir bir C++ Unreal projesinin yolu tanımlanmış olmalıdır.

#### 2. Test Adımları ve Doğrulama Protokolü
| Adım No | Yapılacak Eylem (Step) | Beklenen Çıktı (Expected Result) | Durum (Pass/Fail) |
| :--- | :--- | :--- | :--- |
| **01** | `unreal_package_project` aracıyla paketleme komutunu asenkron tetikle. | Arka planda bağımsız asenkron Windows alt süreci (UAT) başlatılır. Python sunucusu kilitlenmez. | [ ] Pass / [ ] Fail |
| **02** | Paketleme log akışını (output stream) denetle. | Loglar `asyncio.StreamReader` üzerinden satır satır okunur, tıkanma yaşanmaz ve MCP kanalı aktiftir. | [ ] Pass / [ ] Fail |
| **03** | Paketleme bittiğinde süreci denetle. | Süreç exit koduna göre başarıyla kapanır. Bellek kullanımı olağan sınırlarda kalır (VRAM sızıntısı yoktur). | [ ] Pass / [ ] Fail |

---

### TC_QA_BLN_PBI004_A: Blender Headless Prosedürel Mesh Sentez Testi

* **İlgili İş Paketi Linki:** `[PBI_004]`  
* **Referans Tasarım Linkleri:** SRD: `[REQ_SRD_BLN_01]`, `[REQ_SRD_BLN_02]` | TDD: `[REQ_TDD_ARC_05]`  
* **Test Türü:** Procedural Otomasyon Testi  
* **Test Sorumlusu:** @qa-nexus  
* **Test Durumu:** [ ] PASSED / [ ] FAILED / [ ] BLOCKED  

#### 1. Ön Koşullar (Pre-conditions)
* Blender yerel kurulum yolu sunucuda tanımlanmış olmalıdır.

#### 2. Test Adımları ve Doğrulama Protokolü
| Adım No | Yapılacak Eylem (Step) | Beklenen Çıktı (Expected Result) | Durum (Pass/Fail) |
| :--- | :--- | :--- | :--- |
| **01** | `blender_generate_procedural_mesh` aracını tetikle. Parametreler: `{"shape": "cylinder", "radius": 0.5, "height": 2.0}` | Headless Blender asenkron süreci sessizce başlatılır ve python bpy scripti enjekte edilir. | [ ] Pass / [ ] Fail |
| **02** | Üretilen varlık dosyasını geçici klasörde (`Temp`) denetle. | Belirtilen parametrik boyutlarda `.fbx` uzantılı dosyanın hatasız oluşturulduğu doğrulanır. | [ ] Pass / [ ] Fail |
| **03** | Blender çalışırken 30 saniyelik timeout sınırını aşmasını bekle (Mock test). | Sunucu, süreci zorla kapatmalı (kill) ve sunucunun kilitlenmesini engellemelidir. | [ ] Pass / [ ] Fail |

---

### TC_QA_INT_PBI005_A: Blender-UE5 FBX Entegrasyon Köprüsü ve Eksen Hizalama Testi

* **İlgili İş Paketi Linki:** `[PBI_005]`  
* **Referans Tasarım Linkleri:** SRD: `[REQ_SRD_BLN_03]`, `[REQ_SRD_INT_01]` | TDD: `[REQ_TDD_ARC_06]` | PID: `[REQ_PID_AST_02]`  
* **Test Türü:** Uçtan Uca (End-to-End) Entegrasyon Testi  
* **Test Sorumlusu:** @qa-nexus  
* **Test Durumu:** [ ] PASSED / [ ] FAILED / [ ] BLOCKED  

#### 1. Ön Koşullar (Pre-conditions)
* Blender otonom model üretmiş, geçici klasöre kaydetmiş ve Unreal Engine editörü açık durumda olmalıdır.

#### 2. Test Adımları ve Doğrulama Protokolü
| Adım No | Yapılacak Eylem (Step) | Beklenen Çıktı (Expected Result) | Durum (Pass/Fail) |
| :--- | :--- | :--- | :--- |
| **01** | FBX ithalat köprüsünü `/Game/ProceduralAssets/` hedef yoluyla asenkron tetikle. | Dosya Unreal Engine Remote Control ImportTask API ile sessizce ithal edilir. | [ ] Pass / [ ] Fail |
| **02** | Unreal Editor içerisinde ithal edilen Static Mesh objesini sorgula ve sahneye spawn et. | Modelin pivot noktasının tam taban-merkezinde (zemin seviyesinde) olduğu görsel olarak teyit edilir. | [ ] Pass / [ ] Fail |
| **03** | Model eksenlerini ve ölçeğini doğrula. | Modelin Unreal eksenleri (Z-up, -X Forward) ile tam uyumlu olduğu ve boyut sapması (scale drift) yaşamadığı teyit edilir. | [ ] Pass / [ ] Fail |

---

## 3. Ek Kalite Doğrulamaları (Performans & Güvenlik Kapısı)

* [ ] **Bellek Sızıntısı Kontrolü:** Alt süreçlerin (UAT, Blender, Python asyncio) kapatıldıktan sonra RAM veya VRAM üzerinde yetim işlem (zombie process) veya bellek sızıntısı (memory leak) bırakmadığı görev yöneticisi/otomasyon loglarıyla taranacaktır. (Ref: `[REQ_VD_TEC_04]`)
* [ ] **Arayüz Gecikme Spikeları (Spikes):** Unreal viewportTelemetry tetiklendiğinde oyun editörü frame rate değerinin stabil kaldığı, anlık donmaların (hitch/freeze) yaşanmadığı doğrulanacaktır. (Ref: `[REQ_VD_TEC_01]`)

---

### QA & Release Lead Onayı
* **Durum:** L4 QA & Test Planı (QA.md) oluşturuldu. Tüm dökümantasyon kilitlendi. Üretim geliştirme fazına (Phase 3: Kodlama) geçmek için kullanıcı onayı bekleniyor.
* **Karar/Onay İmzası:** *Beklemede...*
