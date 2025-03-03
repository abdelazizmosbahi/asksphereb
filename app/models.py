from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, _id, username, password):
        self._id = _id
        self.username = username
        self.password = password

    def get_id(self):
        return str(self._id)