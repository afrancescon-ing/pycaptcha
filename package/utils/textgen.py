""" Utility functions for random text generation
"""

from random import choice
import logging
from package import TEXTGEN_LENGTH_DEFAULT, TEXTGEN_ALLOWED_CHARS_DEFAULT

logger = logging.getLogger(__name__)

def generate_random_captcha_text(
    length: int=TEXTGEN_LENGTH_DEFAULT,
    allowed_chars: str=TEXTGEN_ALLOWED_CHARS_DEFAULT) -> str:
    """Generates a random text for a captcha

    Args:
        length (int, optional): Length of the text. 
                                Defaults to TEXTGEN_LENGTH_DEFAULT.
        allowed_chars (str, optional): Charset for the text. 
                                       Defaults to TEXTGEN_ALLOWED_CHARS_DEFAULT.

    Returns:
        str: generated text
    """
    if len(allowed_chars) < 1:
        logger.warning('allowed_chars length <0, returned string is always empty')
        return ''
    if length < 1:
        logger.warning('text length <1, returned string is always empty')
        return ''
    return ''.join(choice(allowed_chars) for i in range(length))
