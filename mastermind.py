

def remove_char(string, pos):
    if pos >= len(string):
        raise IndexError
    return string[0:pos] + string[pos+1:len(string)]

def compute_answer(code, guess):
    length = len(code)
    if len(guess) != length:
        raise ValueError("The length of the guess should be equal to the code lenght (%s)" % length)

    # Find blacks
    for i in range(length):
        if code[i] == guess[i]:
            code = remove_char(code, i)
            guess = remove_char(guess, i)
            [b, w] = compute_answer(code, guess)
            return [b + 1, w]

    # Find whites
    for i in range(length):
        for j in range(length):
            if guess[i] == code[j]:
                guess = remove_char(guess,i)
                code = remove_char(code, j)
                [b, w] = compute_answer(code, guess)
                return [b, w + 1]

    return [ 0, 0 ]