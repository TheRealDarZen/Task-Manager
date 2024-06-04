import tkinter as tk
from tkinter import messagebox

from TaskManager import TaskManager
from UserManager import UserManager

from TaskApp import TaskApp

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.user_manager = UserManager()
        self.task_manager = TaskManager()
        self.create_login_ui()
        self.root.geometry('300x130')

    def create_login_ui(self):
        self.root.title('Task Manager - Login')

        self.username_label = tk.Label(self.root, text='Username')
        self.username_label.pack()
        self.username_entry = tk.Entry(self.root, width=30)
        self.username_entry.pack()

        self.password_label = tk.Label(self.root, text='Password')
        self.password_label.pack()
        self.password_entry = tk.Entry(self.root, show='*', width=30)
        self.password_entry.pack()

        # Frame for login, register and delete buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(padx=10, pady=10, fill='x')

        self.login_button = tk.Button(self.button_frame, text='Login', command=self.login, padx=15)
        self.login_button.grid(row=0, column=0, columnspan=2, pady=5)

        self.register_button = tk.Button(self.button_frame, text='Register', command=self.register, padx=15)
        self.register_button.grid(row=0, column=2, columnspan=2, pady=5)

        self.delete_button = tk.Button(self.button_frame, text="Delete Account", command=self.delete_account, padx=15)
        self.delete_button.grid(row=0, column=4, columnspan=2, pady=5)

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

    def delete_account(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.user_manager.validate_user(username, password):
            if messagebox.askyesno("Delete Account", "Are you sure you want to delete this account?"):
                self.user_manager.delete_user(username)
                messagebox.showinfo("Success", "Account deleted successfully")
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def open_task_manager(self, username):
        self.root.withdraw()
        self.task_manager_app = tk.Toplevel(self.root)
        self.task_manager_app.protocol("WM_DELETE_WINDOW", self.on_task_manager_close)
        TaskApp(self.task_manager_app, username)

    def on_task_manager_close(self):
        self.task_manager_app.destroy()
        self.root.deiconify()
        self.clear()

    def clear(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
