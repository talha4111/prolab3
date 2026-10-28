<div align="center">
  <h1>🗄️ Autonomous JSON to 3NF SQLite Database Converter</h1>
  <p><strong>Şemasız (Schema-less) ve İç İçe Geçmiş (Nested) JSON Verilerini Otonom Olarak 3NF İlişkisel SQLite Tablolarına Dönüştüren Python & PyQt5 Masaüstü Platformu</strong></p>
  
  [![Python Version](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
  [![PyQt5](https://img.shields.io/badge/GUI-PyQt5-41CD52?style=for-the-badge&logo=qt&logoColor=white)]()
  [![Database](https://img.shields.io/badge/Database-SQLite_3NF-003B57?style=for-the-badge&logo=sqlite&logoColor=white)]()
</div>

<br>

## 📖 Proje Hakkında
Bu proje, önceden tanımlanmış bir şemaya (schema) ihtiyaç duymadan, karmaşık ve çok katmanlı (deeply nested) JSON dosyalarını özyineli (recursive) algoritmalarla analiz ederek **Üçüncü Normal Form (3NF)** kurallarına uygun ilişkisel **SQLite** veritabanı tablolarına dönüştüren uçtan uca bir veri mühendisliği aracıdır.

---

## ✨ Temel Mühendislik Özellikleri
- 🔍 **Özyineli JSON Çözümleme & Tip Çıkarımı (`json_analyzer.py`, `type_detector.py`):** Sabit şema gerektirmeden tüm JSON ağacını tarar; veri tiplerini (`INTEGER`, `REAL`, `TEXT`, `BOOLEAN`) dinamik olarak tespit eder.
- 🔗 **Otonom İlişkisel Normalizasyon (`object_flattener.py`, `array_handler.py`, `schema_builder.py`):** İç içe nesneleri düzleştirir (flattening) ve alt dizileri (1:N ilişkileri) otomatik olarak `Primary Key` ve `Foreign Key` kısıtlamalarına sahip alt (child) tablolara ayırır.
- ⚙️ **Dinamik DDL/DML Motoru (`query_generator.py`, `database_engine.py`):** Parametreli `CREATE TABLE` ve `INSERT INTO` sorgularını üretir ve işlem bütünlüğü (transaction safety) ile SQLite üzerinde yürütür.
- 🖥️ **Etkileşimli PyQt5 Masaüstü Arayüzü (`gui/`):** JSON hiyerarşisini ağaç görünümünde (`tree_view_widget.py`) ve üretilen ilişkisel SQL tablolarını canlı veri ızgaralarında (`data_grid_widget.py`) görselleştirir.

---

## 🚀 Kurulum ve Kullanım

```bash
git clone https://github.com/talha4111/prolab3.git
cd prolab3
pip install -r requirements.txt
python main.py
```

---

## 📂 Modüler Mimari Yapı
```text
prolab3/
├── main.py                      # Uygulama giriş noktası
├── modules/
│   ├── json_reader.py           # Güvenli dosya okuma ve JSON doğrulama katmanı
│   ├── json_analyzer.py         # Özyineli (recursive) yapı ve düğüm analizcisi
│   ├── object_flattener.py      # 1:1 iç içe nesne düzleştirme motoru
│   ├── array_handler.py         # 1:N dizi ayrıştırma ve alt tablo ilişkilendirici
│   ├── type_detector.py         # Dinamik SQL veri tipi çıkarım modülü
│   ├── schema_models.py         # Tablo, Sütun ve Foreign Key veri modelleri
│   ├── schema_builder.py        # 3NF ilişkisel şema oluşturucu
│   ├── query_generator.py       # SQLite DDL ve DML sorgu üretici
│   └── database_engine.py       # SQLite bağlantı ve transaction yürütme motoru
├── gui/
│   ├── main_window.py           # Ana PyQt5 penceresi ve Sinyal/Slot koordinatörü
│   ├── tree_view_widget.py      # Hiyerarşik JSON ve şema ağaç bileşeni
│   ├── data_grid_widget.py      # İlişkisel SQL tablo görüntüleyici
│   └── styles.py                # Modern karanlık/aydınlık arayüz teması
└── test_data/                   # Basit, iç içe ve çok katmanlı örnek JSON veri setleri
```

---

## 👨‍💻 Geliştirici
**Talha Gürler** — [GitHub (@talha4111)](https://github.com/talha4111)