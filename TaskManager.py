import shelve
from datetime import datetime


class TaskManager:
    def __init__(self, db_name='database/tasks.db'):
        self.db_name = db_name

    def add_task(self, username, task):
        with shelve.open(self.db_name, writeback=True) as db:
            tasks = db.get(username, [])
            tasks.append(task)
            db[username] = tasks

    def get_tasks(self, username):
        with shelve.open(self.db_name, writeback=True) as db:
            tasks = db.get(username, [])
            for task in tasks:
                due_datetime = datetime.strptime(task['due_date'] + ' ' + task['due_time'], '%Y-%m-%d %H:%M')
                if task['status'] != 'Completed' and due_datetime < datetime.now():
                    task['status'] = 'Late'
            db[username] = tasks
            return tasks

    def complete_task(self, username, task_name):
        with shelve.open(self.db_name, writeback=True) as db:
            tasks = db.get(username, [])
            completed_tasks = db.get(f"{username}_completed", [])
            for task in tasks:
                if task['name'] == task_name:
                    if task['status'] == 'Late':
                        task['status'] = 'Completed, Late'
                    else:
                        task['status'] = 'Completed'
                    completed_tasks.append(task)
                    tasks.remove(task)
                    break
            db[username] = tasks
            db[f"{username}_completed"] = completed_tasks

    def get_completed_tasks(self, username):
        with shelve.open(self.db_name) as db:
            return db.get(f"{username}_completed", [])

    def delete_all_tasks(self, username):
        with shelve.open(self.db_name, writeback=True) as db:
            db[username] = []

    def delete_all_completed_tasks(self, username):
        with shelve.open(self.db_name, writeback=True) as db:
            db[f"{username}_completed"] = []
