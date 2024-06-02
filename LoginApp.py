import tkinter as tk
from tkinter import messagebox

from TaskManager import TaskManager
from UserManager import UserManager

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.user_manager = UserManager()
        self.task_manager = TaskManager()
        self.create_login_ui()

    def create_login_ui(self):
        self.root.title('Task Manager - Login')

        self.username_label = tk.Label(self.root, text='Username')
        self.username_label.pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        self.password_label = tk.Label(self.root, text='Password')
        self.password_label.pack()
        self.password_entry = tk.Entry(self.root, show='*')
        self.password_entry.pack()

        self.login_button = tk.Button(self.root, text='Login', command=self.login)
        self.login_button.pack()

        self.register_button = tk.Button(self.root, text='Register', command=self.register)
        self.register_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.user_manager.validate_user(username, password):
            self.open_task_manager(username)
        else:
            messagebox.showerror('Error', 'Invalid username or password')

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.user_manager.create_user(username, password):
            messagebox.showinfo('Success', 'User registered successfully')
        else:
            messagebox.showerror('Error', 'Username already exists')

    def open_task_manager(self, username):
        self.root.withdraw()
        self.task_manager_app = tk.Toplevel(self.root)
        self.task_manager_app.protocol("WM_DELETE_WINDOW", self.root.quit)
        TaskApp(self.task_manager_app, username)
