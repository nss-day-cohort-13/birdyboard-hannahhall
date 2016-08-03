import unittest
from board import *

class Testboard(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.board = Birdyboard('test_board.txt', 'test_users.txt')

    def test_new_user(self):
        self.board.newUser('name', 'username')
        self.board.newUser('gary', 'gary101')
        length_of_users = len(self.board.users)
        self.assertEqual(2, length_of_users)

    def test_select_user(self):
        input = 1
        self.board.selectUser(input)
        self.assertEqual(self.board.currentUser.username, 'username')

    def test_new_public_chirp(self):
        self.board.selectUser(1)
        newchirp = "Hello World"
        startLength = len(self.board.chirps['public'])
        self.board.newPublicChirp(newchirp)
        self.assertEqual(startLength + 1, len(self.board.chirps['public']))

    def test_new_private_chirp(self):
        # creating current user
        self.board.selectUser(1)
        # choosing recipient of message
        recipient = self.board.selectUser(2)
        newchirp = "Hello gary!"
        startLength = len(self.board.chirps['private'])
        self.board.newPrivateChirp(newchirp, recipient)
        self.assertEqual(startLength + 1, len(self.board.chirps['private']))

    def test_chirp_list_view(self):
        self.board.selectUser(1)





if __name__ == '__main__':
	unittest.main()
