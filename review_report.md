# Proje 3 (NoSQL → SQL Dönüşüm Motoru) - Rapor ve Kod İnceleme Raporu

Bu rapor, teslim ettiğiniz **240201092-230201086.pdf** rapor dosyasını ve proje klasöründeki kaynak kodları, dersin **prolab3_spec.txt** dosyasında belirtilen tüm isterlerine göre değerlendirmek amacıyla hazırlanmıştır.

---

## 📊 İster Karşılaştırma Matrisi (Spec Checklist)

Aşağıdaki tabloda projenizin teknik ve raporlama isterlerine ne derece uyum sağladığı gösterilmiştir:

| İster Kategorisi | İster Tanımı | Kod Durumu | Rapor Durumu | Uyum / Notlar |
| :--- | :--- | :--- | :--- | :--- |
| **Sistem Modülleri** | Dosya Seçimi & Görselleştirme (Tree View) | ✅ Tamam | ✅ Tamam | PyQt5 ile ağaç yapısı başarıyla görselleştirilmiş. |
| **Sistem Modülleri** | Veri Tipi Tespiti (Otonom) | ✅ Tamam | ✅ Tamam | `TypeDetector` sınıfı veri tiplerini otomatik analiz ediyor. |
| **Sistem Modülleri** | Düzleştirme (Flattening) | ✅ Tamam | ✅ Tamam | İç içe objeler `ebeveyn_cocuk` formatında düzleştiriliyor. |
| **Normalizasyon** | 1NF (Çoklu Değerlerin Ayrılması / Array) | ✅ Tamam | ✅ Tamam | Diziler (list) tespit edilerek alt tablolara (1:N) aktarılıyor. |
| **Normalizasyon** | 2NF (Primary Key & Foreign Key İlişkileri) | ✅ Tamam | ✅ Tamam | Her tabloya dinamik PK atanıyor, alt tablolar FK ile bağlanıyor. |
| **Normalizasyon** | 3NF (Geçişli Bağımlılıkların Giderilmesi) | ⚠️ **Eksik/Uyumsuz** | ⚠️ **Uyumsuz** | Kodda iç içe nesneler düzleştiriliyor, ayrı tablolara bölünmüyor. |
| **SQL Modülü** | CREATE & INSERT Sorgularının Dinamik Üretimi | ✅ Tamam | ✅ Tamam | `QueryGenerator` otonom sorgu üretiyor. Tablolar topolojik sıralanıyor. |
| **Arayüz Modülü** | SQL Tablo Gösterimi (DataGrid) | ✅ Tamam | ✅ Tamam | SQLite tabloları arayüzde dinamik olarak gösteriliyor. |
| **Arayüz Modülü** | Sıfırlama Butonu (DROP TABLE) | ✅ Tamam | ✅ Tamam | `🗑️ DB Sıfırla` butonu tüm tabloları DROP ediyor. |
| **Rapor Formatı** | IEEE Formatında 4 Sayfa | N/A | ✅ Tamam | Rapor tam olarak 4 sayfadır ve IEEE formatındadır. |
| **Rapor İçeriği** | Özet, Giriş, Yöntem, Sonuç, Kaynakça | N/A | ✅ Tamam | Yapısal şablon tamdır. |
| **Rapor İçeriği** | Akış Diyagramı veya Yalancı Kod | N/A | ✅ Tamam | Yalancı kod (Listing 1) raporda mevcuttur. |
| **Rapor İçeriği** | Class (Sınıf) ve Use Case (Kullanım Senaryosu) Diyagramları | N/A | ❌ **Eksik** | **Raporda class ve use case diyagramları bulunmamaktadır.** |

---

## 🚨 Kritik Bulgular ve Tespit Edilen Eksiklikler

### 1. Eksik Diyagramlar (Rapor İçin En Kritik Eksiklik)
* **Problem**: Proje isterlerinde (*prolab3_spec.txt Line 146-147*) açıkça şu belirtilmektedir:  
  `"Raporda oluşturulan veritabanına ait class diyagramları ve use case diyagramları bulunmalıdır."`
  Teslim ettiğiniz raporda (PDF dosyasında) sadece 3 adet GUI ekran görüntüsü (Şekil 1, 2 ve 3) bulunmakta, **sınıf (class) ve kullanım senaryosu (use case) diyagramları yer almamaktadır.** Bu durum rapordan ciddi puan kırılmasına yol açacaktır.
* **Çözüm**: Aşağıda projeniz için özel olarak hazırladığım **Use Case** ve **Class** diyagram kodlarını (Mermaid formatında) kullanarak bunları çizdirip raporunuza eklemelisiniz.

### 2. 3NF Normalizasyon İsteri ve Kod Arasındaki Uyumsuzluk
* **Problem**: İster belgesinde 3NF şu şekilde tanımlanmıştır:  
  `"Sistem, 5-6 katman derinliğe sahip verileri analiz ederken geçişli bağımlılıkları (transitive dependency) tespit eder. Örneğin; 'Şehir -> İlçe -> Mahalle' gibi iç içe geçmiş nesne grupları, hiyerarşik Foreign Key yapılarıyla birbirine bağlı ayrı tablolara bölünerek veri tekrarı önlenir."`
* **Kodun Durumu**: Yazdığınız kodda `ObjectFlattener` sınıfı iç içe geçmiş nesneleri (JSON dict) **tamamen düzleştirmektedir (flattening)**.  
  Örneğin, `multi_level.json` içindeki `"adres": {"sehir": "Kocaeli", "ilce": "İzmit", "mahalle": {"ad": "Umuttepe"}}` verisi için ayrı `adres` veya `mahalle` tabloları açılmak yerine, bu alanlar `root` tablosuna `adres_sehir`, `adres_ilce`, `adres_mahalle_ad` sütunları olarak eklenmektedir. Bu durum 3NF isterinin tam olarak kodda uygulanmadığını gösterir.
* **Tavsiye**: Eğer jürinin veya hocanın bu konudaki kontrolü çok katıysa, nesneleri (dict) düzleştirmek yerine aynı diziler (list) gibi yeni alt tablolara bölerek 1:1 veya 1:N ilişkisiyle bağlayan bir mantık eklenmesi gerekir. (Aşağıda bunun nasıl çözüleceğine dair kod önerisi verilmiştir.)

### 3. Bölüm III (Ekran Görüntüleri ve Analiz) Metin Eksikliği
* **Problem**: PDF metin analizinde 3. sayfadaki ekran görüntülerinin başlıkları listelenmiş fakat görsellerin altında sistemi analiz eden veya açıklayan herhangi bir metin/paragraf bulunmamaktadır. Görsellerin ne ifade ettiğini açıklayan 1-2 paragraf eklemek rapor kalitesini artıracaktır.

---

## 🛠️ Çözümler ve Destekleyici Materyaller

### A. Raporunuza Eklemeniz Gereken Diyagramlar

#### 1. Use Case (Kullanım Senaryosu) Diyagramı
Bu diyagram, kullanıcının sistemle olan etkileşimini gösterir. Raporunuza çizim olarak ekleyebilirsiniz:

```mermaid
usecaseDiagram
    actor Kullanıcı
    
    Kullanıcı --> (JSON Dosyası Yükleme)
    Kullanıcı --> (Hiyerarşik Ağaç Görünümünü İnceleme)
    Kullanıcı --> (NoSQL'den SQL'e Dönüştürme Başlatma)
    Kullanıcı --> (SQL Tablolarını ve Verilerini Görüntüleme)
    Kullanıcı --> (Veritabanını Sıfırlama)
    
    (NoSQL'den SQL'e Dönüştürme Başlatma) ..> (Dinamik Şema Çıkarımı) : <<include>>
    (NoSQL'den SQL'e Dönüştürme Başlatma) ..> (Dinamik SQL Sorgu Üretimi) : <<include>>
    (NoSQL'den SQL'e Dönüştürme Başlatma) ..> (SQLite Veri Aktarımı) : <<include>>
```

#### 2. Class (Sınıf) Diyagramı
Projenizin modüler nesne yönelimli yapısını gösteren detaylı sınıf diyagramı:

```mermaid
classDiagram
    class MainWindow {
        -JsonFileReader reader
        -JsonAnalyzer analyzer
        -SchemaBuilder schema_builder
        -QueryGenerator query_gen
        -DatabaseEngine db_engine
        -TreeViewWidget tree_widget
        -DataGridWidget data_grid
        -_on_load_json()
        -_on_convert()
        -_on_drop()
    }
    
    class JsonFileReader {
        -dict data
        -dict metadata
        +load_file(path) dict
        +get_file_info() dict
    }
    
    class JsonAnalyzer {
        -TypeDetector type_detector
        -ObjectFlattener flattener
        -ArrayHandler array_handler
        -dict schemas
        +analyze(data) list
        -_process_single_record()
        -_process_array()
    }
    
    class ObjectFlattener {
        -str separator
        +flatten(dict) tuple
        -_recursive_flatten()
    }
    
    class ArrayHandler {
        -TypeDetector type_detector
        +should_create_child_table() bool
        +classify_array() str
        +extract_primitive_records() list
        +extract_object_records() list
    }
    
    class TypeDetector {
        -dict TYPE_MAP
        -dict TYPE_PRIORITY
        +detect_type(val) str
        +map_to_sql_type(val) str
        +merge_types(t1, t2) str
    }
    
    class SchemaBuilder {
        -dict schemas
        +build(list) list
        -_process_schema()
        -_topological_sort()
    }
    
    class DatabaseEngine {
        -str db_path
        -connection
        +connect(path)
        +execute(sql, params)
        +create_tables(schemas)
        +insert_data(schemas)
        +drop_all_tables()
    }
    
    class QueryGenerator {
        +generate_create_table(schema) str
        +generate_insert(schema, record, idx) tuple
        +generate_drop_table(name) str
    }
    
    MainWindow --> JsonFileReader
    MainWindow --> JsonAnalyzer
    MainWindow --> SchemaBuilder
    MainWindow --> DatabaseEngine
    MainWindow --> QueryGenerator
    JsonAnalyzer --> TypeDetector
    JsonAnalyzer --> ObjectFlattener
    JsonAnalyzer --> ArrayHandler
```

---

### B. Kodda 3NF İlişkisel Yapı Eksikliğini Düzeltme Önerisi

Eğer `Şehir -> İlçe -> Mahalle` yapısının tamamen ayrı tablolara bölünmesini ve Foreign Key ile bağlanmasını kod üzerinde sağlamak isterseniz, `ObjectFlattener` ve `JsonAnalyzer` sınıflarında ufak bir mimari değişiklik yapılması gerekir.

Şu anki düzleştirici (flattening) yerine, iç içe objeleri (dict) de yeni birer ilişkili tablo (1:1 ilişkisi) olarak ele alan alternatif bir yaklaşım şu şekilde kodlanabilir:

```python
# modules/object_flattener.py (Eski yaklaşımda dict'ler düzleştiriliyordu)
# Yeni Yaklaşım: Dict'leri düzleştirmek yerine nested_objects listesine ekleyerek
# JsonAnalyzer'ın bunlardan da ayrı tablolar üretmesini sağlayabiliriz.
```

Ancak eğer bu yapılandırma mevcut test senaryolarınızı bozacaksa veya süreniz kısıtlıysa, rapordaki **3NF** tanımını kodunuza uyduracak şekilde yumuşatabilir ya da bu haliyle jüriye sunabilirsiniz. Ancak raporda **diyagram eksikliklerini kesinlikle tamamlamanız gerekmektedir.**

---

> [!IMPORTANT]
> **Özetle Yapılması Gerekenler:**
> 1. Raporunuza yukarıdaki **Sınıf Diyagramı (Class Diagram)** ve **Kullanım Senaryosu Diyagramı (Use Case Diagram)** çizimlerini ekleyin.
> 2. Raporun 3. sayfasında boş kalan **Ekran Görüntüleri ve Analiz** bölümünün altına görselleri açıklayan kısa metinler ekleyin.
> 3. Kodunuzun 3NF kısmında nested nesneleri düzleştirdiğini, dizileri ise alt tablolara bölerek 1:N ilişkisi kurduğunu bilin ve savunmanızı buna göre hazırlayın.
