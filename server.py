import json
import logging
from flask import Flask, request
import gamemanager

logging.basicConfig(level=logging.WARN)

app = Flask(__name__)
app.url_map.strict_slashes = False  # Avoid automatic redirections to add slash


class WrongParameters(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(Exception, self).__init__(message)


class WrongGameId(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(Exception, self).__init__(message)


# Decorator for the endpoints. Catches exceptions and converts them
#   to proper error messages
def process_response(func):
    def func_wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            status = 200
        except WrongParameters as e:
            result = {'error': str(e)}
            status = 400
            print(e)
        except WrongGameId as e:
            result = {'error': str(e)}
            status = 404
            print(e)
        except Exception as e:
            # Don't leak information on unexpected errors
            result = {'error': 'server error'}
            status = 500
            print(e)

        res_json = json.dumps(result, ensure_ascii=False)
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        return res_json, status, headers

    return func_wrapper


@app.route("/games", endpoint='new_game', methods=['POST'])
@process_response
def new_game():
    return dict(game_id=gamemanager.new_game(4, '123456'))


@app.route("/games/<game_id>/guess", endpoint='game_guess', methods=['POST'])
@process_response
def game_guess(game_id):
    json_data = request.get_json()
    if not game_id:
        raise WrongParameters("Missing game_id parameter")
    if 'guess' not in json_data:
        raise WrongParameters("Missing guess parameter")

    try:
        [b, w] = gamemanager.check_guess(game_id, json_data['guess'])
    except IndexError as e:
        raise WrongGameId("No game with game_id=%s" % game_id)
    except ValueError as e:
        raise WrongParameters(str(e))

    return dict(b=b, w=w)


# This won't execute if using FastCGI
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int("8080"))
