
import time
from fastapi.testclient import TestClient
from httpx import Response
from package import \
    CAPTCHA_UUID_KEY,\
    TEXTGEN_ALLOWED_CHARS_ENV,\
    TEXTGEN_LENGTH_ENV
from package.persistency.managers import\
    PM_CLASS_ENV,\
    PM_CACHE_TYPE,\
    PM_REDIS_TYPE,\
    PM_CACHE_TIDYTIME_ENV,\
    PM_CACHE_EXPTIME_ENV,\
    PM_REDIS_EXPTIME_ENV

from package.utils.params_manager import get_cache_tidytime, get_redis_exptime
import package.utils.env_globals as EGLOB
from package.utils.textgen import generate_random_captcha_text

from pycaptcha import app

MULTIPLE_INSERTIONS = 100

# Utility functions

def assert_generate_response(response: Response):
    assert response.status_code == 200
    assert CAPTCHA_UUID_KEY in response.headers

def assert_validate_response(response: Response, expected_value: bool =True):
    assert response.status_code == 200
    assert response.json() == {"validation": expected_value}

def get_uuid_key_from_headers(response: Response):
    assert CAPTCHA_UUID_KEY in response.headers
    return response.headers[CAPTCHA_UUID_KEY]

def generate_req(client: TestClient) -> Response:
    return client.get("/")

def generate_req_and_assert(client: TestClient) -> Response:
    response = generate_req(client)
    assert_generate_response(response)
    return response

def validate_req(client: TestClient, uuid: str, value: str) -> Response:
    return client.get(f"/{uuid}/{value}")

def validate_req_and_assert(client: TestClient, uuid: str, value: str, expected_value: bool =True) -> Response:
    response = client.get(f"/{uuid}/{value}")
    assert_validate_response(response, expected_value)
    return response

# Tests

def test_generate_random_captcha_text():

    client = TestClient(app)

    env_vars = {}
    env_vars[TEXTGEN_LENGTH_ENV] = "2"
    env_vars[TEXTGEN_ALLOWED_CHARS_ENV] = 'A'
    EGLOB.init_environment(env_vars)

    text = generate_random_captcha_text(
        EGLOB.get_textgen_length(),
        EGLOB.get_textgen_allowed_chars())

    assert text == 'AA'

    env_vars[TEXTGEN_LENGTH_ENV] = "2"
    env_vars[TEXTGEN_ALLOWED_CHARS_ENV] = 'B'
    EGLOB.init_environment(env_vars)

    text = generate_random_captcha_text(
        EGLOB.get_textgen_length(),
        EGLOB.get_textgen_allowed_chars())

    assert text == 'BB'

    env_vars[TEXTGEN_LENGTH_ENV] = "5"
    env_vars[TEXTGEN_ALLOWED_CHARS_ENV] = 'c'
    EGLOB.init_environment(env_vars)

    text = generate_random_captcha_text(
        EGLOB.get_textgen_length(),
        EGLOB.get_textgen_allowed_chars())

    assert text == 'ccccc'

    env_vars[TEXTGEN_LENGTH_ENV] = "0"
    env_vars[TEXTGEN_ALLOWED_CHARS_ENV] = 'c'
    EGLOB.init_environment(env_vars)

    text = generate_random_captcha_text(
        EGLOB.get_textgen_length(),
        EGLOB.get_textgen_allowed_chars())

    assert text == ''

    env_vars[TEXTGEN_LENGTH_ENV] = "2"
    env_vars[TEXTGEN_ALLOWED_CHARS_ENV] = ''
    EGLOB.init_environment(env_vars)

    text = generate_random_captcha_text(
        EGLOB.get_textgen_length(),
        EGLOB.get_textgen_allowed_chars())

    assert text == ''
    
    env_vars[TEXTGEN_LENGTH_ENV] = "-1"
    env_vars[TEXTGEN_ALLOWED_CHARS_ENV] = 'c'
    EGLOB.init_environment(env_vars)

    text = generate_random_captcha_text(
        EGLOB.get_textgen_length(),
        EGLOB.get_textgen_allowed_chars())

    assert text == ''

def test_gen_and_validate_cache_pm():

    client = TestClient(app)

    env_vars = {}
    env_vars[TEXTGEN_LENGTH_ENV] = "2"
    env_vars[TEXTGEN_ALLOWED_CHARS_ENV] = 'A'
    env_vars[PM_CLASS_ENV] = PM_CACHE_TYPE
    EGLOB.init_environment(env_vars)

    assert EGLOB.get_pm_type() == PM_CACHE_TYPE

    # "generate" endpoint request + check
    response = generate_req_and_assert(client)

    uuid = get_uuid_key_from_headers(response)

    # The generated captcha text shall be costant because of
    # textgen env var settings
    right_guess = 'AA'

    # First "validate" endpoint request + check: shall be True
    response = validate_req_and_assert(client, uuid, right_guess)
    # Second "validate" endpoint request + check: shall be False
    # since the previous one forced deletion of the key
    response = validate_req_and_assert(client, uuid, right_guess, False)

def test_N_gen_and_validate_cache_pm():

    client = TestClient(app)

    env_vars = {}
    env_vars[TEXTGEN_LENGTH_ENV] = "2"
    env_vars[TEXTGEN_ALLOWED_CHARS_ENV] = 'A'
    env_vars[PM_CLASS_ENV] = PM_CACHE_TYPE

    EGLOB.init_environment(env_vars)

    assert EGLOB.get_pm_type() == PM_CACHE_TYPE

    uuids = []
    # Perform MULTIPLE_INSERTIONS "generate" endpoint requests
    for i in range(MULTIPLE_INSERTIONS):

        # "generate" endpoint request + check
        response = generate_req_and_assert(client)
        # Retrieve uuid and add it to the uuids list
        uuids.append(get_uuid_key_from_headers(response))

    # The generated captcha text shall be costant because of
    # textgen env var settings
    right_guess = 'AA'

    # Perform a "validate" endpoint requests for each uuid in uuids,
    # i.e., MULTIPLE_INSERTIONS validate" endpoint requests
    for uuid in uuids:
        # First "validate" endpoint request + check: shall be True
        response = validate_req_and_assert(client, uuid, right_guess)

def test_tidy_routine_cache_pm():

    client = TestClient(app)

    env_vars = {}
    env_vars[TEXTGEN_LENGTH_ENV] = "2"
    env_vars[TEXTGEN_ALLOWED_CHARS_ENV] = 'A'
    env_vars[PM_CLASS_ENV] = PM_CACHE_TYPE
    env_vars[PM_CACHE_TIDYTIME_ENV] = '2'
    env_vars[PM_CACHE_EXPTIME_ENV] = '3'

    EGLOB.init_environment(env_vars)

    assert EGLOB.get_pm_type() == PM_CACHE_TYPE
    assert get_cache_tidytime() == 2

    uuids = []
    # Perform MULTIPLE_INSERTIONS "generate" endpoint requests
    for i in range(MULTIPLE_INSERTIONS):

        # "generate" endpoint request + check
        response = generate_req_and_assert(client)
        # Retrieve uuid and add it to the uuids list
        uuids.append(get_uuid_key_from_headers(response))

    # Awaits ~5+ seconds: in the meantime all keys should be expired and 
    # tidy routine should have removed them
    for i in range(50):
        time.sleep(0.1)

    # The generated captcha text shall be costant because of
    # textgen env var settings
    right_guess = 'AA'

    # Perform a "validate" endpoint requests for each uuid in uuids,
    # i.e., MULTIPLE_INSERTIONS validate" endpoint requests
    for uuid in uuids:
        # First "validate" endpoint request + check: shall be True
        response = validate_req_and_assert(client, uuid, right_guess, False)

def test_gen_and_validate_redis_pm():

    client = TestClient(app)

    env_vars = {}
    env_vars[TEXTGEN_LENGTH_ENV] = "2"
    env_vars[TEXTGEN_ALLOWED_CHARS_ENV] = 'A'
    env_vars[PM_CLASS_ENV] = PM_REDIS_TYPE

    EGLOB.init_environment(env_vars)

    assert EGLOB.get_pm_type() == PM_REDIS_TYPE

    # "generate" endpoint request + check
    response = generate_req_and_assert(client)

    uuid = get_uuid_key_from_headers(response)

    # The generated captcha text shall be costant because of
    # textgen env var settings
    right_guess = 'AA'

    # First "validate" endpoint request + check: shall be True
    response = validate_req_and_assert(client, uuid, right_guess)
    # Second "validate" endpoint request + check: shall be False
    # since the previous one forced deletion of the key
    response = validate_req_and_assert(client, uuid, right_guess, False)

def test_N_gen_and_validate_redis_pm():

    client = TestClient(app)

    env_vars = {}
    env_vars[TEXTGEN_LENGTH_ENV] = "2"
    env_vars[TEXTGEN_ALLOWED_CHARS_ENV] = 'A'
    env_vars[PM_CLASS_ENV] = PM_REDIS_TYPE

    EGLOB.init_environment(env_vars)

    assert EGLOB.get_pm_type() == PM_REDIS_TYPE

    uuids = []
    # Perform MULTIPLE_INSERTIONS "generate" endpoint requests
    for i in range(MULTIPLE_INSERTIONS):

        # "generate" endpoint request + check
        response = generate_req_and_assert(client)
        # Retrieve uuid and add it to the uuids list
        uuids.append(get_uuid_key_from_headers(response))

    # The generated captcha text shall be costant because of
    # textgen env var settings
    right_guess = 'AA'

    # Perform a "validate" endpoint requests for each uuid in uuids,
    # i.e., MULTIPLE_INSERTIONS validate" endpoint requests
    for uuid in uuids:
        # First "validate" endpoint request + check: shall be True
        response = validate_req_and_assert(client, uuid, right_guess)

def test_key_expiration_redis_pm():

    client = TestClient(app)

    env_vars = {}
    env_vars[TEXTGEN_LENGTH_ENV] = "2"
    env_vars[TEXTGEN_ALLOWED_CHARS_ENV] = 'A'
    env_vars[PM_CLASS_ENV] = PM_REDIS_TYPE
    env_vars[PM_REDIS_EXPTIME_ENV] = '2'

    EGLOB.init_environment(env_vars)

    assert EGLOB.get_pm_type() == PM_REDIS_TYPE
    assert get_redis_exptime() == 2

    uuids = []
    # Perform MULTIPLE_INSERTIONS "generate" endpoint requests
    for i in range(MULTIPLE_INSERTIONS):

        # "generate" endpoint request + check
        response = generate_req_and_assert(client)
        # Retrieve uuid and add it to the uuids list
        uuids.append(get_uuid_key_from_headers(response))

    # Awaits ~2.5+ seconds: in the meantime all keys should be expired
    # and removed
    for i in range(25):
        time.sleep(0.1)

    # The generated captcha text shall be costant because of
    # textgen env var settings
    right_guess = 'AA'

    # Perform a "validate" endpoint requests for each uuid in uuids,
    # i.e., MULTIPLE_INSERTIONS validate" endpoint requests
    for uuid in uuids:
        # First "validate" endpoint request + check: shall be True
        response = validate_req_and_assert(client, uuid, right_guess, False)