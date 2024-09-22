from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QListWidget, QPushButton, QLabel, QInputDialog, QMessageBox, QListWidgetItem
from PySide6.QtCore import Qt
from task_widget import TaskWidget
from task_manager import TaskManager
from ui_components import CustomProgressBar

class TodoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TODO List")
        self.setGeometry(100, 100, 300, 400)

        self.task_manager = TaskManager()

        self.init_ui()
        self.load_tasks()

    def init_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        self.task_list = QListWidget()
        layout.addWidget(self.task_list)

        self.add_button = QPushButton("Add Task")
        self.add_button.clicked.connect(self.add_task)
        layout.addWidget(self.add_button, alignment=Qt.AlignCenter)

        self.tasks_completed_label = QLabel("Tasks completed: 0/0")
        layout.addWidget(self.tasks_completed_label)

        self.progress_bar = CustomProgressBar()
        layout.addWidget(self.progress_bar)

        self.setCentralWidget(central_widget)

    def load_tasks(self):
        tasks = self.task_manager.load_tasks()
        for task in tasks:
            self.add_task_to_list(task['text'], task['completed'])

    def add_task(self):
        task_text, ok = QInputDialog.getText(self, "Add Task", "Enter task:")
        if ok and task_text:
            self.add_task_to_list(task_text)

    def add_task_to_list(self, task_text, completed=False):
        item = QListWidgetItem(self.task_list)
        task_widget = TaskWidget(task_text)
        task_widget.checkbox.setChecked(completed)
        item.setSizeHint(task_widget.sizeHint())
        self.task_list.addItem(item)
        self.task_list.setItemWidget(item, task_widget)

        task_widget.delete_button.clicked.connect(lambda: self.confirm_delete_task(item))
        task_widget.checkbox.stateChanged.connect(self.update_progress)

        self.task_manager.add_task({'text': task_text, 'completed': completed})
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
        task_widget = self.task_list.itemWidget(item)
        task_text = task_widget.checkbox.text()
        self.task_list.takeItem(self.task_list.row(item))
        self.task_manager.remove_task({'text': task_text, 'completed': task_widget.checkbox.isChecked()})
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

        self.task_manager.save_tasks()
