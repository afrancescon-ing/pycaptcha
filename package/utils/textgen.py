
from random import choice
from package import TEXTGEN_LENGTH_DEFAULT, TEXTGEN_ALLOWED_CHARS_DEFAULT

def generate_random_text(length: int, allowed_chars: str):
    return ''.join(choice(allowed_chars) for i in range(length))

def generate_random_captcha_text(
    length: int=TEXTGEN_LENGTH_DEFAULT,
    allowed_chars: str=TEXTGEN_ALLOWED_CHARS_DEFAULT):
    return generate_random_text(length, allowed_chars)
