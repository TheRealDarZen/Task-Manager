import os

from TaskManager import TaskManager
from UserManager import UserManager

if __name__ == "__main__":

    # Creating a database catalogue
    if not os.path.exists('database'):
        os.makedirs('database')
