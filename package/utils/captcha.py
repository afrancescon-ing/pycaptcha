""" Utility functions for captcha image generation
"""

from io import BytesIO
from captcha.image import ImageCaptcha
from package import CAPTCHA_IMAGE_HEIGHT_DEFAULT,\
                    CAPTCHA_IMAGE_WIDTH_DEFAULT

def generate_captcha(text: str,
                     width: int =CAPTCHA_IMAGE_WIDTH_DEFAULT,
                     height: int =CAPTCHA_IMAGE_HEIGHT_DEFAULT):
    """Generates captcha's image

    Args:
        text (str): text originating the captcha
        width (int, optional): image width. 
                               Defaults to CAPTCHA_IMAGE_WIDTH_DEFAULT.
        height (int, optional): image height_.
                                Defaults to CAPTCHA_IMAGE_HEIGHT_DEFAULT.

    Returns:
        bytes: captcha image bytes
    """

    # Configure
    image = ImageCaptcha(width, height)

    # generate the image of the given text
    image_bytes: BytesIO = image.generate(text)

    return image_bytes.getvalue()
