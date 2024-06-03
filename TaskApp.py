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

        self.task_name_label = tk.Label(self.root, text='Task Name:')
        self.task_name_label.pack()
        self.task_entry = tk.Entry(self.root, width=50)
        self.task_entry.pack()

        self.due_date_label = tk.Label(self.root, text='Date DD-MM-YYYY:')
        self.due_date_label.pack()
        self.due_date_entry = tk.Entry(self.root, width=50)
        self.due_date_entry.pack()

        self.due_time_label = tk.Label(self.root, text='Time HH:MM:')
        self.due_time_label.pack()
        self.due_time_entry = tk.Entry(self.root, width=50)
        self.due_time_entry.pack()

        self.add_button = tk.Button(self.root, text='Add Task', command=self.add_task)
        self.add_button.pack()

        self.pending_tasks_label = tk.Label(self.root, text='Pending Tasks:')
        self.pending_tasks_label.pack()
        self.task_listbox = tk.Listbox(self.root, width=100)
        self.task_listbox.pack()

        self.complete_button = tk.Button(self.root, text='Mark as Completed', command=self.complete_task)
        self.complete_button.pack()

        self.delete_all_button = tk.Button(self.root, text='Clear All Pending Tasks', command=self.clear_all_pending_tasks)
        self.delete_all_button.pack()

        self.completed_tasks_label = tk.Label(self.root, text='Completed Tasks:')
        self.completed_tasks_label.pack()
        self.completed_listbox = tk.Listbox(self.root, width=100)
        self.completed_listbox.pack()

        self.delete_all_completed_button = tk.Button(self.root, text='Clear All Completed Tasks',
                                                     command=self.clear_all_completed_tasks)
        self.delete_all_completed_button.pack()

        self.load_tasks()

    def add_task(self):
        task_name = self.task_entry.get()
        due_date = self.due_date_entry.get()
        due_time = self.due_time_entry.get()
        try:
            formatted_due_date = datetime.strptime(due_date, '%d-%m-%Y').strftime('%Y-%m-%d')
            datetime.strptime(formatted_due_date + ' ' + due_time, '%Y-%m-%d %H:%M')
            if task_name and due_date and due_time:
                task = {'name': task_name, 'due_date': formatted_due_date, 'due_time': due_time, 'status': 'Pending'}
                self.manager.add_task(self.username, task)
                self.task_entry.delete(0, tk.END)
                self.due_date_entry.delete(0, tk.END)
                self.due_time_entry.delete(0, tk.END)
                self.load_tasks()
            else:
                messagebox.showerror('Error', 'Please enter task name, due date and due time')
        except ValueError:
            messagebox.showerror('Error',
                                 'Invalid date or time format. Please use DD-MM-YYYY for date and HH:MM for time')

    def load_tasks(self):
        self.task_listbox.delete(0, tk.END)
        tasks = self.manager.get_tasks(self.username)
        for task in tasks:
            self.task_listbox.insert(tk.END,
                                     f"{task['name']} - {task['due_date']} - {task['due_time']} - {task['status']}")

        self.completed_listbox.delete(0, tk.END)
        completed_tasks = self.manager.get_completed_tasks_with_time(self.username)
        for task in completed_tasks:
            self.completed_listbox.insert(tk.END, f"{task['name']} - Due to {task['due']} - Completed at {task['completed_at']}")

    def complete_task(self):
        selected_task = self.task_listbox.get(tk.ACTIVE)
        if selected_task:
            task_split = selected_task.split(' - ')
            task_name = task_split[0]
            task_due_date = task_split[1]
            task_due_time = task_split[2]
            self.manager.complete_task(self.username, task_name, task_due_date, task_due_time)
            self.load_tasks()

    def show_completed_tasks(self):
        self.completed_listbox.delete(0, tk.END)
        completed_tasks = self.manager.get_completed_tasks(self.username)
        for task in completed_tasks:
            self.completed_listbox.insert(tk.END, f"{task['name']} - {task['due_date']} - {task['status']}")

    def clear_all_pending_tasks(self):
        if messagebox.askyesno('Confirm', 'Are you sure you want to clear all pending tasks?'):
            self.manager.delete_all_tasks(self.username)
            self.load_tasks()

    def clear_all_completed_tasks(self):
        if messagebox.askyesno('Confirm', 'Are you sure you want to clear all completed tasks?'):
            self.manager.delete_all_completed_tasks(self.username)
            self.show_completed_tasks()
