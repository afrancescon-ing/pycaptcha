import uuid
import logging
from fastapi import FastAPI
from fastapi.responses import Response, JSONResponse
from package.persistency.prims import pm_factory
from package.utils.captcha import generate_captcha
from package.utils.log_manager import configure_log
from package.utils.params_manager import CAPTCHA_UUID_KEY
from package.utils.textgen import generate_random_captcha_text

# Logger configuration

configure_log()

logger = logging.getLogger(__name__)

# Persistence manager configuration

persistence_manager = pm_factory()

# Instantiate app

app = FastAPI()

@app.get("/")
async def get_captcha() -> Response:

    if persistence_manager is None:
        raise TypeError("Persistence Manager is not assigned")

    captcha_text = generate_random_captcha_text()
    image_bytes = generate_captcha(captcha_text)

    headers: dict = {}
    while not headers:
        captcha_uuid = str(uuid.uuid4())

        if persistence_manager.push(captcha_uuid, captcha_text):
            headers[CAPTCHA_UUID_KEY] = captcha_uuid

    return Response(
        content=image_bytes,
        media_type="image/png",
        headers=headers)

@app.get("/{captcha_uuid}/{captcha_text}")
async def validate(captcha_uuid: str, captcha_text: str) -> JSONResponse:
    if persistence_manager is None:
        raise TypeError("Persistence Manager is not assigned")
    return JSONResponse(
        content={"validation": persistence_manager.pop(captcha_uuid) == captcha_text})
