class Birdyboard():
    def __init__(self):
        self.users = list()
        self.currentUser = None
        self.publicChirps = list()

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
            userLength = len(self.users)
            counter = 1
            index = 0
            while userLength:
                print(str(counter) + '. ' + self.users[index][1])
                counter += 1
                index += 1
                userLength -= 1
            userChoice = input('Select User \n> ')
            self.selectUser(int(userChoice))
            self.menu()
        elif choice == '6':
            exit()

    def newUser(self, name, username):
        self.users.append((name, username))

    def selectUser(self, choice):
        index = choice - 1
        self.currentUser = self.users[index]
        return self.currentUser

    def newPublicChirp(self, message):
        self.publicChirps.append({self.currentUser[1]: message})

# board = Birdyboard()
# board.menu()
