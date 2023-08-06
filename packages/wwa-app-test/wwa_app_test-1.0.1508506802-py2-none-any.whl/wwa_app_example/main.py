def test(input):
    if input < 0:
        raise ValueError("Negative Input not allowed.")
    return input + 1

def run():
    print("It works!")
