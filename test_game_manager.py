import unittest, re
from game_manager import new_game

class TestGameManager(unittest.TestCase):
    def test_new_game(self):
        id = new_game(5, "abcd")
        self.assertIsInstance(id, str)
    
if __name__ == '__main__':
    unittest.main()