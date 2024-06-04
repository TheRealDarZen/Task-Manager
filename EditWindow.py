from datetime import datetime
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

from UserManager import UserManager
from TaskManager import TaskManager

class EditWindow:
    def __init__(self, root, task, username, callback):
        self.root = root
        self.task = task
        self.username = username
        self.callback = callback
        self.user_manager = UserManager()
        self.task_manager = TaskManager()
        self.create_edit_window()

    def create_edit_window(self):
        task_input_frame = tk.Frame(self.root)
        task_input_frame.pack(padx=10, pady=10, fill='x')

        self.task_name_label = tk.Label(task_input_frame, text='Task Name:')
        self.task_name_label.grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.task_entry = tk.Entry(task_input_frame, width=50)
        self.task_entry.insert(0, self.task['name'])
        self.task_entry.grid(row=0, column=1, padx=5, pady=5)

        self.due_date_label = tk.Label(task_input_frame, text='Date DD-MM-YYYY:')
        self.due_date_label.grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.due_date_entry = tk.Entry(task_input_frame, width=50)
        self.due_date_entry.insert(0, f'{self.task['due_date'].split('-')[2]}-{self.task['due_date'].split('-')[1]}-{self.task['due_date'].split('-')[0]}')
        self.due_date_entry.grid(row=1, column=1, padx=5, pady=5)

        self.due_time_label = tk.Label(task_input_frame, text='Time HH:MM:')
        self.due_time_label.grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.due_time_entry = tk.Entry(task_input_frame, width=50)
        self.due_time_entry.insert(0, self.task['due_time'])
        self.due_time_entry.grid(row=2, column=1, padx=5, pady=5)

        self.priority_label = tk.Label(task_input_frame, text='Priority:')
        self.priority_label.grid(row=3, column=0, sticky='e', padx=5, pady=5)
        self.priority_combobox = ttk.Combobox(task_input_frame, values=['Highest', 'High', 'Moderate', 'Low'],
                                              state='readonly')
        priority_order = {'Highest': 1, 'High': 2, 'Moderate': 3, 'Low': 4}
        self.priority_combobox.current(priority_order[self.task['priority']] - 1)
        self.priority_combobox.grid(row=3, column=1, padx=5, pady=5)

        self.edit_button = tk.Button(task_input_frame, text='Edit Task', command=self.edit_task, padx=10)
        self.edit_button.grid(row=4, column=1, columnspan=2, pady=10)

    def edit_task(self):
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
                self.task_manager.add_task(self.username, task)

                self.task_manager.delete_task(self.username, self.task['name'])

                self.on_close()
            else:
                messagebox.showerror('Error', 'Please enter task name, due date and due time')
        except ValueError:
            messagebox.showerror('Error',
                                 'Invalid date or time format. Please use DD-MM-YYYY for date and HH:MM for time')

    def on_close(self):
        if self.callback:
            self.callback()
        self.root.destroy()