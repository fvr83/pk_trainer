import sys
import json
import random

from math import ceil, sin, cos, pi
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from PyQt6.QtCore import Qt, QRect, QSize, QPoint, QTimer
from PyQt6.QtGui import (
    QAction,
    QColor,
    QFont,
    QImage,
    QKeySequence,
    QPainter,
    QPen,
    QPixmap,
)

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QListWidget,
    QComboBox,
    QLineEdit,
    QFrame,
    QMainWindow,
    QMessageBox,
)



bgd_color = "#515152"


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Poker Trainer")

        self.resize(1366, 707)

        self.setStyleSheet(f"""
            QMainWindow {{
                background:{bgd_color};
            }}
        """)

        self.central = QWidget()
        self.setCentralWidget(self.central)

        self.folder = ""
        self.depth = ""
        self.hero_position = ""
        self.villain_position = ""
        self.combo_pool_type = ""
        self.spot_action = ""

MainWindow()