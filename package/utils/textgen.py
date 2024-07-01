
from random import choice
import logging
from package import TEXTGEN_LENGTH_DEFAULT, TEXTGEN_ALLOWED_CHARS_DEFAULT

logger = logging.getLogger(__name__)

def generate_random_text(length: int, allowed_chars: str):
    if len(allowed_chars) < 1:
        logger.warning('allowed_chars length <0, returned string is always empty')
        return ''
    if length < 1:
        logger.warning('text length <1, returned string is always empty')
        return ''
    return ''.join(choice(allowed_chars) for i in range(length))

def generate_random_captcha_text(
    length: int=TEXTGEN_LENGTH_DEFAULT,
    allowed_chars: str=TEXTGEN_ALLOWED_CHARS_DEFAULT):
    return generate_random_text(length, allowed_chars)
