import random
class PrivateMessage:
    def __init__(self, user, receiver, message):
        self.sender = user
        self.receiver = receiver
        self.message = message
        self.conversation = []

    def reply(self, sender, message):
        self.conversation.append({sender: message})

class PublicMessage:
    def __init__(self, user, message):
        self.user = user
        self.message = message
        self.conversation = []

    def reply(self, user, message):
        self.conversation.append({user: message})
        
