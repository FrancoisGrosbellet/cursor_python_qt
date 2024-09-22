from PySide6.QtWidgets import QWidget, QHBoxLayout, QCheckBox, QPushButton
from PySide6.QtGui import QIcon

class TaskWidget(QWidget):
    def __init__(self, task_text, parent=None):
        super().__init__(parent)
        self.init_ui(task_text)

    def init_ui(self, task_text):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.checkbox = QCheckBox(task_text)
        self.delete_button = QPushButton()
        self.delete_button.setIcon(QIcon("trash_icon.png"))
        self.delete_button.setFixedSize(20, 20)

        layout.addWidget(self.checkbox)
        layout.addStretch()
        layout.addWidget(self.delete_button)
