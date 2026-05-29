# L2: PRODUCT BACKLOG ITEM (PBI) OLUŞTURMA VE YAZIM KILAVUZU

**Proje Kodu:** ALM_PBI_STANDARDS  
**Versiyon:** v1.0:0  
**Doküman Sahibi:** Producer / QA Lead  
**Sistem Durumu:** KİLİTLİ / ZORUNLU UYGULAMA  

---

## 1. PBI Nedir? (Çevik İş Paketi Tanımı)

**Product Backlog Item (PBI)**; üst katmandaki GDD, TDD ve ADD dokümanlarında kilitlenen mimari gereksinimlerin, sprint içerisinde tamamlanabilecek, net bir teslimat değerine sahip, atomik ve yoruma kapalı parçalara bölünmüş **L2 seviyesi iş paketidir**.

Otomotiv yazılım süreçlerindeki **"Component Level Specification"** veya Çevik (Agile/Scrum) metodolojilerindeki **User Story / Epic** kavramının tam karşılığıdır. Bir PBI, işin yazılımsal veya tasarımsal olarak "nasıl" yapılacağını (How) tartışmaz; QA ekibinin test edebileceği şekilde **"ne" üretileceğini (What) ve "neden" üretileceğini (Why)** kesin çizgilerle tarif eder.

---

## 2. PBI Yazım Kanunları ve Esnetilemez Kurallar

Backlog listesinde yer alacak her PBI, yorum farklarını ve "bence oldu" krizlerini engellemek için şu 4 altın kurala uymak zorundadır:

* **User Story Formatı Zorunluluğu:** PBI başlığı ve ana tanımı her zaman oyuncu veya geliştirici perspektifinden yazılmalıdır: *"Bir [Rol] olarak, [Eylem] yapmak istiyorum, böylece [Fayda/Değer] sağlayacağım."*
* **Yoruma Kapalı Kabul Kriterleri (Acceptance Criteria - AC):** Bir PBI'ın içine "Kombat akıcı hissettirmeli" yazılamaz. QA uzmanının sadece "EVET/HAYIR" diyebileceği test edilebilir kriterler yazılmalıdır.
* **Evrensel Bitti Tanımı (Definition of Done - DoD) Uyumluluğu:** PBI, projenin genel DoD kurallarını (Örn: Kod analizi, RAM bütçesi, branch kuralı) karşılamadan "Done" sütununa taşınamaz.
* **Net Görev Sorumlusu (Owner):** Her PBI'ın üretim bandında tek bir sorumlusu (Owner) olmak zorundadır. Sahipsiz iş paketleri sprint planlamasına dahil edilemez.

---

## 3. Çift Yönlü İzlenebilirlik ve Linkleme Kuralları (Traceability)

PBI, ALM (Application Lifecycle Management) dashboard'unun kalbidir. Yukarıdaki mimari ile aşağıdaki kod satırlarını birbirine bağlar.

* **Üst Katman Bağlantıları (Backward Traceability):** Her PBI kartı, türetildiği GDD, TDD ve ADD kimlik numaralarını (ID) taşımak zorundadır. Bu linklerden biri eksikse PBI "Kaçak Tasarım" veya "Yetim İş" (Orphan) olarak işaretlenir ve dashboard'da kırmızı alarm verir.
  * *Örnek:* `Links: [REQ_GDD_CMB_04], [REQ_TDD_ARC_12], [REQ_ADD_MOD_01]`
* **Alt Katman Bağlantıları (Forward Traceability):** PBI'ı gerçekleştirmek için feature branch açılırken ve commit atılırken PBI ID'si kullanılmalıdır.
  * *Örnek Branch:* `feature/PBI_042-character-double-jump`
* **PBI ID Standartı:** Backlog'daki her iş paketi ardışık olarak `PBI_[NUMARA]` şeklinde kodlanmalıdır. (Örn: `PBI_001`, `PBI_042`).

---

## 4. L2: Standart PBI Şablonu (Boş Matris)

*Jira, Notion veya GitHub Projects üzerinde yeni bir iş paketi kartı açılırken kopyalanıp doldurulacak resmi şablondur:*

```markdown
# PBI_[NUMARA]: [İŞ PAKETİ ADI] (Örn: PBI_042: Karakter Çift Zıplama Mekaniği)

**Gereksinim Linkleri:** * GDD Link: [REQ_GDD_XXX_XX]
* TDD Link: [REQ_TDD_XXX_XX]
* ADD Link: [REQ_ADD_XXX_XX] (Varsa)

**Sprint:** Sprint [XX]  
**Owner (Sorumlu Personel/Ajan):** [Geliştirici İsmi / Yapay Zeka Ajanı]  
**Status:** Backlog / In Progress / QA Testing / Done  

---

### 1. User Story (Kullanıcı Hikayesi)
* **As a (Kim):** Savaş mekaniklerinde uzmanlaşmak isteyen bir Oyuncu olarak,
* **I want to (Ne):** Havada bir kez daha zıplama tuşuna basarak "Çift Zıplama" (Double Jump) yapabilmek istiyorum,
* **So that (Neden):** Düşman saldırılarından dikey düzlemde kaçınabilmek ve platform öğelerini aşabilmek için.

---

### 2. Technical Implementation Notes (Nasıl Yapılacak? - L3 Seviyesine Yönlendirme)
*Bu kısım TDD'den referans alınarak yazılır ve işi yapacak kişiye teknik rotayı tarif eder:*
* `AGenesisCharacter` sınıfı içerisindeki `JumpCurrentCount` parametresi kontrol edilecek.
* Maksimum zıplama sınırı `2` olarak kilitlenecek.
* Havada ikinci zıplama tetiklendiğinde `UCombatComponent` üzerindeki enerji state'i kontrol edilecek.

---

### 3. Acceptance Criteria (AC - Kabul Kriterleri)
*QA ekibinin görevi onaylamak veya reddetmek için uygulayacağı kesin test şartları:*

* [ ] **AC_01:** Karakter yerdeyken zıplama tuşuna (Space) basıldığında normal zıplama animasyonu tetiklenmeli ve dikey ivme kazanmalıdır.
* [ ] **AC_02:** Karakter dikey yükseliş veya düşüş anındayken (havada) Space tuşuna ikinci kez basıldığında ikinci zıplama tetiklen