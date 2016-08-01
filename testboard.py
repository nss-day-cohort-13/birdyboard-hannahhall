import unittest
from board import *

class Testboard(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.board = Birdyboard()
        self.board.newUser('name', 'username')

    def test_new_user(self):
        self.assertIn(('name', 'username'), self.board.users)
    def test_select_user(self):
        input = 1
        self.board.selectUser(input)
        self.assertEqual(self.board.currentUser, ('name', 'username'))

    def test_new_public_chirp(self):
        self.board.selectUser(1)
        print(self.board.currentUser)
        newMessage = "Hello World"
        self.board.newPublicChirp(newMessage)
        self.assertIn({'username': 'Hello World'}, self.board.publicChirps)




if __name__ == '__main__':
	unittest.main()
