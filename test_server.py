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

    def make_guess(self, game_id, json_data):
        rv = self.client().post(
            '/games/%s/guess' % game_id, json=json_data
            )
        # Check we got a json response
        self.assertEqual(
            rv.headers['content-type'],
            'application/json; charset=utf-8')
        return rv, json.loads(rv.data)

    def test_new_game(self):
        game_info = self.create_game()
        # res has only 'game_id' key
        self.assertEqual([*game_info], ['game_id'])
        # res['game_id'] is only made of numbers
        self.assertTrue(game_info['game_id'].isdigit())

    def test_game_guess(self):
        game_info = self.create_game()
        rv, guess_reply = self.make_guess(
            game_info['game_id'], {'guess': '1234'})
        # res has only 'b' and 'w' keys
        self.assertEqual(set([*guess_reply]), set(['b', 'w']))
        self.assertEqual(rv.status_code, 200)

    def test_game_guess_wrong_id(self):
        game_info = self.create_game()
        rv, guess_reply = self.make_guess('1', {'guess': '1234'})
        self.assertEqual([*guess_reply], ['error'])
        self.assertEqual(rv.status_code, 404)

    def test_game_guess_wrong_guess_length(self):
        game_info = self.create_game()
        rv, guess_reply = self.make_guess(
            game_info['game_id'], {'guess': '12345'})
        self.assertEqual([*guess_reply], ['error'])
        self.assertEqual(rv.status_code, 400)

    def test_game_history(self):
        GUESSES = ['1234', '1212', '3434']
        game_info = self.create_game()
        game_id = game_info['game_id']
        for guess in GUESSES:
            self.make_guess(game_id, {'guess': guess})

        rv = self.client().get('/games/%s' % game_id)
        # Check we got a json response
        self.assertEqual(
            rv.headers['content-type'],
            'application/json; charset=utf-8')
        game_info = json.loads(rv.data)

        # check returned keys
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(set([*game_info]),
                         set(['alphabet', 'length', 'historic']))
        self.assertEqual(set([*(game_info['historic'][0])]),
                         set(['ts', 'guess', 'b', 'w']))
        self.assertEqual(len(game_info['historic']), len(GUESSES))

        historic_guesses = []
        for i in range(len(GUESSES)):
            historic_guesses.append(game_info['historic'][i]['guess'])
        self.assertEqual(GUESSES, historic_guesses)


if __name__ == '__main__':
    unittest.main()
