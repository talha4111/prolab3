"""
PyQt5 Karanlık Tema Stilleri
-----------------------------
Modern, profesyonel karanlık tema CSS tanımları.
"""

DARK_THEME = """
QMainWindow {
    background-color: #1a1a2e;
}

QWidget {
    background-color: #1a1a2e;
    color: #e0e0e0;
    font-family: 'Segoe UI', 'Roboto', sans-serif;
    font-size: 13px;
}

/* Butonlar */
QPushButton {
    background-color: #0f3460;
    color: #ffffff;
    border: 1px solid #533483;
    border-radius: 6px;
    padding: 8px 20px;
    font-weight: bold;
    font-size: 13px;
    min-height: 20px;
}

QPushButton:hover {
    background-color: #533483;
    border-color: #e94560;
}

QPushButton:pressed {
    background-color: #e94560;
}

QPushButton:disabled {
    background-color: #2a2a3e;
    color: #666;
    border-color: #333;
}

QPushButton#btnDrop {
    background-color: #8b0000;
    border-color: #e94560;
}

QPushButton#btnDrop:hover {
    background-color: #e94560;
}

/* Tree View */
QTreeWidget {
    background-color: #16213e;
    border: 1px solid #0f3460;
    border-radius: 6px;
    padding: 5px;
    alternate-background-color: #1a1a2e;
}

QTreeWidget::item {
    padding: 4px 8px;
    border-radius: 3px;
}

QTreeWidget::item:hover {
    background-color: #0f3460;
}

QTreeWidget::item:selected {
    background-color: #533483;
    color: #ffffff;
}

QTreeWidget::branch {
    background-color: #16213e;
}

QHeaderView::section {
    background-color: #0f3460;
    color: #ffffff;
    padding: 6px 10px;
    border: 1px solid #533483;
    font-weight: bold;
}

/* Tablo (DataGrid) */
QTableWidget {
    background-color: #16213e;
    border: 1px solid #0f3460;
    border-radius: 6px;
    gridline-color: #2a2a4a;
    alternate-background-color: #1a1a2e;
}

QTableWidget::item {
    padding: 4px 8px;
}

QTableWidget::item:selected {
    background-color: #533483;
    color: #ffffff;
}

/* ComboBox */
QComboBox {
    background-color: #16213e;
    border: 1px solid #0f3460;
    border-radius: 6px;
    padding: 6px 12px;
    min-width: 200px;
    color: #e0e0e0;
}

QComboBox:hover {
    border-color: #533483;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox QAbstractItemView {
    background-color: #16213e;
    border: 1px solid #533483;
    selection-background-color: #533483;
    color: #e0e0e0;
}

/* Etiketler */
QLabel {
    color: #e0e0e0;
    font-size: 13px;
}

QLabel#titleLabel {
    font-size: 20px;
    font-weight: bold;
    color: #e94560;
}

QLabel#statusLabel {
    font-size: 12px;
    color: #a0a0c0;
    padding: 4px 8px;
    background-color: #16213e;
    border: 1px solid #0f3460;
    border-radius: 4px;
}

/* Grup Kutusu */
QGroupBox {
    border: 1px solid #0f3460;
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 20px;
    font-weight: bold;
    color: #e94560;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 15px;
    padding: 0 8px;
}

/* Splitter */
QSplitter::handle {
    background-color: #533483;
    width: 2px;
}

QSplitter::handle:hover {
    background-color: #e94560;
}

/* ScrollBar */
QScrollBar:vertical {
    background: #1a1a2e;
    width: 10px;
    border-radius: 5px;
}

QScrollBar::handle:vertical {
    background: #533483;
    min-height: 30px;
    border-radius: 5px;
}

QScrollBar::handle:vertical:hover {
    background: #e94560;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar:horizontal {
    background: #1a1a2e;
    height: 10px;
    border-radius: 5px;
}

QScrollBar::handle:horizontal {
    background: #533483;
    min-width: 30px;
    border-radius: 5px;
}

QScrollBar::handle:horizontal:hover {
    background: #e94560;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0;
}

/* Log/TextEdit */
QTextEdit {
    background-color: #16213e;
    border: 1px solid #0f3460;
    border-radius: 6px;
    color: #a0e0a0;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 12px;
    padding: 5px;
}

/* Tab Widget */
QTabWidget::pane {
    border: 1px solid #0f3460;
    border-radius: 6px;
    background-color: #16213e;
}

QTabBar::tab {
    background-color: #1a1a2e;
    color: #a0a0c0;
    padding: 8px 16px;
    border: 1px solid #0f3460;
    border-bottom: none;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    margin-right: 2px;
}

QTabBar::tab:selected {
    background-color: #16213e;
    color: #e94560;
    font-weight: bold;
}

QTabBar::tab:hover {
    background-color: #0f3460;
    color: #ffffff;
}
"""
