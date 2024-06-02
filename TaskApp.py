import tkinter as tk
from datetime import datetime
from tkinter import messagebox

from TaskManager import TaskManager


class TaskApp:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.manager = TaskManager()
        self.create_task_ui()

    def create_task_ui(self):
        self.root.title(f'Task Manager - {self.username}')

        self.task_entry = tk.Entry(self.root, width=50)
        self.task_entry.pack()

        self.due_date_entry = tk.Entry(self.root)
        self.due_date_entry.insert(0, 'YYYY-MM-DD')
        self.due_date_entry.pack()

        self.add_button = tk.Button(self.root, text='Add Task', command=self.add_task)
        self.add_button.pack()

        self.task_listbox = tk.Listbox(self.root, width=50)
        self.task_listbox.pack()

        self.complete_button = tk.Button(self.root, text='Mark as Completed', command=self.complete_task)
        self.complete_button.pack()

        self.show_completed_button = tk.Button(self.root, text='Show Completed Tasks', command=self.show_completed_tasks)
        self.show_completed_button.pack()

        self.completed_listbox = tk.Listbox(self.root, width=50)
        self.completed_listbox.pack()

        self.delete_all_tasks_button = tk.Button(self.root, text='Delete All Active Tasks',
                                                 command=self.delete_all_tasks)
        self.delete_all_tasks_button.pack()

        self.delete_all_completed_tasks_button = tk.Button(self.root, text='Delete All Completed Tasks',
                                                 command=self.delete_all_completed_tasks)
        self.delete_all_completed_tasks_button.pack()

        self.load_tasks()

    def add_task(self):
        task_name = self.task_entry.get()
        due_date = self.due_date_entry.get()
        try:
            datetime.strptime(due_date, '%Y-%m-%d')
            if task_name and due_date:
                task = {'name': task_name, 'due_date': due_date, 'status': 'Pending'}
                self.manager.add_task(self.username, task)
                self.task_entry.delete(0, tk.END)
                self.due_date_entry.delete(0, tk.END)
                self.load_tasks()
            else:
                messagebox.showerror('Error', 'Please enter both task name and due date')
        except ValueError:
            messagebox.showerror('Error', 'Invalid date format. Please use YYYY-MM-DD')

    def load_tasks(self):
        self.task_listbox.delete(0, tk.END)
        tasks = self.manager.get_tasks(self.username)
        for task in tasks:
            self.task_listbox.insert(tk.END, f"{task['name']} - {task['due_date']} - {task['status']}")

    def complete_task(self):
        selected_task = self.task_listbox.get(tk.ACTIVE)
        if selected_task:
            task_name = selected_task.split(' - ')[0]
            self.manager.complete_task(self.username, task_name)
            self.load_tasks()

    def show_completed_tasks(self):
        self.completed_listbox.delete(0, tk.END)
        completed_tasks = self.manager.get_completed_tasks(self.username)
        for task in completed_tasks:
            self.completed_listbox.insert(tk.END, f"{task['name']} - {task['due_date']} - {task['status']}")

    def delete_all_tasks(self):
        if messagebox.askyesno('Confirm', 'Are you sure you want to delete all active tasks?'):
            self.manager.delete_all_tasks(self.username)
            self.load_tasks()

    def delete_all_completed_tasks(self):
        if messagebox.askyesno('Confirm', 'Are you sure you want to delete all completed tasks?'):
            self.manager.delete_all_completed_tasks(self.username)
            self.show_completed_tasks()
