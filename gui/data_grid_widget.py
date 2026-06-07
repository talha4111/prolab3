"""
SQL DataGrid Widget
--------------------
Veritabanında oluşturulan tabloları ve içeriklerini
DataGrid (tablo) formatında gösteren PyQt5 widget'ı.
Kullanıcı ComboBox ile tablolar arasında geçiş yapabilir.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QTableWidget, QTableWidgetItem, QGroupBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from typing import List, Tuple, Optional

from modules.database_engine import DatabaseEngine


class DataGridWidget(QWidget):
    """SQL tablo verilerini DataGrid formatında gösteren widget."""

    def __init__(self, db_engine: DatabaseEngine, parent=None):
        super().__init__(parent)
        self._db_engine = db_engine
        self._setup_ui()

    def _setup_ui(self):
        """Widget arayüzünü oluşturur."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Başlık
        self._title = QLabel("📊 SQL Tablo Görünümü")
        title_font = QFont("Segoe UI", 12, QFont.Bold)
        self._title.setFont(title_font)
        self._title.setStyleSheet("color: #e94560; padding: 5px;")
        layout.addWidget(self._title)

        # Tablo seçici
        selector_layout = QHBoxLayout()
        selector_label = QLabel("Tablo:")
        selector_label.setStyleSheet("font-weight: bold; color: #85c1e9;")
        selector_layout.addWidget(selector_label)

        self._table_combo = QComboBox()
        self._table_combo.currentTextChanged.connect(self._on_table_selected)
        selector_layout.addWidget(self._table_combo)

        # Kayıt sayısı etiketi
        self._record_count = QLabel("")
        self._record_count.setStyleSheet("color: #a0a0c0; margin-left: 10px;")
        selector_layout.addWidget(self._record_count)
        selector_layout.addStretch()

        layout.addLayout(selector_layout)

        # Tablo bilgi grubu (sütun bilgileri)
        self._info_group = QGroupBox("Tablo Yapısı")
        info_layout = QVBoxLayout(self._info_group)
        self._info_label = QLabel("")
        self._info_label.setWordWrap(True)
        self._info_label.setStyleSheet("color: #a8e6cf; font-size: 11px;")
        info_layout.addWidget(self._info_label)
        layout.addWidget(self._info_group)

        # DataGrid tablosu
        self._table = QTableWidget()
        self._table.setAlternatingRowColors(True)
        self._table.setSelectionBehavior(QTableWidget.SelectRows)
        self._table.setSortingEnabled(True)
        self._table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self._table)

    def refresh_tables(self) -> None:
        """Veritabanındaki tablo listesini yeniler."""
        self._table_combo.blockSignals(True)
        self._table_combo.clear()

        if self._db_engine.is_connected:
            tables = self._db_engine.get_table_names()
            self._table_combo.addItems(tables)

        self._table_combo.blockSignals(False)

        # İlk tabloyu göster
        if self._table_combo.count() > 0:
            self._table_combo.setCurrentIndex(0)
            self._on_table_selected(self._table_combo.currentText())
        else:
            self._table.clear()
            self._table.setRowCount(0)
            self._table.setColumnCount(0)
            self._info_label.setText("")
            self._record_count.setText("")

    def _on_table_selected(self, table_name: str) -> None:
        """Kullanıcı tablo seçtiğinde verileri yükler."""
        if not table_name or not self._db_engine.is_connected:
            return

        try:
            # Tablo verilerini al
            columns, rows = self._db_engine.fetch_table_data(table_name)

            # DataGrid'i doldur
            self._table.clear()
            self._table.setColumnCount(len(columns))
            self._table.setRowCount(len(rows))
            self._table.setHorizontalHeaderLabels(columns)

            for row_idx, row in enumerate(rows):
                for col_idx, value in enumerate(row):
                    item = QTableWidgetItem(str(value) if value is not None else "NULL")
                    if value is None:
                        item.setForeground(QColor("#888888"))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self._table.setItem(row_idx, col_idx, item)

            # Sütun genişliklerini ayarla
            self._table.resizeColumnsToContents()

            # Kayıt sayısı
            self._record_count.setText(f"({len(rows)} kayıt)")

            # Tablo yapı bilgisi
            self._show_table_info(table_name)

        except Exception as e:
            self._record_count.setText(f"Hata: {e}")

    def _show_table_info(self, table_name: str) -> None:
        """Tablo sütun ve FK bilgilerini gösterir."""
        try:
            info = self._db_engine.get_table_info(table_name)
            fks = self._db_engine.get_foreign_keys(table_name)

            info_parts = []
            for col in info:
                pk_mark = " 🔑PK" if col["pk"] else ""
                fk_mark = ""
                for fk in fks:
                    if fk["from"] == col["name"]:
                        fk_mark = f" 🔗FK→{fk['table']}.{fk['to']}"
                info_parts.append(f'{col["name"]} ({col["type"]}{pk_mark}{fk_mark})')

            self._info_label.setText(" | ".join(info_parts))

        except Exception:
            self._info_label.setText("")

    def clear(self) -> None:
        """Widget'ı temizler."""
        self._table_combo.clear()
        self._table.clear()
        self._table.setRowCount(0)
        self._table.setColumnCount(0)
        self._info_label.setText("")
        self._record_count.setText("")
