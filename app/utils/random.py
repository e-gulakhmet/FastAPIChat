import random
import string


def random_string(count: int = 10) -> str:
    return ''.join(random.choices(string.ascii_letters, k=count))
