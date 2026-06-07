<div align="center">
  <h1>🗄️ JSON to SQL Database Converter</h1>
  <p><strong>Karmaşık JSON Dosyalarını İlişkisel (Relational) SQL Tablolarına Dönüştüren Otonom Araç</strong></p>
  
  [![Python Version](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
  [![PyQt5](https://img.shields.io/badge/GUI-PyQt5-orange.svg)]()
  [![Database](https://img.shields.io/badge/Database-SQLite-003B57.svg)]()
</div>

<br>

## 📖 Proje Hakkında
Bu proje, şemasız (schema-less), derinlemesine iç içe geçmiş (nested) ve karmaşık veri tipleri barındıran JSON dosyalarını analiz ederek tamamen otomatik bir şekilde SQL (SQLite) tablolarına çeviren gelişmiş bir araçtır. PyQt5 ile tasarlanmış kullanıcı dostu bir arayüze sahiptir.

## ✨ Özellikler
- 🔄 **Dinamik Veri Çözümleme (Parsing):** Herhangi bir hardcoded (sabit) şemaya ihtiyaç duymadan JSON'ı tarar ve özyineli (recursive) bir fonksiyonla ağaç yapısını çıkarır.
- 📐 **İlişkisel Veri Tabanı Normalizasyonu:** İç içe diziler (arrays) ve nesneler (objects) tespit edildiğinde, ana (Parent) - alt (Child) tabloları `Foreign Key` mantığı ile otomatik olarak oluşturarak 3NF'ye uygun veri tabanı modelleri çıkarır.
- 🖥️ **Gelişmiş GUI (Arayüz):** Verilerin ağaç (Tree) yapısını ve üretilen SQL tablolarını anlık olarak inceleyebileceğiniz PyQt5 tabanlı masaüstü arayüzü.

## 🚀 Kurulum & Kullanım

1. **Repoyu İndirin:**
   ```bash
   git clone https://github.com/talha4111/prolab3.git
   cd prolab3
   ```

2. **Gereksinimleri Yükleyin:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Uygulamayı Çalıştırın:**
   ```bash
   python main.py
   ```

## 🧩 Mimari Yapı
Uygulama temel olarak şu modüllerden oluşur:
- `modules/json_parser.py`: JSON verisini okuyan ve düğümleri ayıran katman.
- `modules/sql_generator.py`: Çözümlenen verilerden otomatik olarak `CREATE TABLE` ve `INSERT INTO` sorguları oluşturan çekirdek motor.
- `gui/main_window.py`: Sinyal/Slot mantığı ile çalışan grafiksel arayüz.

## 👨‍💻 Geliştirici
**Talha Gürler** - [@talha4111](https://github.com/talha4111)
