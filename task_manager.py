import json
import os

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.filename = 'tasks.json'

    def add_task(self, task):
        self.tasks.append(task)
        self.save_tasks()

    def remove_task(self, task):
        self.tasks = [t for t in self.tasks if t['text'] != task['text']]
        self.save_tasks()

    def save_tasks(self):
        with open(self.filename, 'w') as f:
            json.dump(self.tasks, f)

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                self.tasks = json.load(f)
        return self.tasks
