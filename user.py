import uuid


class User:
    def __init__(self, name, username):
        self.name = name
        self.username = username
        self.userId = uuid.uuid4()
