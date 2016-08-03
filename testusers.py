import unittest
from user import *

class Testuser(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.gary = User('gary', 'gary101')

    def test_user_creation(self):
        self.assertEqual(self.gary.name, 'gary')
        self.assertEqual(self.gary.username, 'gary101')
        self.assertTrue(self.gary.userId)




if __name__ == '__main__':
	unittest.main()
