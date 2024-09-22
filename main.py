import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, 
                               QListWidget, QPushButton, QInputDialog, QHBoxLayout,
                               QCheckBox, QListWidgetItem, QMessageBox, QLabel, QProgressBar)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

class TaskWidget(QWidget):
    def __init__(self, task_text, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.checkbox = QCheckBox(task_text)
        self.delete_button = QPushButton()
        self.delete_button.setIcon(QIcon("trash_icon.png"))
        self.delete_button.setFixedSize(20, 20)

        layout.addWidget(self.checkbox)
        layout.addStretch()
        layout.addWidget(self.delete_button)

class TodoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TODO List")
        self.setGeometry(100, 100, 300, 400)

        # Main layout
        layout = QVBoxLayout()

        # Task list
        self.task_list = QListWidget()
        layout.addWidget(self.task_list)

        # Add task button
        self.add_button = QPushButton("Add Task")
        self.add_button.clicked.connect(self.add_task)
        layout.addWidget(self.add_button, alignment=Qt.AlignCenter)

        # Tasks completed label
        self.tasks_completed_label = QLabel("Tasks completed: 0/0")
        layout.addWidget(self.tasks_completed_label)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setFormat("%p%")
        
        # Style sheet for the progress bar
        self.progress_bar.setStyleSheet("""
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
        
        layout.addWidget(self.progress_bar)

        # Central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.update_progress()

    def add_task(self):
        task_text, ok = QInputDialog.getText(self, "Add Task", "Enter task:")
        if ok and task_text:
            self.add_task_to_list(task_text)

    def add_task_to_list(self, task_text):
        item = QListWidgetItem(self.task_list)
        task_widget = TaskWidget(task_text)
        item.setSizeHint(task_widget.sizeHint())
        self.task_list.addItem(item)
        self.task_list.setItemWidget(item, task_widget)

        task_widget.delete_button.clicked.connect(lambda: self.confirm_delete_task(item))
        task_widget.checkbox.stateChanged.connect(self.update_progress)

        self.update_progress()

    def confirm_delete_task(self, item):
        task_widget = self.task_list.itemWidget(item)
        task_text = task_widget.checkbox.text()
        
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setText(f"Are you sure you want to delete the task:\n'{task_text}'?")
        msg_box.setWindowTitle("Confirm Delete")
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg_box.setDefaultButton(QMessageBox.Cancel)

        if msg_box.exec() == QMessageBox.Ok:
            self.delete_task(item)

    def delete_task(self, item):
        self.task_list.takeItem(self.task_list.row(item))
        self.update_progress()

    def update_progress(self):
        total_tasks = self.task_list.count()
        completed_tasks = sum(
            1 for i in range(total_tasks)
            if self.task_list.itemWidget(self.task_list.item(i)).checkbox.isChecked()
        )
        
        self.tasks_completed_label.setText(f"Tasks completed: {completed_tasks}/{total_tasks}")
        
        progress_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        self.progress_bar.setValue(int(progress_percentage))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TodoApp()
    window.show()
    sys.exit(app.exec())