import os
import tkinter as tk

from LoginApp import LoginApp

if __name__ == "__main__":

    # Creating a database catalogue
    if not os.path.exists('database'):
        os.makedirs('database')

    # Activating an app
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
    