import hashlib
import shelve


class UserManager:
    def __init__(self, db_name='database/users.db'):
        self.db_name = db_name

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def create_user(self, username, password):
        with shelve.open(self.db_name) as db:
            if username in db:
                return False
            db[username] = self.hash_password(password)
        return True

    def validate_user(self, username, password):
        with shelve.open(self.db_name) as db:
            if username in db and db[username] == self.hash_password(password):
                return True
        return False

    def delete_user(self, username):
        with shelve.open(self.db_name, writeback=True) as db:
            if username in db:
                del db[username]
