import unittest, re
from gamemanager import new_game, get_game, check_guess

class TestGameManager(unittest.TestCase):
    def test_new_game(self):
        id = new_game(5, "abcd")
        self.assertIsInstance(id, str)

    def test_check_guess(self):
        game_id = new_game(5, "abcd")
        game_info = get_game(game_id)
        b, w = check_guess(game_id, game_info['code'])
        self.assertEqual(b, 5)
        self.assertEqual(w, 0)
    
if __name__ == '__main__':
    unittest.main()