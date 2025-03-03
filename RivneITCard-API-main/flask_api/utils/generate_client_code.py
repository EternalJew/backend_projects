import random


def generate_code():
    code = ''.join(str(random.randint(0, 9)) for _ in range(12))
    return code
