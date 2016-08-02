import random
import pickle

class Birdyboard():
    def __init__(self):
        self.currentUser = None
        self.privateRecip = None
        self.userPrivateChirps = dict()
        try:
            self.deserializeChirps('test_board.txt')
        except EOFError:
            self.chirps = dict()
            self.chirps['private'] = dict()
            self.chirps['public'] = dict()
        try:
            self.deserializeUsers('test_users.txt')
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
            recipient = input('Choose who to send private chirp to: \n> ')
            message = input('Enter Chirp: \n> ')
            self.newPrivateChirp(message, recipient)
            self.menu()
        elif choice == '6':
            exit()

    def printAllUsers(self):
        print(self.users)
        userLength = len(self.users)
        counter = 1
        index = 0
        while userLength:
            print(str(counter) + '. ' + self.users[index][1])
            counter += 1
            index += 1
            userLength -= 1

    def newUser(self, name, username):
        self.users.append((name, username))
        self.serializeUsers('test_users.txt')

    def selectUser(self, choice):
        index = choice - 1
        if not self.currentUser:
            self.currentUser = self.users[index]
            return self.currentUser
        else:
            self.privateRecip = self.users[index]
            return self.privateRecip

    def newPublicChirp(self, message):
        key = random.randint(1, 1000)
        self.chirps['public'][key] = []
        self.chirps['public'][key].append({self.currentUser[1]: message})
        self.serializeMessages('test_board.txt')

    def newPrivateChirp(self, message, recipient):
        key = random.randint(1, 1000)
        self.chirps['private'][key] = []
        self.chirps['private'][key].append([self.currentUser, self.privateRecip])
        self.chirps['private'][key].append({self.currentUser[1]: message})
        self.serializeMessages('test_board.txt')


    def showAllChirps(self):
        self.findPrivateChirps()
        privateLength = len(self.chirps['private'])
        publicLength = len(self.chirps['public'])
        print('<<<<<Private Chirps>>>>>')
        counter = 1
        for key, value in self.userPrivateChirps.items():
            message = ''.join("{!s}: {!r}".format(key,val) for (key,val) in value[-1].items())
            print(str(counter) + '. ' + message)
            counter += 1
        print('<<<<<Public Chirps>>>>>')
        for key, value in self.chirps['public'].items():
            message = ''.join("{!s}: {!r}".format(key,val) for (key,val) in value[0].items())
            print(str(counter) + '. ' + message)
            counter += 1
        print(str(counter) + '. ' + 'Main Menu')


    def findPrivateChirps(self):
        for key, value in self.chirps['private'].items():
            for info in value[0]:
                if info == self.currentUser:
                    self.userPrivateChirps[key] = value

if __name__ == '__main__':
    board = Birdyboard()
    board.menu()
