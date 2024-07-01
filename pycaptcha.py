import uuid
import logging
from fastapi import FastAPI
from fastapi.responses import Response, JSONResponse
import package.utils.env_globals as EGLOB
from package import CAPTCHA_UUID_KEY
from package.utils.captcha import generate_captcha
from package.utils.log_manager import configure_log
from package.utils.textgen import generate_random_captcha_text

configure_log()

logger = logging.getLogger(__name__)


# from package import \
#     CAPTCHA_UUID_KEY,\
#     TEXTGEN_ALLOWED_CHARS_ENV,\
#     TEXTGEN_LENGTH_ENV
# from package.persistency.managers import\
#     PM_CLASS_ENV,\
#     PM_CACHE_TYPE,\
#     PM_REDIS_TYPE,\
#     PM_CACHE_TIDYTIME_ENV,\
#     PM_CACHE_EXPTIME_ENV,\
#     PM_REDIS_EXPTIME_ENV
# env_vars = {}
# env_vars[TEXTGEN_LENGTH_ENV] = "2"
# env_vars[TEXTGEN_ALLOWED_CHARS_ENV] = 'A'
# env_vars[PM_CLASS_ENV] = PM_CACHE_TYPE
# env_vars[PM_CACHE_TIDYTIME_ENV] = '2'
# env_vars[PM_CACHE_EXPTIME_ENV] = '3'

EGLOB.init_environment()

# Instantiate app

app = FastAPI()

@app.get("/")
async def generate() -> Response:

    if EGLOB.persistence_manager is None:
        raise TypeError("Persistence Manager is not assigned")

    captcha_text = generate_random_captcha_text(
        EGLOB.textgen_length, EGLOB.textgen_allowed_chars)

    image_bytes = generate_captcha(captcha_text,
                                   EGLOB.captcha_width,
                                   EGLOB.captcha_height)

    headers: dict = {}
    while not headers:
        captcha_uuid = str(uuid.uuid4())

        if EGLOB.persistence_manager.push(captcha_uuid, captcha_text):
            headers[CAPTCHA_UUID_KEY] = captcha_uuid

    return Response(
        content=image_bytes,
        media_type="image/png",
        headers=headers)

@app.get("/{captcha_uuid}/{captcha_text}")
async def validate(captcha_uuid: str, captcha_text: str) -> JSONResponse:
    if EGLOB.persistence_manager is None:
        raise TypeError("Persistence Manager is not assigned")
    return JSONResponse(
        content={"validation": EGLOB.persistence_manager.pop(captcha_uuid) == captcha_text})