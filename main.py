import sys
from PySide6.QtWidgets import QApplication
from todo_app import TodoApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TodoApp()
    window.show()
    sys.exit(app.exec())