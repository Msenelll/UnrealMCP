# L1-B: TECHNICAL DESIGN DOCUMENT (TDD) OLUŞTURMA VE YAZIM KILAVUZU

**Proje Kodu:** ALM_TDD_STANDARDS  
**Versiyon:** v1.0:0  
**Doküman Sahibi:** Technical Director / Lead Architect  
**Sistem Durumu:** KİLİTLİ / ZORUNLU UYGULAMA  

---

## 1. TDD Nedir? (Yazılım ve Mimari Tasarım Tanımı)

**Technical Design Document (TDD)**; GDD'de tanımlanan fonksiyonel oyun kurallarının oyun motoru (Unreal Engine 5) üzerindeki yazılım mimarisini, veri yapılarını, bellek yönetimini ve algoritma akışlarını belirleyen **L1-B seviyesi sistem mimarisi dokümanıdır**.

Otomotiv yazılım mühendisliğindeki **"Software Architecture Design" (Yazılım Mimari Tasarımı)** belgesinin oyun sektöründeki tam karşılığıdır. TDD, "Oyun nasıl oynanır?" sorusuyla ilgilenmez; "Bu oyun mekaniği, hedef donanımın CPU/GPU ve RAM bütçesini aşmadan, en yüksek kod kalitesiyle **yazılımsal olarak nasıl var edilir?**" sorusuna yanıt verir.

---

## 2. TDD Yazım Kanunları ve Mühendislik Prensipleri

TDD yazılırken aşağıdaki teknik kurallara uyulması zorunludur. TDD onayı almamış hiçbir kod mimarisi için feature branch açılamaz.

* **Sürdürülebilir Nesne Yönelimli Mimari (OOP):** Sınıf hiyerarşileri (Inheritance), kompozisyon prensipleri (Actor Components) ve arayüzler (Interfaces) açıkça belirtilmelidir. Kodda spagetti bağımlılıkları (Tight Coupling) engelleyecek modüler yapılar kurgulanmalıdır.
* **Performans ve Zaman Bütçesi Kontrolü:** Ağır işlemlerin (Örn: `Tick` fonksiyonu kullanan döngüler, karmaşık yapay zeka algoritmaları, her karede çağrılan Raycast/Line Trace işlemleri) frame-time ($16.6\text{ ms}$) üzerindeki maliyeti hesaplanmalı ve optimizasyon stratejisi dokümante edilmelidir.
* **Veri Güvenliği ve Serialization:** Oyun verilerinin (Karakter istatistikleri, envanter, save-load dosyaları) hangi veri tipinde (`USTRUCT`, `UCLASS`, `TMap`) tutulacağı ve belleğe nasıl yazılacağı önceden tanımlanmalıdır.

---

## 3. İzlenebilirlik ve Bağlantı Kuralları (Traceability)

TDD, hiyerarşide L0 (Vision Document) ve L1-A (GDD) ile L2 (Product Backlog) arasında çift yönlü bir köprüdür.

* **Yatay Bağlantı (Horizontal Traceability):** Her TDD maddesi, gerçekleştirmekle yükümlü olduğu GDD gereksinim ID'sine doğrudan bağlı olmak zorundadır.
  * *Örnek:* `[REQ_TDD_ARC_01] -> Gerçekleştirir: [REQ_GDD_CMB_01]`
* **Dikey Bağlantı (Vertical Traceability):** Mimarideki bellek ve performans kararları, L0 vizyon dökümanındaki teknik kısıtlara (`REQ_VD_TEC_XX`) çarpmak zorundadır.
* **TDD ID Standartı:** TDD içindeki her teknik gereksinim `REQ_TDD_[MODÜL]_[NUMARA]` formatında kodlanmalıdır.
  * `REQ_TDD_ARC_01`: Mimari ve Altyapı Modülü, 1. Teknik Gereksinim.
  * `REQ_TDD_AI_05`: Yapay Zeka Modülü, 5. Teknik Gereksinim.

---

## 4. L1-B: Standart TDD Şablonu (Boş Matris)

*Yeni bir teknik alt sistem kurulurken kopyalanıp doldurulacak resmi şablondur:*

```markdown
# TDD: [SİSTEM / MODÜL ADI] (Örn: Karakter Combo Sistemi Altyapısı)

**Modül Kodu:** REQ_TDD_[MODÜL_KODU]  
**İlişkili GDD Maddesi:** [REQ_GDD_XXX_XX]  
**Bağlı Olduğu L0 Kısıtı:** [REQ_VD_TEC_XX]  
**Versiyon:** v0.1:0  
**Yazılım Mimarı:** [Adınız / Rolünüz]  

---

### 1. Teknik Mimari Özet
[Bu sistemin yazılımsal olarak nasıl kurulacağına dair üst düzey özet. Hangi Unreal Engine pattern'leri (Örn: Subsystem, Actor Component) kullanılacak?]

---

### 2. Sınıf Hiyerarşisi ve Kalıtım Haritası (Class Architecture)

*Bu modülde oluşturulacak C++ ve Blueprint sınıflarının ilişkisi:*

* **`AGenesisCharacter`** (`ACharacter` sınıfından türetilecek)
  * *Sorumluluk:* Temel karakter girdilerini almak ve animasyon tetiklemelerini yönetmek.
  * *İçereceği Komponent:* `UCombatComponent` (`UActorComponent` sınıfından türetilecek).
* **`UCombatComponent`**
  * *Sorumluluk:* Combo sayacını, hasar logaritmasını ve combo state yapısını tamamen encapsulation kurallarına uygun olarak kendi içinde yönetmek.

---

### 3. Veri Yapıları ve Tip Tanımlamaları (Data Structures)

*Sistemin kullanacağı struct, enum ve veri konteynerleri:*

```cpp
UENUM(BlueprintType)
enum class EComboState : uint8
{
    ECS_Idle        UMETA(DisplayName = "Idle"),
    ECS_LightAttack UMETA(DisplayName = "Light Attack"),
    ECS_HeavyAttack UMETA(DisplayName = "Heavy Attack"),
    ECS_Resetting   UMETA(DisplayName = "Resetting")
};

USTRUCT(BlueprintType)
struct FComboData
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Combat")
    class UAnimMontage* AttackMontage;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Combat")
    float BaseDamage;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Combat")
    float ComboWindowDuration;
};