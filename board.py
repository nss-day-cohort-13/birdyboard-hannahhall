import uuid
import pickle
import os
import sys
from user import *
from chirp import *

class Birdyboard:
    def __init__(self, boardfile, userfile):
        """
        On class creation this function opens corrisponding files and loads the data to chosen variables
        """
        self.currentUser = None
        self.privateRecip = None
        self.userPrivateChirps = {}
        self.boardfile = boardfile
        self.userfile = userfile
        self.listofChirps = []
        self.clearScreen()
        try:
            self.deserializeChirps(boardfile)
        except EOFError:
            self.chirps = {}
            self.chirps['private'] = {}
            self.chirps['public'] = {}
        try:
            self.deserializeUsers(userfile)
        except EOFError:
            self.users = []

    def deserializeChirps(self, filename):
        """Deserialize chirp file"""
        try:
            with open(filename, 'rb+') as f:
                self.chirps = pickle.load(f)
        except FileNotFoundError:
            self.chirps = {}
            self.chirps['private'] = {}
            self.chirps['public'] = {}
        return self.chirps

    def deserializeUsers(self, filename):
        """Deserialize user file"""
        try:
            with open(filename, 'rb+') as f:
                self.users = pickle.load(f)
        except FileNotFoundError:
            self.users = []
        return self.users

    def serializeUsers(self, filename):
        """Serialize user file"""
        with open(filename, 'wb+') as f:
            pickle.dump(self.users, f)

    def serializeMessages(self, filename):
        """Serialize chirp file"""
        with open(filename, 'wb+') as f:
            pickle.dump(self.chirps, f)

    def menu(self):
        """Function to show the main menu with 6 options"""

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
            self.clearScreen()
            name = input("Enter Full Name: \n> ")
            username = input("Enter User Name: \n> ")
            self.newUser(name, username)
            self.clearScreen()
            self.menu()
        elif choice == '2':
            self.clearScreen()
            self.printAllUsers()
            userChoice = input('Select User \n> ')
            self.selectUser(int(userChoice))
            self.clearScreen()
            self.menu()
        elif choice == '3':
            if not self.currentUser:
                self.checkForUser()
            else:
                self.clearScreen()
                self.chirpMenu()
        elif choice == '4':
            if not self.currentUser:
                self.checkForUser()
            else:
                self.clearScreen()
                chirp = input('Create new public chirp: \n> ')
                self.newPublicChirp(chirp)
                self.clearScreen()
                self.chirpMenu()
        elif choice == '5':
            if not self.currentUser:
                self.checkForUser()
            else:
                self.clearScreen()
                self.printAllUsers()
                userchoice = input('Choose who to send private chirp to: \n> ')
                recipient = self.selectRecipient(int(userchoice))
                message = input('Enter Chirp: \n> ')
                self.newPrivateChirp(message, recipient)
                self.clearScreen()
                self.chirpMenu()
        elif choice == '6':
            sys.exit()
        else:
            self.clearScreen()
            print('Please enter a number that corrisponds to an item')
            self.menu()

    def printAllUsers(self):
        """Prints a list of users"""
        userLength = len(self.users)
        counter = 1
        for user in self.users:
            print(str(counter) + '. ' + user.username)
            counter += 1

    def newUser(self, name, username):
        """Creates a new user and stores it in file and as currentUser"""
        existingUsers = []
        for user in self.users:
            existingUsers.append(user.username)
        if not username in existingUsers:
            user = User(name, username)
            self.users.append(user)
            self.currentUser = user
            self.serializeUsers(self.userfile)

    def selectUser(self, choice):
        """Selects a user to post chirps as"""
        index = choice - 1
        self.currentUser = self.users[index]
        return self.currentUser

    def selectRecipient(self, choice):
        """Selects recipient of private chirps"""
        index = choice - 1
        self.privateRecip = self.users[index]
        return self.privateRecip

    def newPublicChirp(self, message):
        """Creates a new public chirp and adds it to the board file"""
        key = uuid.uuid4()
        self.chirps['public'][key] = PublicMessage(self.currentUser.username, message)
        self.serializeMessages(self.boardfile)

    def newPrivateChirp(self, message, recipient):
        """Creates a new private chirp and adds it to the board file"""
        key = uuid.uuid4()
        self.chirps['private'][key] = PrivateMessage(self.currentUser.username, self.privateRecip.username, message)
        self.serializeMessages(self.boardfile)

    def chirpMenu(self):
        """Menu that lists all of a users private and public chirps"""
        self.findPrivateChirps()
        print('<<<<<Private Chirps>>>>>')
        counter = 1
        try:
            for key, value in self.userPrivateChirps.items():
                print(str(counter) + '. ' + value.sender + ': ' + value.message)
                counter += 1
        except AttributeError:
            pass
        print('<<<<<Public Chirps>>>>>')
        for key, value in self.chirps['public'].items():
            print(str(counter) + '. ' + value.sender + ': ' + value.message)
            counter += 1
        print(str(counter) + '. ' + 'Main Menu')
        userchoice = input('Choose chirp to reply \n> ')
        if userchoice == str(counter):
            self.clearScreen()
            self.menu()
        else:
            self.getListofChirps()
            message = self.listofChirps[int(userchoice) - 1]
            self.clearScreen()
            self.replyMenu(message)

    def getListofChirps(self):
        """
        Appends to a list all of a users private and public chirps.
        Used to find the corresponding chirp in self.chirps
        """
        self.findPrivateChirps()
        try:
            for key, value in self.userPrivateChirps.items():
                self.listofChirps.append(value)
        except AttributeError:
            pass
        try:
            for key, value in self.chirps['public'].items():
                self.listofChirps.append(value)
        except AttributeError:
            pass
        return self.listofChirps


    def findPrivateChirps(self):
        """Find current users private chirps"""
        for key, value in self.chirps['private'].items():
            if (self.currentUser.username == value.sender) or (self.currentUser.username == value.receiver):
                self.userPrivateChirps[key] = value
                return self.userPrivateChirps
            else:
                self.userPrivateChirps = dict()
                return self.userPrivateChirps

    def printConversation(self, message):
        """Print's an individual chirp's reply's"""
        print(message.sender + ': ' + message.message)
        for reply in message.conversation:
            for key in reply:
                print(key + ': ' + reply[key])

    def replyMenu(self, conversation):
        """Prompts the user to either reply to message or go back to chirp menu"""
        self.clearScreen()
        self.printConversation(conversation)
        userchoice = input('1. Reply \n2. Go Back \n> ')
        if userchoice == '1':
            self.clearScreen()
            newReply = input('Enter Reply \n> ')
            self.reply(newReply, conversation)
            self.clearScreen()
            self.replyMenu(conversation)
        elif userchoice == '2':
            self.clearScreen()
            self.chirpMenu()

    def reply(self, reply, conversation):
        """Searches for chosen message in message file and appends a reply to its conversation list"""
        for key, value in self.chirps['public'].items():
            if value == conversation:
                value.reply(self.currentUser.username, reply)
                self.serializeMessages(self.boardfile)
        for key, value in self.chirps['private'].items():
            if value == conversation:
                value.reply(self.currentUser.username, reply)
                self.serializeMessages(self.boardfile)

    def clearScreen(self):
        """Clears cli of clutter"""
        os.system('clear')

    def checkForUser(self):
        """Checks to make sure user has chosen a current user before reading or creating chirps"""
        self.clearScreen()
        print("Please select or create a new user before continuing")
        self.menu()


if __name__ == '__main__':
    board = Birdyboard('txt_files/board.txt', 'txt_files/users.txt')
    board.menu()
