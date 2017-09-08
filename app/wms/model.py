from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, _id):
        self.id = _id
        self.name = "Lol"
