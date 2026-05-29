# L1-C: ART DESIGN DOCUMENT (ADD) OLUŞTURMA VE YAZIM KILAVUZU

**Proje Kodu:** ALM_ADD_STANDARDS  
**Versiyon:** v1.0:0  
**Doküman Sahibi:** Art & Audio Director / Tech Artist  
**Sistem Durumu:** KİLİTLİ / ZORUNLU UYGULAMA  

---

## 1. ADD Nedir? (Görsel Mimari ve Performans Kısıtları Tanımı)

**Art Design Document (ADD)**; oyunun sanatsal stilini, renk teorisini, ışıklandırma paletini ve arayüz estetiğini belirlerken; aynı zamanda 3D model, kaplama (texture), animasyon ve efektlerin (VFX) oyun motoruna aktarılma standartlarını ve performans bütçelerini tanımlayan **L1-C seviyesi görsel mimari dokümanıdır**.

Otomotiv endüstrisindeki **"Styling & Surface Specification"** standartlarının oyun sektöründeki tam karşılığıdır. ADD, sadece "Oyun güzel görünsün" diye yazılmaz; "Sanatsal varlıklar (assets), TDD'nin koyduğu RAM/VRAM ve GPU bütçelerini ihlal etmeden **en optimize şekilde nasıl üretilir?**" sorusuna yanıt verir.

---

## 2. ADD Yazım Kanunları ve Optimizasyon Prensipleri

ADD yazılırken aşağıdaki teknik-sanatsal (Tech-Art) kurallara uyulması zorunludur. Bu kuralları karşılamayan hiçbir görsel varlık projeye dahil edilemez.

* **Katı İsimlendirme Standartları (Naming Conventions):** Projedeki tüm varlıklar motorun anlayacağı ve ALM sisteminin indeksleyebileceği şekilde isimlendirilmelidir. (Örn: Ana karakter dokusu: `T_Hero_Base_D`, Statik Çevre Modeli: `SM_Factory_Wall_01`).
* **Metrik Tabanlı Poligon ve Doku Sınırları:** "Düşman modeli düşük poligonlu olacak" gibi ucu açık ifadeler yasaktır. Hedef donanıma göre net poligon (Tris) ve doku çözünürlüğü ($1024\times1024$, $512\times512$) sınırları matris halinde verilmelidir.
* **Shader ve Materyal Kompleksite Kontrolü:** Materyallerdeki instruction count (kod karmaşıklığı) ve dinamik ışık alan vertex sayıları sınırlandırılmalıdır. Mobil veya el konsolu hedeflerinde (Steam Deck) aşırı şeffaflık (Overdraw) yaratacak duman/efekt (VFX) tasarımlarından kaçınılmalıdır.

---

## 3. İzlenebilirlik ve Bağlantı Kuralları (Traceability)

ADD, hiyerarşide L0 (Vision Document) ve L1-B (TDD) ile L2 (Product Backlog) arasında doğrudan bir köprüdür.

* **Dikey Bağlantı (Vertical Traceability):** ADD'de tanımlanan her bütçe ve stil kararı, L0 vizyon dökümanındaki sanatsal kısıtlara (`REQ_VD_ART_XX`) ve teknik kısıtlara (`REQ_VD_TEC_XX`) çarpmak zorundadır.
  * *Örnek:* `[REQ_ADD_MOD_01] -> Sınırlar: [REQ_VD_ART_02] (Karakter poligon bütçesi)`
* **Yatay Bağlantı (Horizontal Traceability):** Sanatçıların üreteceği varlıkların teknik sınıfları ve import kuralları, TDD'deki veri ve bellek optimizasyon planlarıyla (`REQ_TDD_XXX`) senkronize olmalıdır.
* **ADD ID Standartı:** ADD içindeki her sanatsal gereksinim `REQ_ADD_[MODÜL]_[NUMARA]` formatında kodlanmalıdır.
  * `REQ_ADD_STY_01`: Stil ve Renk Paleti Modülü, 1. Gereksinim.
  * `REQ_ADD_TEX_03`: Kaplama ve Dokulandırma Modülü, 3. Teknik Gereksinim.

---

## 4. L1-C: Standart ADD Şablonu (Boş Matris)

*Yeni bir görsel biyom, karakter grubu veya efekt seti tasarlanırken kopyalanıp doldurulacak resmi şablondur:*

```markdown
# ADD: [GÖRSEL MODÜL / VARLIK GRUBU ADI] (Örn: Fabrika Biyomu Çevre Modelleri)

**Modül Kodu:** REQ_ADD_[MODÜL_KODU]  
**Bağlı Olduğu L0 Kısıtı:** [REQ_VD_ART_XX] & [REQ_VD_TEC_XX]  
**Versiyon:** v0.1:0  
**Teknik Sanatçı / Tasarımcı:** [Adınız / Rolünüz]  

---

### 1. Görsel Konsept ve Renk Teorisi
[Bu modülün oyunun genel atmosferindeki yeri nedir? Hangi duyguyu geçirmeyi hedefliyor? Kullanılacak ana renk paleti (Hex kodları ile) ve ışıklandırma referansları.]

---

### 2. Varlık İsimlendirme ve Klasör Standartları (Naming Conventions)

*Bu modülde üretilecek assetlerin Unreal Engine içindeki isimlendirme kuralları:*

* **Static Mesh (Statik Model):** `SM_[BiyomName]_[AssetDescription]_[Num]` -> Örn: `SM_Factory_Pipe_01`
* **Skeletal Mesh (Animasyonlu Model):** `SK_[CharacterName]` -> Örn: `SK_Boss_Mecha`
* **Textures (Dokular):**
  * Base Color / Diffuse: `T_[AssetDescription]_D`
  * Normal Map: `T_[AssetDescription]_N`
  * Mask (Red: Ambient Occlusion, Green: Roughness, Blue: Metallic): `T_[AssetDescription]_ORM`

---

### 3. Sanatsal ve Teknik Performans Matrisi (Asset Budgets)

| Gereksinim ID | Varlık Tipi | Maksimum Poligon (Tris) / Çözünürlük Sınırı | LOD (Level of Detail) Standartları |
| :--- | :--- | :--- | :--- |
| **[REQ_ADD_MOD_01]** | Ana Karakter | Maksimum 15.000 Tris (LOD 0) | LOD 1 (%50 azaltma), LOD 2 (%75 azaltma) zorunludur. |
| **[REQ_ADD_TEX_01]** | Çevre Kaplamaları | Maksimum $1024\times1024$ piksel çözünürlük. | Tüm dokularda Mip-Mapping açık olmak zorundadır. |
| **[REQ_ADD_VFX_01]** | Patlama Efektleri | Eşzamanlı maksimum particle sayısı: 150. | Overdraw engellemek için alpha haritaları optimize edilecektir. |

---

### 4. Teknik Sanat ve Materyal Kuralları (Tech-Art Rules)
*Modellerin motor içindeki shader ve materyal kurguları:*

* **Master Material Kullanımı:** Her model için ayrı materyal (Material) oluşturulamaz. Teknik ekibin hazırladığı tek bir `MM_Prop_Master` veya `MM_Character_Master` temel alınarak **Material Instance** türetilecektir.
* **Movable Işık Kısıtı:** Çevre modellerinin üzerinde dinamik/hareketli ışık (Movable Light) üreten kaçak bileşenler bulunamaz. Tüm çevre ışıkları önceden hesaplanacaktır (Baked/Static Lighting) veya Unreal Engine Lumen kısıtlarına tam uyumlu olacaktır.