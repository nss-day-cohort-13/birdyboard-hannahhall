import unittest
from board import *

class Testboard(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.board = Birdyboard()
        self.board.newUser('name', 'username')
        self.board.newUser('gary', 'gary101')

    def test_new_user(self):
        self.assertIn(('name', 'username'), self.board.users)

    def test_select_user(self):
        input = 1
        self.board.selectUser(input)
        self.assertEqual(self.board.currentUser, ('name', 'username'))

    def test_new_public_chirp(self):
        self.board.selectUser(1)
        newchirp = "Hello World"
        self.board.newPublicChirp(newchirp)
        for key, value in self.board.chirps['public'].items():
            self.assertIn({'username': 'Hello World'}, value)

    def test_new_private_chirp(self):
        # creating current user
        self.board.selectUser(1)
        # choosing recipient of message
        self.board.selectUser(2)
        newChirp = "Hello gary!"
        self.board.newPrivateChirp(newChirp, self.board.privateRecip)
        for key, value in self.board.chirps['private'].items():
            self.assertEqual([{'username', 'gary101', key}, ('username', 'Hello gary!')], value)

    def test_chirp_list_view(self):
        self.board.selectUser(1)





if __name__ == '__main__':
	unittest.main()
