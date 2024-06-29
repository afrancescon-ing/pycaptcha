
from random import choice
from string import ascii_uppercase

CAPTCHA_ALLOWED_CHARS = ascii_uppercase

def generate_random_text(length: int, allowed_chars: str):
    return ''.join(choice(allowed_chars) for i in range(length))

def generate_random_captcha_text(length: int=10, allowed_chars: str=CAPTCHA_ALLOWED_CHARS):
    return generate_random_text(length, allowed_chars)
