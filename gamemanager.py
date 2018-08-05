import time
import redisclient, mastermind

def new_id():
    c = 0
    while True:
        timestamp = repr(int(time.time()*1000000))
        if not redisclient.get(timestamp):
            return timestamp
        c += 1
        if c == 10:
            raise RuntimeError("Error: Can't generate an unused game id")
    

def new_game(length, alphabet):
    game_id = new_id()
    code = mastermind.generate_code(length, alphabet)
    redisclient.set(
        game_id, 
        dict(alphabet = alphabet, length = length, code = code))

    return game_id


def get_game(game_id):
    game_info = redisclient.get(game_id)
    if not game_info:
        raise IndexError("Game not found")

    return game_info


def check_guess(game_id, guess):
    game_info = get_game(game_id)

    return mastermind.compute_answer(game_info['code'], guess)
