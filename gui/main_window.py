"""
Ana Pencere (Main Window)
--------------------------
Tüm modülleri birleştiren ve kullanıcı etkileşimini
yöneten ana uygulama penceresi.

Özellikler:
  - JSON dosya yükleme (File Dialog)
  - Tree View görselleştirme
  - Dönüştür butonu (JSON → SQL)
  - SQL tablo görüntüleme (DataGrid)
  - DB Sıfırla butonu (DROP ALL)
  - Durum çubuğu ve log paneli
"""

import os
import sys
import traceback

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QSplitter, QFileDialog,
    QMessageBox, QTextEdit, QApplication, QGroupBox
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon

from modules.json_reader import JsonFileReader
from modules.json_analyzer import JsonAnalyzer
from modules.schema_builder import SchemaBuilder
from modules.query_generator import QueryGenerator
from modules.database_engine import DatabaseEngine

from gui.tree_view_widget import TreeViewWidget
from gui.data_grid_widget import DataGridWidget
from gui.styles import DARK_THEME


class MainWindow(QMainWindow):
    """NoSQL → SQL Dönüşüm Motoru ana penceresi."""

    def __init__(self):
        super().__init__()

        # Modülleri başlat
        self._reader = JsonFileReader()
        self._analyzer = JsonAnalyzer()
        self._schema_builder = SchemaBuilder()
        self._query_gen = QueryGenerator()
        self._db_engine = DatabaseEngine()

        # DB bağlantısını başlat
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "database.db")
        self._db_engine.connect(os.path.abspath(db_path))

        self._setup_ui()
        self._log("✅ Sistem hazır. Bir JSON dosyası yükleyin.")

    def _setup_ui(self):
        """Ana pencere arayüzünü oluşturur."""
        self.setWindowTitle("🔄 NoSQL → SQL Dönüşüm Motoru")
        self.setMinimumSize(QSize(1200, 750))
        self.resize(1400, 850)
        self.setStyleSheet(DARK_THEME)

        # Merkezi widget
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # ═══════════════ ÜST BAR: Başlık + Butonlar ═══════════════
        top_bar = QHBoxLayout()

        # Başlık
        title = QLabel("🔄 NoSQL → SQL Dönüşüm Motoru")
        title.setObjectName("titleLabel")
        top_bar.addWidget(title)
        top_bar.addStretch()

        # JSON Yükle butonu
        self._btn_load = QPushButton("📂 JSON Yükle")
        self._btn_load.setToolTip("Bir JSON dosyası seçip yükleyin")
        self._btn_load.clicked.connect(self._on_load_json)
        top_bar.addWidget(self._btn_load)

        # Dönüştür butonu
        self._btn_convert = QPushButton("▶ Dönüştür")
        self._btn_convert.setToolTip("JSON verisini SQL veritabanına dönüştür")
        self._btn_convert.setEnabled(False)
        self._btn_convert.clicked.connect(self._on_convert)
        top_bar.addWidget(self._btn_convert)

        # DB Sıfırla butonu
        self._btn_drop = QPushButton("🗑️ DB Sıfırla")
        self._btn_drop.setObjectName("btnDrop")
        self._btn_drop.setToolTip("Veritabanındaki tüm tabloları sil")
        self._btn_drop.clicked.connect(self._on_drop)
        top_bar.addWidget(self._btn_drop)

        main_layout.addLayout(top_bar)

        # ═══════════════ ORTA: Splitter (TreeView | DataGrid) ═══════════════
        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(3)

        # Sol panel: JSON Tree View
        self._tree_widget = TreeViewWidget()
        splitter.addWidget(self._tree_widget)

        # Sağ panel: SQL DataGrid
        self._data_grid = DataGridWidget(self._db_engine)
        splitter.addWidget(self._data_grid)

        # Splitter oranları (40% - 60%)
        splitter.setStretchFactor(0, 4)
        splitter.setStretchFactor(1, 6)

        main_layout.addWidget(splitter, stretch=1)

        # ═══════════════ ALT: Durum / Log Paneli ═══════════════
        log_group = QGroupBox("İşlem Günlüğü")
        log_layout = QVBoxLayout(log_group)

        self._log_text = QTextEdit()
        self._log_text.setReadOnly(True)
        self._log_text.setMaximumHeight(140)
        log_layout.addWidget(self._log_text)

        main_layout.addWidget(log_group)

        # Durum çubuğu
        self._status_label = QLabel("Hazır")
        self._status_label.setObjectName("statusLabel")
        main_layout.addWidget(self._status_label)

        # Mevcut tabloları yükle (varsa)
        self._data_grid.refresh_tables()

    # ═══════════════════════════════════════════════════════════
    #                      OLAY YÖNETİCİLERİ
    # ═══════════════════════════════════════════════════════════

    def _on_load_json(self):
        """JSON dosya yükleme butonu olayı."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "JSON Dosyası Seç", "",
            "JSON Dosyaları (*.json);;Tüm Dosyalar (*)"
        )
        if not file_path:
            return

        try:
            self._log(f"📂 Dosya yükleniyor: {file_path}")
            data = self._reader.load_file(file_path)

            # Tree View'da göster
            filename = os.path.basename(file_path)
            self._tree_widget.load_json(data, root_name=filename)

            # Dönüştür butonunu aktifleştir
            self._btn_convert.setEnabled(True)

            # Dosya bilgisi
            info = self._reader.get_file_info()
            self._log(
                f"✅ Dosya yüklendi: {info['filename']} "
                f"({info['size_bytes']} byte, kök tip: {info['root_type']}, "
                f"eleman sayısı: {info['root_length']})"
            )
            self._status("JSON yüklendi — Dönüştürmek için ▶ butonuna basın")

        except (FileNotFoundError, ValueError, IOError) as e:
            self._log(f"❌ Dosya yükleme hatası: {e}")
            QMessageBox.critical(self, "Hata", str(e))

    def _on_convert(self):
        """Dönüştür butonu olayı — JSON → SQL."""
        data = self._reader.get_data()
        if data is None:
            QMessageBox.warning(self, "Uyarı", "Önce bir JSON dosyası yükleyin!")
            return

        try:
            self._log("🔍 JSON analizi başlatılıyor...")
            self._status("Analiz ediliyor...")
            QApplication.processEvents()

            # 1. Analiz et
            self._analyzer.reset()
            schemas = self._analyzer.analyze(data)
            self._log(f"   → {len(schemas)} tablo şeması oluşturuldu")

            # 2. Şemayı hazırla
            self._log("📐 Şema hazırlanıyor...")
            ordered_schemas = self._schema_builder.build(schemas)

            for schema in ordered_schemas:
                fk_info = ""
                if schema.foreign_keys:
                    fk_refs = [f"{fk.column}→{fk.ref_table}" for fk in schema.foreign_keys]
                    fk_info = f" | FK: {', '.join(fk_refs)}"
                col_count = len([c for c in schema.columns if not c.is_primary_key])
                self._log(
                    f"   📋 {schema.name}: {col_count} sütun, "
                    f"{len(schema.records)} kayıt{fk_info}"
                )

            # 3. Mevcut tabloları temizle
            self._log("🗑️ Mevcut tablolar temizleniyor...")
            self._db_engine.drop_all_tables()

            # 4. Tabloları oluştur
            self._log("⚙️ CREATE TABLE sorguları çalıştırılıyor...")
            QApplication.processEvents()

            for schema in ordered_schemas:
                sql = self._query_gen.generate_create_table(schema)
                self._log(f"   SQL: {sql[:100]}...")
                self._db_engine.execute(sql)

            # 5. Verileri yaz
            self._log("📝 INSERT INTO sorguları çalıştırılıyor...")
            QApplication.processEvents()
            total_records = 0

            for schema in ordered_schemas:
                for idx, record in enumerate(schema.records, start=1):
                    sql, params = self._query_gen.generate_insert(schema, record, idx)
                    self._db_engine.execute(sql, params)
                    total_records += 1

            # 6. DataGrid'i güncelle
            self._data_grid.refresh_tables()

            self._log(
                f"✅ Dönüşüm tamamlandı! "
                f"{len(ordered_schemas)} tablo oluşturuldu, "
                f"{total_records} kayıt eklendi."
            )
            self._status(
                f"✅ {len(ordered_schemas)} tablo, {total_records} kayıt — Başarılı"
            )

        except Exception as e:
            error_detail = traceback.format_exc()
            self._log(f"❌ Dönüşüm hatası: {e}\n{error_detail}")
            self._status("❌ Hata oluştu")
            QMessageBox.critical(self, "Dönüşüm Hatası", str(e))

    def _on_drop(self):
        """DB Sıfırla butonu olayı."""
        reply = QMessageBox.question(
            self, "Onay",
            "Veritabanındaki TÜM tablolar silinecek.\nEmin misiniz?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                dropped = self._db_engine.drop_all_tables()
                self._data_grid.refresh_tables()
                self._tree_widget.clear()
                self._btn_convert.setEnabled(False)
                self._reader.reset()

                if dropped:
                    self._log(f"🗑️ {len(dropped)} tablo silindi: {', '.join(dropped)}")
                else:
                    self._log("ℹ️ Silinecek tablo bulunamadı.")

                self._status("Veritabanı sıfırlandı")

            except Exception as e:
                self._log(f"❌ DB sıfırlama hatası: {e}")
                QMessageBox.critical(self, "Hata", str(e))

    # ═══════════════════════════════════════════════════════════
    #                      YARDIMCI METODLAR
    # ═══════════════════════════════════════════════════════════

    def _log(self, message: str) -> None:
        """Log paneline mesaj ekler."""
        self._log_text.append(message)
        # Otomatik en alta kaydır
        scrollbar = self._log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def _status(self, message: str) -> None:
        """Durum çubuğunu günceller."""
        self._status_label.setText(message)

    def closeEvent(self, event):
        """Uygulama kapanırken DB bağlantısını kapat."""
        self._db_engine.close()
        event.accept()
