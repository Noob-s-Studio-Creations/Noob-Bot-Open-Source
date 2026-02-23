import random
import string

def GetRandomText(length=50):
    characters = string.ascii_letters + string.digits
    random_filename = ''.join(random.choice(characters) for _ in range(length))

    return random_filename