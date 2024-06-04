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
                if task['status'] not in ['Completed', 'Completed, Late'] and due_datetime < datetime.now():
                    task['status'] = 'Pending, Late'
            db[username] = tasks
            return tasks

    def update_task(self, username, old_task_name, new_task):
        with shelve.open(self.db_name, writeback=True) as db:
            tasks = db.get(username, [])
            for task in tasks:
                if task['name'] == old_task_name:
                    tasks.remove(task)
                    tasks.append(new_task)
                    break
            db[username] = tasks

    def get_completed_tasks_with_time(self, username):
        with shelve.open(self.db_name) as db:
            completed_tasks = db.get(f"{username}_completed", [])
            return completed_tasks

    def complete_task(self, username, task_name):
        with shelve.open(self.db_name, writeback=True) as db:
            tasks = db.get(username, [])
            completed_tasks = db.get(f"{username}_completed", [])
            for task in tasks:
                if task['name'] == task_name:
                    if task['status'] == 'Pending, Late':
                        task['status'] = 'Completed, Late'
                    else:
                        task['status'] = 'Completed'
                    task['completed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M')
                    completed_tasks.append(task)
                    tasks.remove(task)
                    break
            db[username] = tasks
            db[f"{username}_completed"] = completed_tasks

    def get_completed_tasks(self, username):
        with shelve.open(self.db_name) as db:
            return db.get(f"{username}_completed", [])

    def delete_task(self, username, task_name, completed=False):
        with shelve.open(self.db_name, writeback=True) as db:
            if completed:
                tasks = db.get(f"{username}_completed", [])
            else:
                tasks = db.get(username, [])
            for task in tasks:
                if task['name'] == task_name:
                    tasks.remove(task)
                    break
            if completed:
                db[f"{username}_completed"] = tasks
            else:
                db[username] = tasks

    def delete_all_tasks(self, username):
        with shelve.open(self.db_name, writeback=True) as db:
            db[username] = []

    def delete_all_completed_tasks(self, username):
        with shelve.open(self.db_name, writeback=True) as db:
            db[f"{username}_completed"] = []
