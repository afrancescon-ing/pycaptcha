# PyCaptcha

A Python, captcha and docker exercise.

## Assignment

Your company is behind an online forum about cooking, but the registration procedure is too easy for a bot to complete. You’re therefore asked to provide a backend service to work with captcha images. The service must be capable of generating captchas and validate them against the solution. You can find a definition of captcha on wikipedia: https://en.wikipedia.org/wiki/CAPTCHA

You’re responsible to design a complete solution and to actually code it in Python or Node.js (just use the language you’re more comfortable with). You must version this project with git and provide a public URL where we can check your solution. Please don’t put any reference to our company inside the repository.

Some constraints:
* [C1] provide a README.md file with clear instructions about how we can test your service in a local development environment;
* [C2] the communication protocol will be HTTP. We expect one route to provide the CAPTCHA and a second route to validate it. You’re free to design as you like, but you’re asked to provide documentation for both of the endpoints;
* [C3] this service is meant to operate inside a micro-services architecture and must be shipped inside a docker image;

Some suggestions:
* [Sa] use either Fastify for node.js, or FastAPI for python;
* [Sb] automated unit tests for the project are a plus;
* [Sc] typing your code (typescript or typed python checked with mypy) is considered a plus;
* [Sd] using an external database for persistency is a plus, but even an in memory solution is ok.

## About constraints and suggestions
[C1] This file, which has plenty of information about solution design and testing.

[C2] See [S1](#s1-endpoint-1-generate-requestfunction),[S2](#s2-endpoint-2-validate-requestfunction) and [S3](#s4-captcha) (and all other _SX_ subsections) in the [Solution](#solution-description) section

[C3] See [S7](#s7-environmental-variables-management) and [S10](#s10-docker)

[Sa] FastAPI used

[Sb] See [S8](#s9-testing) section

[Sc] All code is typed (mypy gives the green light, and also its VSCode plugin does not highlight criticalities)

[Sd] Both an in-memory (dict-based Cache) and an external (Redis-based) solution are provided (see respectively [S6.1](#s61-local-cache) and [S6.2](#s62-redis))

## Proposed Solution

### Used libs
Python version: `Python 3.9.18`

Installed libraries:

* [FastAPI](https://fastapi.tiangolo.com/)
* [uvicorn](https://www.uvicorn.org/)
* [mypy](https://pypi.org/project/mypy/)
* [captcha](https://pypi.org/project/captcha/)
* [redis](https://github.com/redis/redis-py)
* [httpx](https://www.python-httpx.org/)
* [pytest](https://docs.pytest.org/en/8.2.x/)

```
pip install fastapi uvicorn mypy captcha redis httpx pytest
```
### Run it
Simply go for
```
python3 <path_to_pycaptcha>/pycaptcha.py
```
API shall be now accessible at `127.0.0.1:8000`

### Folder Structure

Note: empty `__init__.py` omitted
```
docker/                         docker folder
    compose.yaml                pycaptcha+redis service descriptor for docker
    Dockerfile                  Dockerfile to generate a docker image for 
                                  pycaptcha
log/                            log folder (created at runtime)
package/                        source code for modules developed for the app
    __init__.py                 app constants
    persistency/                folder for persistency-related components
        managers/               definitions of persistency managers (pm)
            __init__.py         Persistency Managers specific constants
            cache_local_pm.py   in-memory, dict-based pm class
            pm_interface.py     interface for pms
            redis_pm.py         redis-based pm class
        prims.py                primitives associated with persistency managers
                                  component handling
    utils/                      folder for useful functions
        captcha.py              utility functions related to capcha management
        env_globals.py          utility functions related to env vars management
        log_manager.py          utility functions related to log configuration
        params_manager.py       utility functions related to app parameters mgmt
        textgen.py              utility functions related to text generation 
pycaptcha.py                    main file
README.md                       this file
test_pycaptcha.py               test file example
```
### Solution Description

According to the assignment, the solution consists of defining two endpoints and other modules that provide functionalities that support endpoints' proper functioning. The app endpoints are exposed on a given port `port` of a given host `hostname`

#### S1. ENDPOINT 1: **GENERATE** request/function
The 'generate' function, the first part of our solution, is responsible for creating a new captcha.  
A GET request at the plain URL:  
_http://`hostname`:`port`_  
triggers this function, which generates a random string and creates a unique identifier `uuid` for it.  
Then, it stores the pair (uuid, text) in the Persistence Manager.  
Once the pair is stored, the function generates the captcha image and returns it as a response, with the uuid associated with the captcha **in the header of the response** (key=`captcha_uuid`).  

_**NOTE:**_ 
To avoid having couples stored in the Persistence Manager for an indeterminate amount of time, it is worth assigning an expiration_time to each added couple: when the timer expires, the couple is deleted from the Persistence Manager. Thus, even if a couple is never checked again, it will be removed after a finite time.

#### S2. ENDPOINT 2: **VALIDATE** request/function
The "validate" function is responsible for validating users' captcha interpretation.  
It triggers on the arrival of a GET request at this endpoint URL:  
_http://`hostname`:`port`/`uuid`/`captcha_guess`_  
where `uuid` is the identifier associated with the previously generated captcha (stored in the header of the received response on generation), while `captcha_guess` is the value users guessed for the captcha.  
The function retrieves from the Persistence Manager the value associated with the passed uuid and then checks if the user's guessed value is the same as the stored value (`True` if they are equal, `False` otherwise). The check response is added to the body of the response message, which is a JSON file structured as follows:  
```
{
 "validation": <check_response>
}
```
_**NOTE 1:**_ 
If the requested `uuid` is not found in the `Persistence Manager,` the check is evaluated as `False.`  

_**NOTE 2:**_ 
When the `Persistence Manager` retrieves a given `value` at a given `uuid`, it should return the `value` and delete the couple to prevent repeated attempts.

#### S3.SERVICE FLOW example
Our cooking site registration operation can operate as follows:
1. A User clicks the registration button.

2. The website prompts a Registration Form: the last Form entry is a captcha-generating/refreshing button with an image box showing the captcha and a text field for user's guess. **The captcha has been generated via a `GENERATE` request, and the returned `uuid` in the response's header is used to pre-generate the URL of the following `VALIDATE` request**.

3. If the user refreshes the captcha, a new GET request is sent to endpoint 1, and **the returned `uuid` is used to update the URL for the next `VALIDATE` request**.

4. The user pushes the form submit button. Before proceeding with the registration, the website checks the VALIDATE response: **it fills the URL with the user `captcha_guess` and then performs the `VALIDATE` request**.

5. In response, the website parses it and retrieves the check value: 
    * on `true`, it triggers the User registration process

    * on `false`, it stops the submission process, notifies the user about the failed attempt and proceeds with the actions planned in case of error (e.g., requesting the user to guess on another captcha)

#### S4. CAPTCHA
For captcha image generation, I relied on `captcha` library.  
After a simple initialization, an input string is used to generate a related captcha.  
For the text, I added a basic random text generator module (see next [subsection](#s5-text-generator))

#### S5. TEXT Generator
The text generator generates random text starting from the expected length of the generated text (passed as an integer) and the set of allowed chars (passed as a string).

#### S6. PERSISTENCY Managers
The Persistency Manager (PM) is the system component meant to store and preserve (according to some policies) all the information reqired for the correct functioning of the solution.  
In terms of stored data, the PM saves the association between a generated captcha text and the identifier (uuid) generated when that captcha text is used to generate the captcha image. This is done by defining a `(key, value)` couple, where `key` is the `uuid` and `value` is the `text`.  
In terms of policies, we would like to have the following behaviors implemented:  
1. For each new captcha generated, its associated couple (uuid, text) has to be saved immediately into PM.  
 That couple is said `active`;

2. Every captcha created, even if generated by the same input text, has an identifier different from any of all the other active couples (=captchas);

3. When a couple (uuid, text) is accessed for validation, it has to be DELETED from the PM.
 That couple is now said `consumed`;

4. After passing a given amount of time (i.e., `EXPIRATION_TIME`) since a couple's activation (i.e., insertion into PM), if that couple has not been consumed yet, it is considered `expired` and listed as a candidate for deletion. It can be deleted immediately (`strict expiration time`) or after some time variable (`loose expiration time`): the point is not to have it lingering in the PM forever.

5. Each operation on the PM has to be synchronized, to have each operation executed in sequence and avoid any chance of concurrent access to the resource

Policy 1. ensures the couple's immediate availability for incoming validation checks.  
Policy 2. grants no ambiguities or collisions between active captchas. Using `uuids` ensures the identifier's uniqueness.  
Policy 3. prevents multiple attempts on failed validation.  
Policy 4. prevents the PM from being saturated by not-validated couples.  
Policy 5. prevents simultaneous access to the resource for validation, trying to validate it by flooding it with concurrent requests. The synchronized approach is implemented using `threading.Lock'- based checks on PM operations.

##### S6.1) Local Cache PM
This PM class is an in-memory implementation of PM based on a dictionary.  
Activation and consumption of the key are trivial, respectively, based on insertion and deletion.  
Since implementing a strict expiration mechanism is somewhat resource-consuming (it implies one or more threads in the background performing the deletion operation with a timer specific for each couple, leading to a potentially impacting resource consumption and overmanagement), the proposed implementation relies on a `loose expiration approach`, where the activation generates and stores a `3-ple (key, value, activation_time)` and then a `tidy routine` is assumed to be triggered periodically (every `TIDY_TIME` seconds) checking all active entries and deleting those expired. Thus, after `EXPIRATION_TIME+TIDY_TIME` seconds passed since its creation, it is sure that that PM entry is no more.

##### S6.2) Redis PM
This implementation relies on an external Redis running instance (python library `redis` is required to interface with it). Redis instance hostname and port are supposed to be set:
* by hardcoding default values here  
`pycaptcha/package/persistency/managers/__init__.py`

* indirectly, by defining these specific environmental variables (with proper values)  
`PYCAP_APP_REDIS_HOST`  
`PYCAP_APP_REDIS_PORT`  
before running the app.  
**_NOTE_**: The same dual approach can be applied for other parameters, as explained in [S7](#s7-environmental-variables-management)

* by passing (altering the code) the new environmental variables' name and values structured as a dictionary `env_vars` to the function  
`EGLOB.init_environment(env_vars)` in `pycaptcha.py`  
(again, see [S7](#s7-environmental-variables-management))

Policy 1. is satisfied by leveraging `redis` SET method, and, by specifying the `ex` option, at the same time, we configure for that inserted couple (uuid, value) an expiration time natively managed by Redis (thus, satisfying also policy 4. with a `strict expiration` approach).  
Policy 3. is granted by using the `getdel` method, which returns the value associated with that key and deletes the entry at the same time.

#### S7. ENVironmental VARiables Management
The application is capable of retrieving the values for its main parameters from environmental variables to provide greater flexibility to the code.  
These are the currently available parameters covered by such a feature: 

`PYCAP_APP_HOST`: application host  
`PYCAP_APP_PORT`: application port  

`PYCAP_LOG_LEVEL`: log level  
`PYCAP_LOG_LOGFOLDER`: log folder  

`PYCAP_TEXTGEN_LENGTH`: length of the randomly generated text for captchas  
`PYCAP_TEXTGEN_ALLOWED_CHARS`: allowed charset for randomly generated text for captchas  

`PYCAP_CAPTCHA_WIDTH`: captcha image's width  
`PYCAP_CAPTCHA_HEIGHT`: captcha image's width  

`PYCAP_PM_CLASS`: class of PM to use (`'cache'` or `'redis'`)  

`PYCAP_PM_CACHE_EXPTIME`: expiration time for Local Cache PM  
`PYCAP_PM_CACHE_TIDYTIME`: tidy time for Local Cache PM  


`PYCAP_APP_REDIS_HOST`: Redis instance host  
`PYCAP_APP_REDIS_PORT`: Redis instance port  
`PYCAP_PM_REDIS_EXPTIME`: expiration time for Redis PM  
`PYCAP_PM_REDIS_DECODE_RESP`: decode_response value for Redis PM (should be `True`)

The names and default values for such environmental variables are defined here:
* `pycaptcha/package/__init__.py`
* `pycaptcha/package/persistency/managers/__init__.py`

and some utility functions for handling them during application execution are defined here:
* `pycaptcha/package/utils/params_manager.py`

The policy regarding the usage of such parameters is the following:  
* IF the related argument is explicitly passed in a function call, THEN the argument value is used
* ELSE, IF the associate environmental variable is defined, THEN the value of the env var is used
* ELSE, the default value is used

_**NOTE**_: such an ENV_VAR-based configuration approach could also be useful when the application is run in a docker container since environmental variables can be set-overridden at launch time without the need for modifying the application code directly.

#### S8. GLOBAL VARIABLES
Application proper functioning relies on these five global variables (defined in `pycaptcha/package/utils/env_globals.py`): 

`persistence_manager`: current instance of PM in use  
`captcha_width`: current value for the captcha image's width (in pixels)  
`captcha_height`: current value for the captcha image's height (in pixels)  
`textgen_length`: current value for randomly generated captcha text's length  
`textgen_allowed_chars`: current value for randomly generated captcha text's allowed charset  

`init_environment` function (defined in the same file) assigns the value to these variables (and also sets environmental variables, if provided - as anticipated at the end of section [S62](#s62-redis-pm)).

_**NOTE**_: Running this function multiple times overwrites previous values (something that will impact heavily any previous operation on PM since a new instance of it will be generated and used, with the previous one left with no references, waiting for garbage collection)

#### S9. TESTING
FastAPi can be tested by leveraging `httpx` and `pytest`.  
File `test_pycaptcha.py` is an example of the test file.  
`init_environment` is also helpful here since it allows modifying the env vars on the fly and retriggering the initialization of the global variables, thus enabling the setup of specific testing scenarios.  
The only recommendation while using such a function is to avoid referring to any operation/event that happened before invoking it, since the persistency manager those operations relied on is no longer the one now referenced by the global variable `persistence_manager`.

#### S10. DOCKER
Since the app is meant to run in a docker container, a `Dockerfile` for generating a Docker image with the last version of the app and the proper environment to run it is provided in folder `docker/`.  
The image exposes port `8000`, to be mapped to a host port, thus the app endpoints can be accessed locally.
A pycaptcha Docker image generated with that doker file can be retrived from DockerHub:
```
docker pull afrancescon/pycaptcha:latest
```

For testing purposes, it can be configured to rely on a Redis instance by providing via environmental vars Redis host and port and and the PM to redis:
```
PYCAP_PM_CLASS = redis
PYCAP_APP_REDIS_HOST = <redis_HOST_value>
PYCAP_APP_REDIS_PORT = <redis_PORT_value>
```
A Redis Docker image can be retrieved running
```
docker pull redis
```

To test it,
1. Run a container with `redis` image

2. Run a container with `pycaptcha` image (configuring env vars according to redis container setting).
It is worth also adding at least these two extra env vars (which basically allow to know in advance the text used for genertaing the captcha - 'AA', in this case)
```
PYCAP_TEXTGEN_ALLOWED_CHARS = A
PYCAP_TEXTGEN_LENGTH = 2
```  

3. Assuming `pycaptcha`'s exposed port `8000` is mapped to host port `8888`, perform a  
`GET` request on host @`127.0.0.1:8888/`  
It will return a captcha ass a png image, with the uuid saved in the header of the response (key=`captcha_uuid`).  
Alternatively, that `uuid` value can be retrieved from pycaptcha's log, since every time a new captcha is created, a new line like the following is added to log:  
`[<LOG_TIME_MODULE_INFO>] {[<PM_TYPE>] ADDED new captcha @<app_host>:<app_port>/<uuid>/<text>}`  

4. Perform a  
`GET` request on host @`127.0.0.1:8888/<uuid>/<text>`  
The JSON response with have `validation` key set to `true`

5. Repeat the same request, the JSON response with have `validation` key set to `false` (the couple `(uuid,text)` is `consumed` now)

6. Keep playing around with it, creating new captchas, checking them and using wrong uuids or texts to see how the app reacts

_**NOTE:**_ This whole scenario can be recreated entering `docker` folder and using the `compose.yaml` file by running
```
docker compose up
```
Then, open a browser and play with  
`GENERATE` --> `http://127.0.0.1:8888`  
and  
`VALIDATE` --> `http://127.0.0.1:8888/<uuid>/<text>`  
requests.