import uuid
from io import BytesIO
from random import choice
from string import ascii_uppercase
from multiprocessing import Lock
from fastapi import FastAPI
from fastapi.responses import Response, JSONResponse
from captcha.image import ImageCaptcha


app = FastAPI()

cache = {}


# estrapolare cache e fare persistenza per redis (set+ expire + delete)
CAPTCHA_ALLOWED_CHARS = ascii_uppercase
CAPTCHA_UUID_KEY = 'captcha-uuid'
KEY_LIFETIME_SECONDS = 60

lock = Lock()

def push_captcha(captcha_uuid: str, captcha_text: str):
    lock.acquire()
    try:
        if captcha_uuid in cache:
            return False
        cache[captcha_uuid] = captcha_text
        return True
    finally:
        lock.release()

def pop_captcha(captcha_uuid: str):
    lock.acquire()
    try:
        return cache.pop(captcha_uuid)
    except KeyError:
        return None
    finally:
        lock.release()

def generate_captcha_text(length: int): 
    return ''.join(choice(CAPTCHA_ALLOWED_CHARS) for i in range(length))

@app.get("/")
async def root():

    # Create an image instance of the given size
    image = ImageCaptcha(width = 280, height = 100)

    # Image captcha text
    captcha_text = generate_captcha_text(10)

    headers = {}

    while not headers:
        captcha_uuid = str(uuid.uuid4())

        if push_captcha(captcha_uuid, captcha_text):
            headers[CAPTCHA_UUID_KEY] = captcha_uuid
            print(f'127.0.0.1:8000/{captcha_uuid}/{captcha_text}')

    # generate the image of the given text
    image_bytes: BytesIO= image.generate(captcha_text)
    
    return Response(content=image_bytes.getvalue(), media_type="image/png", headers=headers)

@app.get("/{captcha_uuid}/{captcha_text}")
async def ciccio(captcha_uuid: str, captcha_text: str):
    return JSONResponse(content={"validation": pop_captcha(captcha_uuid) == captcha_text})

