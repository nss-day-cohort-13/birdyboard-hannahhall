import random

class Birdyboard():
    def __init__(self):
        self.users = list()
        self.currentUser = None
        self.publicChirps = list()
        self.privateChirps = dict()
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
            printAllUsers()
            userChoice = input('Select User \n> ')
            self.selectUser(int(userChoice))
            self.menu()
        elif choice == '4':
            chirp = input('Create new public chirp: \n> ')
            self.newPublicChirp(message)
        elif choice == '5':
            printAllUsers()
            recipient = input('Choose who to send private chirp to: \n> ')
            message = input('Enter Chirp: \n> ')
            self.newPrivateChirp(message, recipient)
        elif choice == '6':
            exit()

    def printAllUsers():
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

    def selectUser(self, choice):
        index = choice - 1
        if not self.currentUser:
            self.currentUser = self.users[index]
            return self.currentUser
        else:
            self.privateRecip = self.users[index]
            return self.privateRecip

    def newPublicChirp(self, message):
        self.publicChirps.append({self.currentUser[1]: message})

    def newPrivateChirp(self, message, recipient):
        key = random.randint(1, 1000)
        self.privateChirps[key] = []
        self.privateChirps[key].append({key, self.currentUser[1], recipient[1]})        
        self.privateChirps[key].append((self.currentUser[1], message))

if __name__ == '__main__':
    board = Birdyboard()
    board.menu()
