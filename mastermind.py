import random


def generate_code(length, chars):
    return ''.join(random.choices(chars, k=length))


def remove_char(string, pos):
    if pos >= len(string):
        raise IndexError
    return string[0:pos] + string[pos+1:len(string)]


def compute_answer(code, guess):
    length = len(code)
    if len(guess) != length:
        raise ValueError(
            "Guess length should be equal to code length (%s)" % length)

    b = w = 0

    # Find blacks
    black_pos = []
    for i in range(length):
        if code[i] == guess[i]:
            black_pos.append(i)
            b += 1

    # Remove black findings from guess and code
    # do it in reverse order to keep black_pos indexes valid
    for pos in reversed(black_pos):
        code = remove_char(code, pos)
        guess = remove_char(guess, pos)

    # Find whites
    for i in range(len(guess)):
        for j in range(len(code)):
            if guess[i] == code[j]:
                w += 1
                code = remove_char(code, j)
                break

    return [b, w]
