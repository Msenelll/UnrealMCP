# Oyun Geliştirme Dokümantasyon ve Süreç Çerçevesi (Framework)

Bu doküman, projenin vizyon aşamasından kod satırına kadar olan tüm süreçlerini, rollerini, dokümantasyon hiyerarşisini ve sürüm kontrol protokollerini tanımlayan ana kılavuzdur. Proje boyunca bu çerçeveye tavizsiz uyulacaktır.

---

## 1. Indie MVP Ekip Rolleri ve Kapasite Dağılımı

Proje geliştirme sürecinde (Solo-Dev mimarisinde yapay zeka ajanları delege edilirken veya ekip genişletilirken) kullanılacak temel şapkalar/roller aşağıdadir:

* **Game Director / Product Owner (Oyun Yönetmeni):** Vizyonun korunması, GDD'nin yazımı, mekaniklerin kararlaştırılması ve ürünün rotasından sorumludur. ("Oyun ne yapacak? Hedef kitle kim?" sorularına odaklanır).
* **Technical Director / Lead Architect (Teknik Direktör):** TDD'nin yazımı, sistem mimarisi, class hiyerarşisi, performans ve bellek bütçelerinden sorumludur. ("Unreal Engine'de en optimize nasıl çalışır?" sorusuna odaklanır).
* **Art & Audio Director (Sanat ve Ses Yönetmeni):** ADD'nin yazımı, görsel bütünlük, poligon limitleri, animasyon ağaçları, UI/UX tasarımı ve işitsel atmosferden sorumludur. ("Ürün nasıl hissettirecek ve görünecek?" sorusuna odaklanır).
* **Producer / QA Lead (Yapımcı ve Test Lideri):** Product Backlog (PBI) yönetimi, Sprint planlaması, Definition of Done (DoD) kontrolleri ve test senaryolarının işletilmesinden sorumludur. ("Proje takvime uyuyor mu? Sistem hatasız çalışıyor mu?" sorularına odaklanır).

---

## 2. Dokümantasyon Mimarisi ve İzlenebilirlik (Traceability) Matrisi



| Seviye | Doküman / Obje | Amacı (Neden Var?) | İçermesi Gereken Alt Başlıklar / Format | Sorumlu Rol |
| :--- | :--- | :--- | :--- | :--- |
| **L0** | **Vision Document (VD)** | Projenin anayasasıdır. Kapsamı (Scope) kilitler, kısıtları belirler. Değişmesi en zor dokümandır. | - Elevator Pitch<br>- Core Gameplay Loop<br>- Hedef Platform (PC/Konsol)<br>- Teknik Kısıtlar (Örn: Max Draw Call, FPS hedefi)<br>- Hedef Kitle (Persona) | Game Director |
| **L1** | **Game Design Doc. (GDD)** | L0'daki vizyonu kurallara döker. Sistemin nasıl oynanacağını anlatır, yazılımdan bağımsızdır. | - Mekanik Kuralları (State Machine geçişleri)<br>- Karakter ve Kontrol şemaları<br>- Ekonomi ve İlerleme (Progression)<br>- Level Design yönergeleri | Game Director |
| **L1** | **Technical Design Doc. (TDD)** | GDD'deki kuralların Unreal C++/Blueprint mimarisini, veri tiplerini ve algoritmalarını kurar. | - Class Hiyerarşisi (`APawn`, `AActor`)<br>- Veri Yapıları (Struct, Enum, Database mantığı)<br>- Sistem Mimarisi (GameMode, GameState yönetimi)<br>- Optimizasyon ve Bellek Bütçeleri | Technical Director |
| **L1** | **Art Design Doc. (ADD)** | Oyunun görsel sınırlarını ve varlık (Asset) üretim standartlarını belirler. | - Renk Paletleri ve Işıklandırma Kılavuzu<br>- Poligon (LOD) ve Texture Çözünürlük Bütçeleri<br>- Dosya İsimlendirme Standartları (Naming Conventions) | Art Director |
| **L2** | **Product Backlog Item (PBI / Epic)** | GDD ve TDD'de yazanları teslim edilebilir iş paketlerine dönüştürür. "Nasıl" yapılacağını söylemez, "Ne" teslim edileceğini söyler. | - **User Story:** "Kullanıcı olarak şunu yapabilmeliyim..."<br>- **Acceptance Criteria (AC):** O işe özel test onay şartları.<br>- **Definition of Done (DoD):** Tüm projede geçerli kalite standartları.<br>- İlgili GDD/TDD Linki (Traceability) | Producer |
| **L3** | **Sprint Task / Sub-task** | PBI'ı tamamlamak için atılması gereken teknik ve atomik adımlardır. Kod yazılan, Blueprint bağlanan yer burasıdır. | - Yapılacak teknik işlem (Örn: "Raycast fonksiyonunu yaz").<br>- Çıktı lokasyonu (Hangi klasör/branch?).<br>- Gerekli referans döküman veya kod parçası. | Developer / LLM Agent |

---

[ L0: VISION DOCUMENT ] (Proje Anayasası & Kısıtlar)
  │
  ├──► [ L1-A: GAME DESIGN ] ─── (İşlevsel Kurallar)
  │         ▲
  │         ▼ (Çift Yönlü Entegrasyon)
  ├──► [ L1-B: TECH DESIGN ] ─── (Yazılım Mimarisi)
  │         ▲
  │         ▼ (Performans Bütçeleri)
  └──► [ L1-C: ART DESIGN  ] ─── (Görsel Sınırlar)
            │
            ▼ (Gereksinimlerin Birleşimi)
[ L2: PRODUCT BACKLOG (PBI) ] ── (Kabul Kriterleri & DoD)
  │
  ├──► [ L3: TASK DESCRIPTION & CODE & ASSET EXECUTION ] ── (Geliştirme/Branch)
  │         ▲
  │         ▼ (Test / Sürekli Doğrulama)
  └──► [ L4: QA & TEST PLAN ] ────────── (Çift Yönlü Traceback)

## 3. Sürüm Kontrol, Dal (Branch) Yönetimi ve Süreç Protokolü

Projedeki her kod satırı ve varlık (asset) yönetimi aşağıdaki Git kurallarına göre işletilmek zorundadır:

### Branch Kuralları
1. Projedeki her aksiyon/task için yeni bir **Feature Branch** oluşturulacaktır.
2. Yapılacak lokal ve otomasyon testleri sonrasında, bu branch'ler herhangi bir onaya gerek duyulmadan doğrudan `develop` branch'i ile merge edilecektir.
3. `master` branch'ine **kesinlikle** onay alınmadan (Ludus Magnus onayı olmadan) merge yapılmayacaktır.
4. Canlıda/Yayında olacak veya stabil sürümü temsil edecek sayfa/ürün her zaman `master` branch'i olmalıdır.
5. Geliştirme faaliyetleri aktif olarak ilgili feature branch'lerinde yönetilip `develop` üzerinde birleştirilecektir.

### Commit Mesajı ve Versiyon Numaralandırma Standardı
Her commit mesajının başına sürüm durumunu belirten `vA.B:C` formatında bir numaralandırma eklenecektir:
* **A:** Master branch seviyesi (Major sürümler/Milestones)
* **B:** Develop branch seviyesi (Sprint çıktıları/Minor sürümler)
* **C:** Feature branch seviyesi (Atomik task commits)

*Örnek commit mesajı:* `v0.1:12 - Added character double jump mechanics physics override`