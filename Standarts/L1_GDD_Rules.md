# L1-A: GAME DESIGN DOCUMENT (GDD) OLUŞTURMA VE YAZIM KILAVUZU

**Proje Kodu:** ALM_GDD_STANDARDS  
**Versiyon:** v1.0:0  
**Doküman Sahibi:** Game Director / Product Owner  
**Sistem Durumu:** KİLİTLİ / ZORUNLU UYGULAMA  

---

## 1. GDD Nedir? (Fonksiyonel Gereksinim Tanımı)

**Game Design Document (GDD)**; bir oyunun mekaniklerini, sistem kurallarını, oyuncu döngülerini, arayüz (UI/UX) akışlarını ve bölüm tasarımı (Level Design) yönergelerini tanımlayan **L1-A seviyesi fonksiyonel gereksinim dokümanıdır**.

Otomotiv veya yazılım mühendisliğindeki **"Functional Specification" (Fonksiyonel Şartname)** belgesinin oyun sektöründeki tam karşılığıdır. GDD, sistemin yazılımsal mimarisini (TDD) veya görsel varlık standartlarını (ADD) belirlemez; sadece **oyunun kuralları ve oyuncu deneyiminin matematiksel/mantıksal çerçevesini** çizer.

---

## 2. GDD Yazım Kanunları ve Tasarım Prensipleri

GDD yazılırken aşağıdaki metodolojik kurallara uyulması zorunludur. Bu kuralları ihlal eden tasarım metinleri TDD ve Üretim (Backlog) fazına geçemez.

* **Yoruma Kapalı ve Net Dil:** "Karakter çok hızlı koşar", "Düşman güçlü bir darbe vurur" gibi sübjektif ifadeler yasaktır. Yerine: "Karakter temel koşu hızından (Base_Speed) %50 daha hızlı hareket eder", "Düşman oyuncuya 25 HP saf hasar (True Damage) verir" şeklinde metrik tabanlı yazılmalıdır.
* **Yazılımdan Bağımsızlık:** GDD içinde "C++", "Blueprint", "Line Trace", "Tick Fonksiyonu" gibi yazılımsal terimler kullanılmamalıdır. Tasarımcı mekaniği mantıksal kurallarla (State Machine, If/Else koşulları) anlatmalıdır. Nasıl kodlanacağı tamamen TDD'nin konusudur.
* **Modülerlik:** Her mekanik kendi içinde bağımsız birer fonksiyonel modül olarak tasarlanmalıdır. Bir mekaniğin değişmesi, diğer sistemlerin temel mantığını çökertmemelidir.

---

## 3. İzlenebilirlik ve Bağlantı Kuralları (Traceability)

GDD, hiyerarşide L0 (Vision Document) ile L1-B (TDD) ve L2 (Product Backlog) arasında bir köprüdür.

* **Yukarı Doğru Bağlantı (Backward Traceability):** GDD'de yazılan her ana başlık veya mekanik grubu, L0 vizyon dökümanındaki en az bir kısıta bağlanmalıdır. 
  * *Örnek:* `# 3. Kombi Sistemi (Ref: [REQ_VD_SCP_01])`
* **Aşağı Doğru Bağlantı (Forward Traceability):** Her GDD maddesi, teknik karşılığının yazılması için TDD'ye ve iş paketine bölünmesi için Product Backlog'a (`PBI`) referans verilerek kırılmalıdır.
* **GDD ID Standartı:** GDD içindeki her atomik gereksinim `REQ_GDD_[MODÜL]_[NUMARA]` formatında kodlanmalıdır.
  * `REQ_GDD_CMB_01`: Kombat Modülü, 1. Gereksinim.
  * `REQ_GDD_UI_12`: Arayüz Modülü, 12. Gereksinim.

---

## 4. L1-A: Standart GDD Şablonu (Boş Matris)

*Yeni bir modül veya mekanik tasarlanırken kopyalanıp doldurulacak resmi şablondur:*

```markdown
# GDD: [MODÜL ADI] (Örn: Karakter Hareket Sistemi)

**Modül Kodu:** REQ_GDD_[MODÜL_KODU]  
**Bağlı Olduğu L0 Kısıtı:** [REQ_VD_XXX]  
**Versiyon:** v0.1:0  
**Tasarımcı:** [Adınız / Rolünüz]  

---

### 1. Mekanik Özet ve Amacı
[Bu mekaniğin oyundaki işlevi nedir? Oyuncuya hangi oyun zevkini/hissiyatını vermeyi amaçlıyor? Kısa özeti.]

---

### 2. Fonksiyonel Gereksinimler Listesi (Requirements Matrix)

| Gereksinim ID | Fonksiyon / Kural Adı | Mantıksal Koşul ve Kural Açıklaması |
| :--- | :--- | :--- |
| **[REQ_GDD_XXX_01]** | [Örn: Temel Hareket] | [Oyuncu W,A,S,D tuşlarına bastığında karakter yöne doğru ivmelenir. Maksimum hız X Unreal Unit'tir.] |
| **[REQ_GDD_XXX_02]** | [Örn: Durma Ataleti] | [Oyuncu hareket tuşlarını bıraktığında karakter anında durmaz; X saniye boyunca sürtünme ile yavaşlar.] |

---

### 3. Durum Makinesi (State Machine) Kuralları
*Mekaniğin sahip olduğu durumlar (States) ve bu durumlar arası geçiş tetikleyicileri:*

* **IDLE State:** Karakter hareket etmiyor.
  * *Geçiş Koşulu:* `Hareket_Girdisi > 0` ise `MOVE` durumuna geç.
* **MOVE State:** Karakter ivmeleniyor veya maksimum hızda koşuyor.
  * *Geçiş Koşulu:* `Hareket_Girdisi == 0` ise `IDLE` durumuna geç.
  * *Geçiş Koşulu:* `Hasar_Alındı == True` ve `Stun_Süresi > 0` ise `STUNNED` durumuna geç.

---

### 4. Kullanıcı Arayüzü (UI/UX) ve Geri Bildirim (Feedback) Kuralları
*Mekaniğin oyuncuya görsel ve işitsel olarak nasıl yansıtılacağı:*

* **Görsel Feedback (VFX/Animasyon):** Karakter `MOVE` durumuna geçtiğinde ayaklarından toz efekti tetiklenmelidir.
* **İşitsel Feedback (SFX):** Karakterin bastığı zemine göre (Metal, Toprak) dinamik ayak sesi (Footstep Audio) tetiklenmelidir (Ref: Audio Design).
* **Arayüz (UI):** Karakterin hızı maksimuma ulaştığında ekrandaki Motion Blur efekti %5 oranında artmalıdır.