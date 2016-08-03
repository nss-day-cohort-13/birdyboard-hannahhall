import random
import pickle
from user import *
from chirp import *

class Birdyboard:
    def __init__(self, boardfile, userfile):
        self.currentUser = None
        self.privateRecip = None
        self.userPrivateChirps = dict()
        self.boardfile = boardfile
        self.userfile = userfile
        try:
            self.deserializeChirps(boardfile)
        except EOFError:
            self.chirps = dict()
            self.chirps['private'] = dict()
            self.chirps['public'] = dict()
        try:
            self.deserializeUsers(userfile)
        except EOFError:
            self.users = list()

    def deserializeChirps(self, filename):
        try:
            with open(filename, 'rb+') as f:
                self.chirps = pickle.load(f)
        except FileNotFoundError:
            self.chirps = dict()
            self.chirps['private'] = dict()
            self.chirps['public'] = dict()
        return self.chirps

    def deserializeUsers(self, filename):
        try:
            with open(filename, 'rb+') as f:
                self.users = pickle.load(f)
        except FileNotFoundError:
            self.users = list()
        return self.users

    def serializeUsers(self, filename):
        with open(filename, 'wb+') as f:
            pickle.dump(self.users, f)

    def serializeMessages(self, filename):
        with open(filename, 'wb+') as f:
            pickle.dump(self.chirps, f)

    def menu(self):
        print("""
<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>
<<<         <<<Birdyboard>>>         >>>
<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>
1. New User Account
2. Select User
3. View Chirps
4. New Public Chirp
5. New Private Chirp
6. Exit
        """)
        choice = input('> ')
        if choice == '1':
            name = input("Enter Full Name: \n> ")
            username = input("Enter User Name: \n> ")
            self.newUser(name, username)
            self.menu()
        elif choice == '2':
            self.printAllUsers()
            userChoice = input('Select User \n> ')
            self.selectUser(int(userChoice))
            self.menu()
        elif choice == '3':
            self.showAllChirps()
        elif choice == '4':
            chirp = input('Create new public chirp: \n> ')
            self.newPublicChirp(chirp)
            self.menu()
        elif choice == '5':
            self.printAllUsers()
            userchoice = input('Choose who to send private chirp to: \n> ')
            recipient = self.selectUser(int(userchoice))
            message = input('Enter Chirp: \n> ')
            self.newPrivateChirp(message, recipient)
            self.menu()
        elif choice == '6':
            exit()

    def printAllUsers(self):
        print(self.users)
        userLength = len(self.users)
        counter = 1
        for user in self.users:
            print(str(counter) + '. ' + user.username)
            counter += 1

    def newUser(self, name, username):
        existingUsers = []
        for user in self.users:
            existingUsers.append(user.username)
        if not username in existingUsers:
            user = User(name, username)
            self.users.append(user)
            self.serializeUsers(self.userfile)

    def selectUser(self, choice):
        index = choice - 1
        if not self.currentUser:
            self.currentUser = self.users[index]
            print(self.currentUser.username)
            return self.currentUser
        else:
            self.privateRecip = self.users[index]
            print(self.privateRecip.username)
            return self.privateRecip

    def newPublicChirp(self, message):
        key = random.randint(1, 1000)
        self.chirps['public'][key] = PublicMessage(self.currentUser.username, message)
        self.serializeMessages(self.boardfile)

    def newPrivateChirp(self, message, recipient):
        key = random.randint(1, 1000)
        self.chirps['private'][key] = PrivateMessage(self.currentUser.username, self.privateRecip.username, message)
        self.serializeMessages(self.boardfile)


    def showAllChirps(self):
        self.findPrivateChirps()
        print('<<<<<Private Chirps>>>>>')
        counter = 1
        for key, value in self.userPrivateChirps.items():
            print(str(counter) + '. ' + value.sender + ': ' + value.message)
            counter += 1
        print('<<<<<Public Chirps>>>>>')
        for key, value in self.chirps['public'].items():
            print(str(counter) + '. ' + value.sender + ': ' + value.message)
            counter += 1
        print(str(counter) + '. ' + 'Main Menu')


    def findPrivateChirps(self):
        for key, value in self.chirps['private'].items():
            if self.currentUser.username == value.sender or value.receiver:
                self.userPrivateChirps[key] = value

if __name__ == '__main__':
    board = Birdyboard('board.txt', 'users.txt')
    board.menu()
