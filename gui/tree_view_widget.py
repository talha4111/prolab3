"""
JSON Tree View Widget
----------------------
Yüklenen JSON verisini hiyerarşik ağaç yapısında (Tree View)
görselleştiren PyQt5 widget'ı.
Objeler, diziler ve primitif değerler farklı ikonlarla gösterilir.
"""

from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
from typing import Any, Union


class TreeViewWidget(QWidget):
    """JSON verisini ağaç yapısında gösteren widget."""

    # Tip renklerini tanımla
    TYPE_COLORS = {
        "str": QColor("#a8e6cf"),      # Yeşil - metin
        "int": QColor("#ffd3b6"),      # Turuncu - tam sayı
        "float": QColor("#ffaaa5"),    # Pembe - ondalık
        "bool": QColor("#d4a5ff"),     # Mor - boolean
        "null": QColor("#888888"),     # Gri - null
        "dict": QColor("#85c1e9"),     # Mavi - obje
        "list": QColor("#f9e79f"),     # Sarı - dizi
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        """Widget arayüzünü oluşturur."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Başlık
        self._title = QLabel("📋 JSON Ağaç Görünümü")
        title_font = QFont("Segoe UI", 12, QFont.Bold)
        self._title.setFont(title_font)
        self._title.setStyleSheet("color: #e94560; padding: 5px;")
        layout.addWidget(self._title)

        # Ağaç widget'ı
        self._tree = QTreeWidget()
        self._tree.setHeaderLabels(["Anahtar", "Değer", "Tip"])
        self._tree.setColumnWidth(0, 250)
        self._tree.setColumnWidth(1, 300)
        self._tree.setColumnWidth(2, 100)
        self._tree.setAlternatingRowColors(True)
        self._tree.setAnimated(True)
        layout.addWidget(self._tree)

    def load_json(self, data: Union[dict, list], root_name: str = "root") -> None:
        """
        JSON verisini ağaca yükler.
        
        Args:
            data: JSON verisi (dict veya list)
            root_name: Kök düğüm adı
        """
        self._tree.clear()

        root_item = QTreeWidgetItem(self._tree)
        root_item.setText(0, root_name)

        if isinstance(data, dict):
            root_item.setText(2, "Object")
            root_item.setForeground(2, self.TYPE_COLORS["dict"])
            self._add_dict_items(data, root_item)
        elif isinstance(data, list):
            root_item.setText(1, f"[{len(data)} eleman]")
            root_item.setText(2, "Array")
            root_item.setForeground(2, self.TYPE_COLORS["list"])
            self._add_list_items(data, root_item)

        root_item.setExpanded(True)
        self._tree.expandToDepth(1)

    def _add_dict_items(self, data: dict, parent: QTreeWidgetItem) -> None:
        """Dict elemanlarını ağaca ekler."""
        for key, value in data.items():
            item = QTreeWidgetItem(parent)
            item.setText(0, str(key))
            self._set_value_display(item, value)

    def _add_list_items(self, data: list, parent: QTreeWidgetItem) -> None:
        """List elemanlarını ağaca ekler."""
        for idx, value in enumerate(data):
            item = QTreeWidgetItem(parent)
            item.setText(0, f"[{idx}]")
            self._set_value_display(item, value)

    def _set_value_display(self, item: QTreeWidgetItem, value: Any) -> None:
        """Değer tipine göre ağaç düğümünü ayarlar."""
        if isinstance(value, dict):
            item.setText(1, f"{{{len(value)} alan}}")
            item.setText(2, "Object")
            item.setForeground(2, self.TYPE_COLORS["dict"])
            bold_font = QFont()
            bold_font.setBold(True)
            item.setFont(0, bold_font)
            self._add_dict_items(value, item)

        elif isinstance(value, list):
            item.setText(1, f"[{len(value)} eleman]")
            item.setText(2, "Array")
            item.setForeground(2, self.TYPE_COLORS["list"])
            bold_font = QFont()
            bold_font.setBold(True)
            item.setFont(0, bold_font)
            self._add_list_items(value, item)

        elif isinstance(value, str):
            item.setText(1, f'"{value}"')
            item.setText(2, "String")
            item.setForeground(1, self.TYPE_COLORS["str"])
            item.setForeground(2, self.TYPE_COLORS["str"])

        elif isinstance(value, bool):
            item.setText(1, str(value).lower())
            item.setText(2, "Boolean")
            item.setForeground(1, self.TYPE_COLORS["bool"])
            item.setForeground(2, self.TYPE_COLORS["bool"])

        elif isinstance(value, int):
            item.setText(1, str(value))
            item.setText(2, "Integer")
            item.setForeground(1, self.TYPE_COLORS["int"])
            item.setForeground(2, self.TYPE_COLORS["int"])

        elif isinstance(value, float):
            item.setText(1, str(value))
            item.setText(2, "Float")
            item.setForeground(1, self.TYPE_COLORS["float"])
            item.setForeground(2, self.TYPE_COLORS["float"])

        elif value is None:
            item.setText(1, "null")
            item.setText(2, "Null")
            item.setForeground(1, self.TYPE_COLORS["null"])
            item.setForeground(2, self.TYPE_COLORS["null"])

    def clear(self) -> None:
        """Ağacı temizler."""
        self._tree.clear()
