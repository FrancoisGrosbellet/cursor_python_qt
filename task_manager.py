import json
import os

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.filename = 'tasks.json'

    def add_task(self, task):
        self.tasks.append({'text': task['text'], 'completed': task['completed']})
        self.save_tasks()

    def remove_task(self, task):
        self.tasks = [t for t in self.tasks if t['text'] != task['text']]
        self.save_tasks()

    def update_task_status(self, task_text, completed):
        for task in self.tasks:
            if task['text'] == task_text:
                task['completed'] = completed
                break
        self.save_tasks()

    def save_tasks(self):
        with open(self.filename, 'w') as f:
            json.dump(self.tasks, f)

    def load_tasks(self):
        self.tasks = []
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                content = f.read().strip()
                if not content:
                    # Silently handle empty file case
                    # In this case, we'll just use an empty task list
                    return self.tasks
                
                try:
                    self.tasks = json.loads(content)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON in {self.filename}: {str(e)}")
                    print("Starting with an empty task list.")
                    # Log the error for debugging purposes
                    # You might want to use a proper logging system in a production environment
                    with open('error_log.txt', 'a') as error_log:
                        error_log.write(f"JSON decode error in {self.filename}: {str(e)}\n")
        return self.tasks
