from io import BytesIO
from captcha.image import ImageCaptcha
from package import CAPTCHA_IMAGE_HEIGHT_DEFAULT,\
                    CAPTCHA_IMAGE_WIDTH_DEFAULT

def generate_captcha(text: str,
                     width: int =CAPTCHA_IMAGE_WIDTH_DEFAULT,
                     height: int =CAPTCHA_IMAGE_HEIGHT_DEFAULT):

    # Configure
    image = ImageCaptcha(width, height)

    # generate the image of the given text
    image_bytes: BytesIO = image.generate(text)

    return image_bytes.getvalue()
