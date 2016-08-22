import unittest
from board import Birdyboard


class Testboard(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.board = Birdyboard('txt_files/test_board.txt', 'txt_files/test_users.txt')
        self.board.newUser('name', 'username')
        self.board.newUser('gary', 'gary101')
        self.board.newUser('larry', 'larry101')

    def test_new_user(self):
        length_of_users = len(self.board.users)
        self.assertEqual(3, length_of_users)

    def test_select_user(self):
        self.board.selectUser(1)
        self.assertEqual(self.board.currentUser.username, 'username')

    def test_select_private_recipient(self):
        self.board.selectRecipient(2)
        self.assertEqual(self.board.privateRecip.username, 'gary101')

    def test_new_public_chirp(self):
        # must select user before creating chirp
        self.board.selectUser(2)
        newchirp = "Hello World"
        startLength = len(self.board.chirps['public'])
        self.board.newPublicChirp(newchirp)
        self.assertEqual(startLength + 1, len(self.board.chirps['public']))

    def test_new_private_chirp(self):
        # must select user before creating chirp
        self.board.selectUser(1)
        recipient = self.board.selectRecipient(2)
        newchirp = "Hello gary!"
        startLength = len(self.board.chirps['private'])
        self.board.newPrivateChirp(newchirp, recipient)
        self.assertEqual(startLength + 1, len(self.board.chirps['private']))

    def test_private_chirp_list_user_that_should_have_none(self):
        self.board.selectUser(3)
        self.board.findPrivateChirps()
        self.assertEqual(0, len(self.board.userPrivateChirps))

    def test_private_chirp_list_user_that_should_have_private_chirps(self):
        self.board.selectUser(2)
        self.board.findPrivateChirps()
        self.assertTrue(self.board.userPrivateChirps)

    def test_reply_chooses_correct_message(self):
        self.board.selectUser(2)
        updatedChirp = None
        replyTo = self.board.getListofChirps()[0]
        # use for in loop to find the value that matches the reply to chirp
        for key, value in self.board.chirps['private'].items():
            if value == replyTo:
                updatedChirp = value
        self.assertEqual(updatedChirp, replyTo)

if __name__ == '__main__':
    unittest.main()
