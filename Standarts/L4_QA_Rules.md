# L4: QA & TEST PLAN (KALİTE GÜVENCE VE TEST PLANI KILAVUZU)

**Proje Kodu:** ALM_L4_QA_STANDARDS  
**Versiyon:** v1.0:0  
**Doküman Sahibi:** QA Lead / Test Automation Architect  
**Sistem Durumu:** KİLİTLİ / ZORUNLU UYGULAMA  

---

## 1. L4 Katmanının Tanımı ve Amacı

**L4: QA & Test Plan**; L3 (Code & Asset Execution) katmanında feature branch'ler üzerinde geliştirilen tüm yazılım bileşenlerinin ve sanatsal varlıkların, L2 katmanında kilitlenen **Kabul Kriterlerine (Acceptance Criteria)** ve L0 katmanında kilitlenen **Üretim Kısıtlarına (Production Constraints)** uygunluğunu doğrulayan **kalite güvence ve test katmanıdır**.

Otomotiv yazılım mühendisliğindeki (ASPICE) **"Software Integration Test"** ve **"Software Verification"** aşamalarının oyun sektöründeki tam karşılığıdır. L4 katmanının ana amacı; subjektif "bence test ettim, çalışıyor" algısını yıkarak, projenin her aşamasını yoruma kapalı, tekrarlanabilir ve matematiksel test senaryolarına (Test Cases) bağlamaktır.

---

## 2. Test Senaryosu (Test Case) Yazım Standartları

QA ekibi veya test otomasyon mekanizmaları, testleri doğrusal olmayan yöntemlerle değil, önceden tanımlanmış matrislere göre işletir. Her test senaryosu şu anatomiyi korumak zorundadır:

### Numaralandırma ve Kimlik Kuralları (ID Syntax)
TC_QA_[MODÜL_KODU][PBI_ID][ARTIŞLI_HARF]

### Test Senaryosu Şablonu
* **Test Case ID:** TC_QA_CMB_PBI_042_01 (Kombat Modülü, PBI-042, 1. Test)
* **Pre-Conditions (Ön Koşullar):** Geliştirici tarafından sağlanması gereken durumlar (Örn: Karakter "Grounded" durumunda olmalıdır).
* **Test Steps (Adımlar):** Otomasyonun izleyeceği sıralı komutlar veya manuel test adımları.
* **Expected Results (Beklenen Sonuç):** PBI'ın Kabul Kriterlerine uygun, yoruma kapalı sonuç.
* **Actual Results (Gerçek Sonuç):** Test sonucunda elde edilen değerler.
* **Status (Durum):** PASS / FAIL / BLOCKED

* `TC_QA_CMB_PBI042_A`: Kombat modülü, `PBI_042` iş paketine bağlı, ilk (A) test senaryosu.

### Esnetilemez Yazım Kuralları
* **Ön Koşul (Pre-conditions) Tanımı:** Test başlamadan önce oyun motorunun, haritanın ve aktörün içinde bulunması gereken kesin durum belirtilmelidir.
* **Adım Adım Eylem (Steps):** Testi koşan kişinin yoruma yer bırakmayacağı net fiziksel eylemler (Örn: "Klavyeden `Shift` tuşuna basılı tutarak `W` tuşuna bas").
* **Beklenen Çıktı (Expected Result):** Eylem sonucunda motorun veya arayüzün vermesi gereken kesin ve ölçülebilir tepki.

---

## 3. L4: Standart Test Senaryosu Şablonu (Boş Matris)

*Backlog'daki bir PBI "QA Testing" durumuna geldiğinde, QA uzmanının çalıştırmak üzere kopyalayıp dolduracağı resmi şablondur:*

```markdown
# TC_QA_[MODÜL]_[PBI_ID]_[HARF]: [TEST SENARYOSU ADI]

**İlgili İş Paketi Linki:** [PBI_XXX]  
**Referans Tasarım Linkleri:** GDD: [REQ_GDD_XXX_XX] | TDD: [REQ_TDD_XXX_XX]  
**Test Türü:** Manuel / Otomasyon (Unit-Automation)  
**Test Sorumlusu (Tester):** [QA Uzmanı veya Otomasyon Ajanı]  
**Test Durumu:** [ ] PASSED / [ ] FAILED / [ ] BLOCKED  

---

### 1. Test Ortamı ve Ön Koşullar (Pre-conditions)
* **Derleme / Build Sürümü:** v[A].[B]:[C] (Örn: v0.1:04)
* **Test Haritası / Sahnesi:** `Maps/TestMaps/TM_[ModulName]_Gym`
* **Gerekli Donanım / Profil:** [Örn: PC (RTX 3050) veya Mobil (iOS)]
* **Ön Koşul:** [Örn: Oyuncu karakterinin can havuzu (HP) %100 dolu ve hareketsiz (IDLE) olmalıdır.]

---

### 2. Test Adımları ve Doğrulama Protokolü (Execution Matrix)

| Adım No | Yapılacak Eylem (Step) | Beklenen Çıktı (Expected Result) | Durum (Pass/Fail) |
| :--- | :--- | :--- | :--- |
| **01** | [Eylemi yazın] | [Beklenen tepkiyi yazın] | [ ] Pass / [ ] Fail |
| **02** | [Eylemi yazın] | [Beklenen tepkiyi yazın] | [ ] Pass / [ ] Fail |
| **03** | [Eylemi yazın] | [Beklenen tepkiyi yazın] | [ ] Pass / [ ] Fail |

---

### 3. Ek Kalite Doğrulamaları (Performans & Sanat)
* [ ] **Performans Kontrolü:** Bu mekanik tetiklendiğinde anlık FPS düşüşü (FPS Spike) yaşandı mı? Frame-time $16.6\text{ ms}$ sınırını aştı mı? (Ref: `[REQ_VD_TEC_02]`)
* [ ] **Görsel Kontrol:** Karakter animasyonları oynarken mesh üzerinde yırtılma, titreme veya texture kayması meydana geldi mı? (Ref: `[REQ_ADD_XXX]`)

4. Hata Raporlama (Bug Lifecycle) ve Ters İzlenebilirlik
Bir test adımı FAILED (Başarısız) olarak işaretlendiğinde, QA sistemi otomatik olarak bir Hata Raporu (Bug Ticket) oluşturur. Hatanın sistemde kabul edilebilmesi için yukarı doğru izlenebilirlik bağı (Reverse Traceability) kurulmalıdır:

Hata Kartı ID Standartı
BUG_[PBI_ID]_[ARTIŞLI_NUMARA] -> Örn: BUG_PBI042_01
Ters İzlenebilirlik Zinciri (Reverse Traceability Chain)
Hata kartı, yazılımcının hatayı kökten çözebilmesi için şu hiyerarşik bağı taşımak zorundadır:

[BUG_PBI042_01] ──► [PBI_042] ──► [REQ_TDD_CMB_01] ──► [REQ_GDD_CMB_02] ──► [REQ_VD_TEC_02]