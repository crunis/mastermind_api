import json
import logging
from flask import Flask, request
import gamemanager

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.url_map.strict_slashes = False  # Avoid automatic redirections to add slash


# Decorator for the endpoints. Catches exceptions and converts them
#   to proper error messages
def process_response(func):
    def func_wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            status = 200
        except Exception as e:
            # Don't leak information on unexpected errors
            result = {'error': 'server error'}
            status = 500
            print(e)

        res_json = json.dumps(result, ensure_ascii=False)
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        return res_json, status, headers

    return func_wrapper


@app.route("/games", methods=['POST'])
@process_response
def new_game():
    return dict(game_id=gamemanager.new_game(4, '123456'))


# This won't execute if using FastCGI
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int("8080"))
