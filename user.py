import random
class User:
    def __init__(self, name, username):
        self.name = name
        self.username = username
        self.userId = random.randint(1, 1000) * random.randint(1, 50)
