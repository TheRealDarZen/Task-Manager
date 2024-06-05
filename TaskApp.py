import tkinter as tk
from datetime import datetime, timedelta
from tkinter import messagebox
import tkinter.ttk as ttk
import threading

from TaskManager import TaskManager
from EditWindow import EditWindow


class TaskApp:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.manager = TaskManager()
        self.notificationsOn = tk.BooleanVar()
        self.create_task_ui()

        self.check_due_thread = threading.Thread(target=self.manager.check_due_tasks, args=(self.username, self.get_notifications_val,))
        self.check_due_thread.daemon = True
        self.check_due_thread.start()

        self.update_tasks_status = threading.Thread(target=self.manager.update_status, args=(self.load_tasks, ))
        self.update_tasks_status.daemon = True
        self.update_tasks_status.start()

    def create_task_ui(self):
        self.root.title(f'Task Manager - {self.username}')
        self.root.config(bg='grey')

        # Frame for task input
        task_input_frame = tk.Frame(self.root, bg='grey')
        task_input_frame.pack(padx=10, pady=10, fill='x')

        self.task_name_label = tk.Label(task_input_frame, text='Task Name:', fg='white', bg='grey')
        self.task_name_label.grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.task_entry = tk.Entry(task_input_frame, width=50, fg='white', bg='grey')
        self.task_entry.grid(row=0, column=1, padx=5, pady=5)

        self.due_date_label = tk.Label(task_input_frame, text='Date DD-MM-YYYY:', fg='white', bg='grey')
        self.due_date_label.grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.due_date_entry = tk.Entry(task_input_frame, width=50, fg='white', bg='grey')
        self.due_date_entry.grid(row=1, column=1, padx=5, pady=5)

        self.due_today_button = tk.Button(task_input_frame, text='Due Today', command=self.set_task_due_today, fg='white', bg='grey')
        self.due_today_button.grid(row=1, column=2, padx=5, pady=5)

        self.due_tomorrow_button = tk.Button(task_input_frame, text='Due Tomorrow', command=self.set_task_due_tomorrow, fg='white', bg='grey')
        self.due_tomorrow_button.grid(row=1, column=3, padx=5, pady=5)

        self.due_time_label = tk.Label(task_input_frame, text='Time HH:MM:', fg='white', bg='grey')
        self.due_time_label.grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.due_time_entry = tk.Entry(task_input_frame, width=50, fg='white', bg='grey')
        self.due_time_entry.grid(row=2, column=1, padx=5, pady=5)

        self.due_to_end_of_the_week_button = tk.Button(task_input_frame, text='Due to end of the week',
                                                       command=self.set_task_due_to_end_of_the_week, fg='white', bg='grey')
        self.due_to_end_of_the_week_button.grid(row=2, column=2, columnspan=2, padx=10, pady=5)

        self.priority_label = tk.Label(task_input_frame, text='Priority:', fg='white', bg='grey')
        self.priority_label.grid(row=3, column=0, sticky='e', padx=5, pady=5)
        self.priority_combobox = ttk.Combobox(task_input_frame, values=['Highest', 'High', 'Moderate', 'Low'], state='readonly')
        self.priority_combobox.current(2)
        self.priority_combobox.grid(row=3, column=1, padx=5, pady=5, sticky='w')

        self.add_button = tk.Button(task_input_frame, text='Add Task', command=self.add_task, padx=10, fg='white', bg='grey')
        self.add_button.grid(row=4, column=1, columnspan=1, pady=10)

        # Frame for filtering and sorting
        self.filter_sort_frame = tk.Frame(self.root, bg='grey')
        self.filter_sort_frame.pack(padx=10, fill='x')

        self.filter_by_status_label = tk.Label(self.filter_sort_frame, text='Filter by Status:', fg='white', bg='grey')
        self.filter_by_status_label.grid(row=0, column=0, padx=10, pady=10)
        self.filter_by_status_combobox = ttk.Combobox(self.filter_sort_frame, values=['All', 'Due', 'Late'], state='readonly', width=30)
        self.filter_by_status_combobox.current(0)
        self.filter_by_status_combobox.bind("<<ComboboxSelected>>", self.filter_tasks_by_status)
        self.filter_by_status_combobox.grid(row=0, column=1, padx=10, pady=10)

        self.filter_by_priority_label = tk.Label(self.filter_sort_frame, text='Filter by Priority:', fg='white', bg='grey')
        self.filter_by_priority_label.grid(row=1, column=0, padx=10, pady=10)
        self.filter_by_priority_combobox = ttk.Combobox(self.filter_sort_frame,
                                                        values=['All', 'Highest', 'High/Highest', 'Moderate/High/Highest'], state='readonly', width=30)
        self.filter_by_priority_combobox.current(0)
        self.filter_by_priority_combobox.bind("<<ComboboxSelected>>", self.filter_tasks_by_priority)
        self.filter_by_priority_combobox.grid(row=1, column=1, padx=10, pady=10)

        self.sort_label = tk.Label(self.filter_sort_frame, text='Sort By:', fg='white', bg='grey')
        self.sort_label.grid(row=2, column=0, padx=10, pady=10, sticky='e')
        self.sort_combobox = ttk.Combobox(self.filter_sort_frame, values=['Date', 'Name', 'Status', 'Priority'],
                                          state='readonly', width=30)
        self.sort_combobox.current(0)
        self.sort_combobox.bind("<<ComboboxSelected>>", self.sort_tasks)
        self.sort_combobox.grid(row=2, column=1, padx=10, pady=10)

        # Frame for pending tasks
        pending_tasks_frame = tk.Frame(self.root, bg='grey')
        pending_tasks_frame.pack(padx=10, pady=10, fill='x')

        self.pending_tasks_label = tk.Label(pending_tasks_frame, text='Pending Tasks:', fg='white', bg='grey', font=('DejaVu Sans', 12, 'bold'))
        self.pending_tasks_label.pack()
        self.task_listbox = tk.Listbox(pending_tasks_frame, height=15, width=100, fg='white', bg='grey')
        self.task_listbox.pack(pady=5)

        self.complete_button = tk.Button(pending_tasks_frame, text='Mark as Completed', command=self.complete_task, padx=10, fg='white', bg='grey')
        self.complete_button.pack(pady=5)

        self.edit_task_button = tk.Button(pending_tasks_frame, text='Edit Task', command=self.edit_task, padx=10, fg='white', bg='grey')
        self.edit_task_button.pack(pady=5)

        self.delete_task_button = tk.Button(pending_tasks_frame, text='Delete Task', command=self.delete_task,
                                            padx=10, fg='white', bg='grey')
        self.delete_task_button.pack(pady=5)

        # Frame for completed tasks
        completed_tasks_frame = tk.Frame(self.root, bg='grey')
        completed_tasks_frame.pack(padx=10, pady=10, fill='x')

        self.completed_tasks_label = tk.Label(completed_tasks_frame, text='Completed Tasks:', fg='white', bg='grey', font=('DejaVu Sans', 12, 'bold'))
        self.completed_tasks_label.pack()
        self.completed_listbox = tk.Listbox(completed_tasks_frame, width=100, fg='white', bg='grey')
        self.completed_listbox.pack(pady=5)

        # Frame for clearing all tasks and stats
        clear_tasks_buttons_frame = tk.Frame(self.root, bg='grey')
        clear_tasks_buttons_frame.pack(padx=10, pady=10, fill='x')

        self.clear_all_pending_button = tk.Button(clear_tasks_buttons_frame, text='Clear All Pending Tasks',
                                                  command=self.clear_all_pending_tasks, padx=20, fg='white', bg='grey')
        self.clear_all_pending_button.grid(row=0, column=0, pady=5, sticky='w')

        self.clear_all_completed_button = tk.Button(clear_tasks_buttons_frame, text='Clear All Completed Tasks',
                                                    command=self.clear_all_completed_tasks, padx=20, fg='white', bg='grey')
        self.clear_all_completed_button.grid(row=0, column=1, pady=5, sticky='w')

        # Adding empty columns to create space between left and right buttons
        clear_tasks_buttons_frame.grid_columnconfigure(2, weight=1)

        self.stats_button = tk.Button(clear_tasks_buttons_frame, text='Show Stats', command=self.show_stats, padx=10, fg='white', bg='grey')
        self.stats_button.grid(row=0, column=3, pady=5, sticky='e')

        # Ensure that columns are stretched to fill the space
        clear_tasks_buttons_frame.grid_columnconfigure(0, weight=0)
        clear_tasks_buttons_frame.grid_columnconfigure(1, weight=0)
        clear_tasks_buttons_frame.grid_columnconfigure(3, weight=0)

        self.notification_checkbox = tk.Checkbutton(self.root, text="Enable Notifications", variable=self.notificationsOn,
                                       onvalue=True, offvalue=False)
        self.notification_checkbox.pack(anchor=tk.SW)

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

    def edit_task(self):
        selected_task = self.task_listbox.get(tk.ACTIVE)
        if selected_task:
            tasks = self.manager.get_tasks(self.username)
            for task in tasks:
                if task['name'] == selected_task.split(' - ')[0]:
                    self.edit_window = tk.Toplevel(self.root)
                    EditWindow(self.edit_window, task, self.username, self.load_tasks)
                    break

    def load_tasks(self):
        self.task_listbox.delete(0, tk.END)
        tasks = self.manager.get_tasks(self.username)
        filter_by_status = self.filter_by_status_combobox.get()
        filter_by_priority = self.filter_by_priority_combobox.get()
        sort_by = self.sort_combobox.get()

        # Filtering
        if filter_by_status == 'Due':
            tasks = [task for task in tasks if task['status'] == 'Pending']
        elif filter_by_status == 'Late':
            tasks = [task for task in tasks if task['status'] == 'Pending, Late']

        if filter_by_priority == 'Highest':
            tasks = [task for task in tasks if task['priority'] == 'Highest']
        elif filter_by_priority == 'High/Highest':
            tasks = [task for task in tasks if task['priority'] == 'Highest' or task['priority'] == 'High']
        elif filter_by_priority == 'Moderate/High/Highest':
            tasks = [task for task in tasks if task['priority'] == 'Highest' or task['priority'] == 'High' or task['priority'] == 'Moderate']

        # Sorting
        if sort_by == 'Name':
            tasks.sort(key=lambda x: x['name'])
        elif sort_by == 'Status':
            tasks.sort(key=lambda x: x['status'])
        elif sort_by == 'Priority':
            priority_order = {'Highest': 1, 'High': 2, 'Moderate': 3, 'Low': 4}
            tasks.sort(key=lambda x: priority_order[x['priority']])
        else:
            tasks.sort(key=lambda x: (x['due_date'], x['due_time']))

        for task in tasks:
            self.task_listbox.insert(tk.END, f"{task['name']} - {task['due_date']} {task['due_time']} - {task['priority']} - {task['status']}")

        self.completed_listbox.delete(0, tk.END)
        completed_tasks = self.manager.get_completed_tasks_with_time(self.username)
        for task in completed_tasks:
            self.completed_listbox.insert(tk.END, f"{task['name']} - Due to {task['due_date']} {task['due_time']} - Completed at {task['completed_at']} "
                                                  f"{('(Late)' if task['status'] == 'Completed, Late' else '')} - {task['priority']}")

    def filter_tasks_by_status(self, event=None):
        self.load_tasks()

    def filter_tasks_by_priority(self, event=None):
        self.load_tasks()

    def sort_tasks(self, event=None):
        self.load_tasks()

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

    def delete_task(self):
        selected_task = self.task_listbox.get(tk.ACTIVE)
        if selected_task:
            task_name = selected_task.split(' - ')[0]
            self.manager.delete_task(self.username, task_name)
            self.load_tasks()
        else:
            selected_task = self.completed_listbox.get(tk.ACTIVE)
            if selected_task:
                task_name = selected_task.split(' - ')[0]
                self.manager.delete_task(self.username, task_name, completed=True)
                self.load_tasks()

    def clear_all_pending_tasks(self):
        if messagebox.askyesno('Confirm', 'Are you sure you want to clear all pending tasks?'):
            self.manager.delete_all_tasks(self.username)
            self.load_tasks()

    def clear_all_completed_tasks(self):
        if messagebox.askyesno('Confirm', 'Are you sure you want to clear all completed tasks?'):
            self.manager.delete_all_completed_tasks(self.username)
            self.show_completed_tasks()

    def get_notifications_val(self):
        return self.notificationsOn.get()

    def set_task_due_today(self):
        self.due_date_entry.delete(0, tk.END)
        self.due_time_entry.delete(0, tk.END)
        self.due_date_entry.insert(0, datetime.today().strftime('%d-%m-%Y'))
        self.due_time_entry.insert(0, '23:59')

    def set_task_due_tomorrow(self):
        self.due_date_entry.delete(0, tk.END)
        self.due_time_entry.delete(0, tk.END)
        self.due_date_entry.insert(0, (datetime.today() + timedelta(days=1)).strftime('%d-%m-%Y'))
        self.due_time_entry.insert(0, '23:59')

    def set_task_due_to_end_of_the_week(self):
        self.due_date_entry.delete(0, tk.END)
        self.due_time_entry.delete(0, tk.END)
        self.due_date_entry.insert(0, (datetime.today() + timedelta(days=(6-datetime.today().weekday()))).strftime('%d-%m-%Y'))
        self.due_time_entry.insert(0, '23:59')

    def show_stats(self):
        stats_window = tk.Toplevel(self.root)
        stats_window.title('Task Statistics')
        stats_window.geometry('300x150')

        total_tasks, completed_tasks, completed_on_time_tasks, pending_tasks, completed_late_tasks, pending_late_tasks = (
            self.manager.get_stats(self.username))

        tk.Label(stats_window, text=f'Total Tasks: {total_tasks}').pack()
        tk.Label(stats_window, text=f'Pending Tasks: {pending_tasks}').pack()
        tk.Label(stats_window, text=f'Pending late Tasks: {pending_late_tasks}').pack()
        tk.Label(stats_window, text=f'Completed Tasks: {completed_tasks}').pack()
        tk.Label(stats_window, text=f'Completed on time Tasks: {completed_on_time_tasks} '
                                    f'({round((completed_on_time_tasks*100/completed_tasks), 1) if completed_tasks > 0 else 0.0}%)').pack()
        tk.Label(stats_window, text=f'Completed late Tasks: {completed_late_tasks}').pack()
