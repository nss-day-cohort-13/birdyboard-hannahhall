import unittest
from chirp import PublicMessage
from chirp import PrivateMessage


class Testchirp(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.privateChirp = PrivateMessage('sender', 'receiver', 'howdy')
        self.publicChirp = PublicMessage('sender', 'hello world')

    def test_private_chirp_creation(self):
        self.assertEqual(self.privateChirp.sender, 'sender')
        self.assertEqual(self.privateChirp.receiver, 'receiver')
        self.assertEqual(self.privateChirp.message, 'howdy')
        self.assertIsInstance(self.privateChirp.conversation, list)

    def test_private_reply(self):
        startLength = len(self.privateChirp.conversation)
        self.privateChirp.reply('sender', 'message')
        self.assertEqual(len(self.privateChirp.conversation), startLength + 1)

    def test_public_chirp_creation(self):
        self.assertEqual(self.publicChirp.sender, 'sender')
        self.assertEqual(self.publicChirp.message, 'hello world')
        self.assertIsInstance(self.privateChirp.conversation, list)

    def test_public_reply(self):
        startLength = len(self.publicChirp.conversation)
        self.publicChirp.reply('sender', 'message')
        self.assertEqual(len(self.publicChirp.conversation), startLength + 1)

if __name__ == '__main__':
    unittest.main()
