"""
NoSQL → SQL Dönüşüm Motoru
============================
Kocaeli Üniversitesi - Bilgisayar Mühendisliği
Programlama Laboratuvarı II - Proje 3

Yapısı önceden bilinmeyen karmaşık JSON (NoSQL) verilerini
dinamik olarak analiz edip ilişkisel SQL (SQLite) veritabanına
dönüştüren jenerik masaüstü uygulaması.

Çalıştırma:
    python main.py
"""

import sys
import os

# Proje kök dizinini Python path'ine ekle
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from gui.main_window import MainWindow


def main():
    """Uygulamayı başlatır."""
    # High DPI desteği
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setApplicationName("NoSQL → SQL Dönüşüm Motoru")

    # Ana pencereyi oluştur ve göster
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
