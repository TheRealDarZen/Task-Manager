import tkinter as tk
from datetime import datetime
from tkinter import messagebox
import tkinter.ttk as ttk

from TaskManager import TaskManager


class TaskApp:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.manager = TaskManager()
        self.create_task_ui()

    def create_task_ui(self):
        self.root.title(f'Task Manager - {self.username}')

        # Frame for task input
        task_input_frame = tk.Frame(self.root)
        task_input_frame.pack(padx=10, pady=10, fill='x')

        self.task_name_label = tk.Label(task_input_frame, text='Task Name:')
        self.task_name_label.grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.task_entry = tk.Entry(task_input_frame, width=50)
        self.task_entry.grid(row=0, column=1, padx=5, pady=5)

        self.due_date_label = tk.Label(task_input_frame, text='Date DD-MM-YYYY:')
        self.due_date_label.grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.due_date_entry = tk.Entry(task_input_frame, width=50)
        self.due_date_entry.grid(row=1, column=1, padx=5, pady=5)

        self.due_time_label = tk.Label(task_input_frame, text='Time HH:MM:')
        self.due_time_label.grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.due_time_entry = tk.Entry(task_input_frame, width=50)
        self.due_time_entry.grid(row=2, column=1, padx=5, pady=5)

        self.priority_label = tk.Label(task_input_frame, text='Priority:')
        self.priority_label.grid(row=3, column=0, sticky='e', padx=5, pady=5)
        self.priority_combobox = ttk.Combobox(task_input_frame, values=['Highest', 'High', 'Moderate', 'Low'])
        self.priority_combobox.current(2)
        self.priority_combobox.grid(row=3, column=1, padx=5, pady=5)

        self.add_button = tk.Button(task_input_frame, text='Add Task', command=self.add_task, padx=10)
        self.add_button.grid(row=4, column=1, columnspan=2, pady=10)

        # Frame for pending tasks
        pending_tasks_frame = tk.Frame(self.root)
        pending_tasks_frame.pack(padx=10, pady=10, fill='x')

        self.pending_tasks_label = tk.Label(pending_tasks_frame, text='Pending Tasks:')
        self.pending_tasks_label.pack()
        self.task_listbox = tk.Listbox(pending_tasks_frame, width=100)
        self.task_listbox.pack(pady=5)

        self.complete_button = tk.Button(pending_tasks_frame, text='Mark as Completed', command=self.complete_task)
        self.complete_button.pack(pady=5)

        self.clear_all_pending_button = tk.Button(pending_tasks_frame, text='Clear All Pending Tasks',
                                                  command=self.clear_all_pending_tasks)
        self.clear_all_pending_button.pack(pady=5)

        # Frame for completed tasks
        completed_tasks_frame = tk.Frame(self.root)
        completed_tasks_frame.pack(padx=10, pady=10, fill='x')

        self.completed_tasks_label = tk.Label(completed_tasks_frame, text='Completed Tasks:')
        self.completed_tasks_label.pack()
        self.completed_listbox = tk.Listbox(completed_tasks_frame, width=100)
        self.completed_listbox.pack(pady=5)

        self.clear_all_completed_button = tk.Button(completed_tasks_frame, text='Clear All Completed Tasks',
                                                    command=self.clear_all_completed_tasks)
        self.clear_all_completed_button.pack(pady=5)

        self.load_tasks()

    def add_task(self):
        task_name = self.task_entry.get()
        due_date = self.due_date_entry.get()
        due_time = self.due_time_entry.get()
        priority = self.priority_combobox.get()
        try:
            formatted_due_date = datetime.strptime(due_date, '%d-%m-%Y').strftime('%Y-%m-%d')
            datetime.strptime(formatted_due_date + ' ' + due_time, '%Y-%m-%d %H:%M')
            if task_name and due_date and due_time:
                task = {'name': task_name, 'due_date': formatted_due_date, 'due_time': due_time, 'priority': priority,
                        'status': 'Pending'}
                self.manager.add_task(self.username, task)
                self.task_entry.delete(0, tk.END)
                self.due_date_entry.delete(0, tk.END)
                self.due_time_entry.delete(0, tk.END)
                self.priority_combobox.current(2)
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
                                     f"{task['name']} - {task['due_date']} {task['due_time']} - {task['priority']} - {task['status']}")

        self.completed_listbox.delete(0, tk.END)
        completed_tasks = self.manager.get_completed_tasks_with_time(self.username)
        for task in completed_tasks:
            self.completed_listbox.insert(tk.END, f"{task['name']} - Due to {task['due_date']} {task['due_time']} - {task['priority']} - Completed at {task['completed_at']}")

    def complete_task(self):
        selected_task = self.task_listbox.get(tk.ACTIVE)
        if selected_task:
            task_split = selected_task.split(' - ')
            task_name = task_split[0]
            self.manager.complete_task(self.username, task_name)
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
