# L0: PROJE VİZYON DÖKÜMANI (VD) TANIM VE ŞABLON REHBERİ

**Proje Kodu:** ALM_VD_TEMPLATE_MASTER  
**Versiyon:** v1.0:0  
**Doküman Sahibi:** Game Director / Product Owner  
**Sistem Durumu:** KİLİTLİ / REFERANS KAYNAK  

---

## 1. Vision Document (VD) Nedir? (Mühendislik Tanımı)

**Vision Document (VD)**, bir projenin üst düzey anayasasıdır. Ürünün ticari, teknik, sanatsal ve kapsam (scope) sınırlarını belirleyen, pazar hedefleri ile fiziksel kısıtları tek bir noktada buluşturan **L0 seviyesi stratejik gereksinim dökümanıdır**.

Otomotiv mühendisliğindeki *Vehicle Target Specification (VTS)* veya savunma sanayiindeki *Sistem Gereksinim Dokümanı (SRD)* ne ise, dijital bir üretim bandında VD de odur. VD, oyunun "ne" olduğunu değil, **"hangi sınırlar ve kısıtlar altında var olacağını"** tanımlar.

> **Mühendislik Aksiyomu:** VD bir fantezi metni değildir; alt katmanlardaki GDD (Tasarım), TDD (Yazılım) ve ADD (Sanat) dökümanlarını kısıtlayan, bütçe aşımını (Feature Creep) ve performans çökmelerini daha tasarım aşamasındayken engelleyen bir bariyerdir.

---

## 2. VD Neden Gereklidir? Üretim Bandındaki Kritik Rolü

* **Kapsam Sapmasını Engeller (Feature Creep Control):** Geliştirme sürecinde akla gelen "Şu mekaniği de mi eklesek?" sorusunun eleneceği ilk yer burasıdır. Eğer fikir VD'deki kısıtlara uymuyorsa elenir.
* **Teknik ve Sanatsal Bütçeyi Kilitler:** Hedef donanım (Örn: Steam Deck), bellek (RAM/VRAM) ve frame-time sınırları burada kilitlendiği için, yazılımcı (TDD) mimariyi buna göre kurar, çizer (ADD) poligon sayısını buna göre optimize eder.
* **ALM ve İzlenebilirlik (Traceability) Başlangıcıdır:** Projedeki en küçük kod fonksiyonu veya asset, yukarı doğru izlendiğinde VD'deki bir kısıt veya hedefe (`REQ_VD_XXX`) bağlanmak zorundadır. Linki olmayan iş "kaçak üretimdir".

---

## 3. İzlenebilirlik Numaralandırma Standartları (ID Syntax)

Bir ALM (Notion, Jira veya GitHub Projects) sisteminde VD gereksinimlerinin hatasız filtrelenebilmesi için her madde şu formatta kodlanmalıdır:

`[REQ_VD]_[KATEGORİ]_[MADDENİN_NUMARASI]`

* **`REQ_VD_TEC_XX`**: Teknik ve Altyapı Kısıtları (RAM, CPU, FPS, Ağ Yapısı)
* **`REQ_VD_ART_XX`**: Görsel ve Sanatsal Performans Kısıtları (Poligon, Dokular, Animasyon)
* **`REQ_VD_SCP_XX`**: Kapsam ve MVP Sınırları (Harita sayısı, Karakter sayısı, Süre)
* **`REQ_VD_VAL_XX`**: Doğrulama ve Entegrasyon Kuralları

---

## 4. L0: Vision Document Canlı Şablonu (Üretime Hazır)

*Aşağıdaki şablon, yeni bir projeye başlandığında doğrudan kopyalanarak içi doldurulacak olan resmi ALM matrisidir:*

```markdown
# PROJE VİZYON DÖKÜMANI (VISION DOCUMENT)

**Proje Kodu:** [PROJE_KODU]  
**Versiyon:** v0.0:0  
**Doküman Sahibi:** Game Director / Product Owner  

---

### 1. Executive Summary (Proje Özeti)

* **Proje Adı:** [Geçici veya Resmi İsim]
* **Tür (Genre):** [Örn: Aksiyon-Roguelike, FPS, RPG vb.]
* **Kamera Açısı / Perspektif:** [Örn: İzometrik, First-Person, Third-Person]
* **Hedef Platform:** [Örn: PC (Steam), Mobil (iOS/Android), PS5]
* **Oyun Motoru:** [Örn: Unreal Engine 5.X (C++ & Blueprint)]
* **Elevator Pitch:** [Oyuncuya vaat edilen temel deneyimin, hedef kitleyle olan bağının tek paragraflık net özeti.]

---

### 2. Core Gameplay Loop (Çekirdek Oyun Döngüsü)

*Oyuncunun oyunda kalmasını sağlayan en temel makro döngü (3-4 adımdan oluşmalıdır):*

1. **[Adım 1 - Eylem]:** [Örn: Savaş ve Odaları Keşfet]
2. **[Adım 2 - Ödül]:** [Örn: Rün ve Enerji Kaynakları Topla]
3. **[Adım 3 - Kayıp]:** [Örn: Öl ve Ana Üsse (Hub) Geri Dön]
4. **[Adım 4 - Gelişim]:** [Örn: Toplanan Kalıcı Paralarla Karakter Şasisini Güçlendir]

---

### 3. Unique Selling Points (USP - Benzersiz Satış Noktaları)

* **[USP_01]:** [Rakiplerde olmayan, pazarda bu ürünü öne çıkaracak ilk büyük mekanik veya sistem.]
* **[USP_02]:** [Oyunu özgün kılan dinamik veya tasarımsal unsur.]
* **[USP_03]:** [Teknik veya görsel olarak fark yaratan inovasyon.]

---

### 4. Production Constraints Matrix (Üretim Kısıtları Matrisi)

| Gereksinim ID | Kategori | Açıklama ve Kesin Sınır |
| :--- | :--- | :--- |
| **[REQ_VD_TEC_01]** | Ağ Yapısı (Networking) | [Örn: Oyun kesinlikle single-player olacaktır. Kod tabanında çok oyunculu replikasyon mimarisi kurulmayacaktır.] |
| **[REQ_VD_TEC_02]** | Performans Hedefi | [Örn: Hedef donanımda (Örn: RTX 3050) 1080p çözünürlükte stabil 60 FPS. Maksimum frame-time bütçesi 16.6 ms.] |
| **[REQ_VD_TEC_03]** | Bellek Bütçesi | [Örn: Maksimum 8 GB Sistem RAM ve 4 GB VRAM kullanımı.] |
| **[REQ_VD_ART_01]** | Sanat Stili | [Örn: Stylized 3D (Hand-painted). Fotogerçekçi asset kullanımı yasaktır.] |
| **[REQ_VD_ART_02]** | Poligon Bütçesi | [Örn: Ana karakter maks 15.000, düşmanlar maks 7.500 Tris (LOD 0).] |
| **[REQ_VD_SCP_01]** | MVP / Dikey Kesit Sınırı | [Örn: İlk aşamada 1 karakter, 2 silah tipi, 1 biyom ve 1 boss üretilecektir. Maksimum oynanış süresi 15 dakikadır.] |

---

### 5. Entegrasyon ve Doğrulama Kuralları

* **[REQ_VD_VAL_01]:** Alt katmandaki tüm dökümanlar (GDD, TDD, ADD) buradaki ID'lere linklenmek zorundadır.
* **[REQ_VD_VAL_02]:** Kalite güvence (QA) test senaryoları, doğrudan bu matristeki sınırları doğrulamak üzere kurgulanacaktır.