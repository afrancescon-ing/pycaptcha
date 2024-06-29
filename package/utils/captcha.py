from io import BytesIO
from captcha.image import ImageCaptcha

# Captcha image sizing
CAPTCHA_IMAGE_WIDTH: int = 280
CAPTCHA_IMAGE_HEIGHT: int = 100

def generate_captcha(text: str, width: int =CAPTCHA_IMAGE_WIDTH, height: int =CAPTCHA_IMAGE_HEIGHT):

    # Configure
    image = ImageCaptcha(width, height)

    # generate the image of the given text
    image_bytes: BytesIO = image.generate(text)

    return image_bytes.getvalue()
