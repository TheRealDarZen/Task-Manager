import shelve
from datetime import datetime, timedelta
from plyer import notification
import time


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
                if task['status'] not in ['Completed', 'Completed, Late'] and (due_datetime + timedelta(minutes=1)) < datetime.now():
                    task['status'] = 'Pending, Late'
            db[username] = tasks
            return tasks

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

    def get_stats(self, username):
        pending_tasks = self.get_tasks(username)
        completed_tasks = self.get_completed_tasks(username)
        completed_tasks_count = len(completed_tasks)
        completed_on_time_tasks_count = len([task for task in completed_tasks if task['status'] == 'Completed'])
        pending_tasks_count = len(pending_tasks)
        completed_late_tasks_count = len([task for task in completed_tasks if task['status'] == 'Completed, Late'])
        pending_late_tasks_count = len([task for task in pending_tasks if task['status'] == 'Pending, Late'])
        total_tasks_count = len(pending_tasks) + len(completed_tasks)
        return total_tasks_count, completed_tasks_count, completed_on_time_tasks_count, pending_tasks_count, completed_late_tasks_count, pending_late_tasks_count

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

    def check_due_tasks(self, username):
        while True:
            with shelve.open(self.db_name) as db:
                tasks = db.get(username, [])
                now = datetime.now()
                for task in tasks:
                    due_date = datetime.strptime(task['due_date'] + ' ' + task['due_time'], '%Y-%m-%d %H:%M')
                    if task['status'] == 'Pending' and now >= due_date - timedelta(minutes=180):
                        notification.notify(
                            title=f"Task Due Soon: {task['name']}",
                            message=f"{username}, you have a task: {task['name']} due at {task['due_time']} on {task['due_date']}."
                                    f" The priority of this task is {task['priority']}.",
                            timeout=30
                        )
            time.sleep(900) # 15 minutes

    def update_status(self, func):
        last_time = datetime.now().strftime('%H:%M')
        while True:
            current_time = datetime.now().strftime('%H:%M')
            if current_time != last_time:
                if func:
                    func()
                last_time = current_time
            time.sleep(1)
