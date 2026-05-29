# L3: CODE & ASSET EXECUTION (ÜRETİM VE YÜRÜTME SÜRÜM KILAVUZU)

**Proje Kodu:** ALM_L3_EXECUTION_STANDARDS  
**Versiyon:** v1.0:0  
**Doküman Sahibi:** Technical Director / Lead Programmer  
**Sistem Durumu:** KİLİTLİ / ZORUNLU UYGULAMA  

---

## 1. L3 Katmanının Tanımı ve Amacı

**L3: Code & Asset Execution**; bir üst katmanda (L2) Kabul Kriterleri (Acceptance Criteria) belirlenmiş olan PBI'ların (Product Backlog Items), geliştiriciler veya yapay zeka ajanları tarafından fiziksel olarak koda (C++/Blueprint) veya optimize edilmiş görsel varlıklara (Static/Skeletal Mesh, Texture, VFX, Audio) dönüştürüldüğü **aktif üretim katmanıdır**.

Otomotiv yazılım süreçlerindeki **"Software Component Implementation"** veya standart yazılım mühendisliğindeki **"Coding & SCM (Source Code Management)"** aşamasının tam karşılığıdır. L3 katmanının ana amacı; kodun ve sanatsal varlıkların kaotik bir şekilde değil, sürüm kontrol kurallarına ve mimari bütçelere (TDD/ADD) %100 uyumlu olarak motor ana dizinine (`develop` branch) aktarılmasını sağlamaktır.

---

## 2. Git ve Branch (Dal) Yönetimi Kuralları

L3 katmanında üretilen her kod satırı veya asset, izole bir ortamda geliştirilmek zorundadır. Ana dallara doğrudan müdahale kesinlikle yasaktır.

### Dal Hiyerarşisi (Branch Strategy)
* **`master` / `main`:** Sadece canlıya/Milestone'a çıkmaya hazır, L4 (QA) testlerinden %100 başarıyla geçmiş kararlı sürümleri barındırır.
* **`develop`:** Aktif entegrasyon dalıdır. Geliştiricilerin tamamladığı işler buraya merge edilir.
* **`feature/PBI_[ID]-[Kisa_Tanim]`:** Sadece ilgili PBI kodu için açılan, ömrü o iş bittiğinde sona eren geçici üretim dallarıdır.

[master]     ───────────────────────────────────► [Milestone Sürümü]
▲
[develop]    ────┼─────────┬───────────────┬────► [Entegrasyon ve Test]
│         ▲               ▲
[feature]        └─ PBI_042┘       └─ PBI_043┘    [İzole Üretim Dalları]

### Commit Mesajı ve Versiyon Numaralandırma (Versioning)
L3 katmanındaki her commit, **vX.Y:Z** formatında prefix içermek zorundadır.
* **vX.Y** (`develop` seviyesi): Genel sprint başarısını gösterir.
* **vX.Y:Z** (`feature` seviyesi): O işe özel atomik adımdır.
**v[Ana_Sürüm].[Minor_Sürüm]:[Task_No] - [PBI_ID] - [Değişiklik Özeti ve Referans ID]**

**Örnek:** `v0.3:15 - Added character double jump mechanics physics override [PBI-042]`

---

### Özellik Dalı Açma Komut Protokolü
Geliştirici (veya kod ajanı) işe başlarken terminalde şu komut zincirini çalıştırmak zorundadır:
```bash
# 1. Yerel develop dalını güncelle
git checkout develop
git pull origin develop

# 2. İlgili PBI ID'sine bağlı yeni izole dalı aç
git checkout -b feature/PBI_042-character-double-jump

## 3. Kodlama Kuralları (Programming Standards)

### Blueprint ve C++ Senkronizasyonu
Yazılan her mantık, TDD'ye uygun olarak ya C++ class'ı olarak tasarlanmalı ya da en azından C++ temel sınıfından türetilmelidir.
* **Blueprints:** Sadece görsel bağlama (Visual Wiring) için kullanılır. İş mantığı (Logic)Blueprint içinde yazılmaz.
* **İsimlendirme:** `BP_` prefix'i ile C++ sınıfının isimlendirmesi (`APawn`, `AActor`) ile tutarlı olmalıdır.

### Performans Kriterleri
* `GetAllActorsOfClass()` fonksiyonu **yasaktır**. Yerine Component Tags veya Component Interfaces kullanılmalıdır.
* `Construction Script` içinde ağır hesaplama (Heavy Calculation) yapılmamalıdır. Sadece referans atamaları yapılmalıdır.

---

## 4. Asset Üretim Kuralları (Art & Audio Production)

### 3D Model (Static/Skeletal Mesh) Kuralları
* **LOD (Level of Detail) Zorunluluğu:** Hiçbir model LOD 0 seviyesinde bırakılamaz. En az 3 seviyeli LOD (LOD0, LOD1, LOD2) motor içine import edilmek zorundadır.
* **Triangle Budget:** Modelin polygon sayısı, TDD/ADD'de belirlenen bütçeyi aşamaz.
* **Vertex Normal ve Tangent Uzay:** Normallerin "soft" veya "hard" olarak doğru export edildiğinden emin olunmalıdır.

### Texture & Material Kuralları
* **Normal Map Space:** Unreal Engine için her zaman "OpenGL" (G - Yeşil Kanal ters çevrilmiş) formatında export edilmelidir.
* **PBR Pipeline:** Metallic-Roughness iş akışı zorunludur. ORM maskesi (Occlusion, Roughness, Metallic) tek dokuda birleştirilerek VRAM tasarrufu sağlanmalıdır.

### Animasyon Kuralları
* Animasyonlar, oyun motorunun `retargeting` sistemine uygun olmalıdır.
* `Locomotion` animasyonları (yürüme, koşma) blend-space'e (BS_Hero_Locomotion) entegre edilmek zorundadır.

---

## 5. QA ve Test Protokolü (L3'e Özel)
* **L3 Commit Review:** Feature branch'ten `develop`'a merge talebi açıldığında, QA Lead/Agent, PBI'daki **Acceptance Criteria**'ya göre kod incelemesi yapar.
* **Sanity Check:** AI geliştiricisi (veya insan), kodun `develop`'a aktarılmadan önce motor içinde çökmediğini (Crash) ve compile error vermediğini doğrular.