import os
import re
import unittest
import json

from server import app


class TestServer(unittest.TestCase):
    def client(self):
        app.config['TESTING'] = True
        return app.test_client()

    def create_game(self):
        rv = self.client().post('/games')
        # Check we got a json response
        self.assertEqual(
            rv.headers['content-type'],
            'application/json; charset=utf-8')
        return json.loads(rv.data)

    def test_new_game(self):
        game_info = self.create_game()
        # res has only 'game_id' key
        self.assertEqual([*game_info], ['game_id'])
        # res['game_id'] is only made of numbers
        self.assertTrue(game_info['game_id'].isdigit())


if __name__ == '__main__':
    unittest.main()
