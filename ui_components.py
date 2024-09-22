from PySide6.QtWidgets import QProgressBar
from PySide6.QtCore import Qt

class CustomProgressBar(QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTextVisible(True)
        self.setAlignment(Qt.AlignCenter)
        self.setFormat("%p%")
        self.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 5px;
                text-align: center;
                padding: 1px;
                font-size: 14px;
                height: 30px;
                background-color: palette(base);
            }
            QProgressBar::chunk {
                background-color: palette(highlight);
                border-radius: 5px;
            }
        """)
