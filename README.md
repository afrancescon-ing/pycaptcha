

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
* [Sd] using an external database for persistency is a plus, but even an in memory solution is ok;

You have two weeks starting from today to deliver your assignment. When you’re done, please reply to this email with a working link to the project repository.

## About constraints and suggestions
[C1] This file, with plenty of information about solution design and testing.

[C2] See [S1](#s1-endpoint-1-generate-requestfunction),[S2](#s2-endpoint-2-validate-requestfunction) and [S3](#s4-captcha) (and all other _SX_ subsections) in the [Solution](#solution-description) section

[C3] See [S7](#s7-environmental-variables-management)

[Sa] FastAPI used

[Sb] See [S8](#s8-testing) section

[Sc] All code is typed (mypy is green and also its VSCode plugin does not highlight criticalities)

[Sd] Both an in-memory (dict-based Cache) and an external (Redis-based) solution are provided (see respectively [S6.1](#s61-local-cache) and [S6.2](#s62-redis))

## Proposed Solution

### Used libs
Python version: `Python 3.9.18`

Libraries:

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

### Folder Structure

Note: empty `__init__.py` omitted
```
log/                            log folder
package/                        source code for modules developed for the app
    __init__.py                 app constants
    persistency/                folder for persistency related components
        managers/               definitions of persistency managers (pm)
            __init__.py         Persistency Managers specific constants
            cache_local_pm.py   in-memory, dict-based pm class
            pm_interface.py     interface for pms
            redis_pm.py         redis-based pm class
        prims.py                primitives associated with persistency managers
                                component handling
    utils/                      folder for useful functions
        captcha.py              utility functions associated with capcha management
        env_globals.py          utility functions associated with env vars management
        log_manager.py          utility functions associated with log configuration
        params_manager.py       utility functions associated with app parameters mgmt
        textgen.py              utility functions associated with text generation 
pycaptcha.py                    main file
README.md                       this file
test_pycaptcha.py               test file example
```
### Solution Description

According to the assignment, the solution consists of defining two endpoints and other modules that provide functionalities that support the endpoints' proper functioning. The app endpoints are exposed on a given port `port` of a given host `hostname`

#### S1. ENDPOINT 1: **GENERATE** request/function
The 'generate' function, the first part of our solution, is responsible for creating a new captcha.  
A GET request at the plain URL:   
_http://`hostname`:`port`_  
triggers this function, which generates a random string and creates a unique identifier `uuid` for it.  
Then, it stores the pair (uuid, text) in the Persistence Manager.  
Once the pair is stored, the function generates the captcha image and returns it as a response, with the uuid associated with the captcha in the header of the response file (key=`captcha_uuid`).  

_**NOTE:**_ 
To avoid having couples stored in the Persistence Manager for an indeterminate amount of time, it is worth assigning an expiration_time to each added couple: when the timer expires, the couple is deleted from the Persistence Manager. Thus, even if a couple is not checked again, it will be removed after a finite amount of time.

#### S2. ENDPOINT 2: **VALIDATE** request/function
The "validate" function is responsible for validating users' captcha interpretation.
To trigger it, a GET request is required at this endpoint URL:  
_http://`hostname`:`port`/`uuid`/`captcha_guess`_  
where `uuid` is the identifier associated with the previously generated captcha (stored in the header of the received response on generation), while `captcha_guess` is the value users guessed for the captcha.
The function retrieves from the Persistence Manager the value associated with the passed uuid and then checks if the user's guessed value is the same as the stored value (`True` if they are equal, `False` otherwise). The check response is added to the body of the response message, which is a JSON file structured as follows:  
```
{
    "validation": <check_response>
}
```
_**NOTE 1:**_ 
If requested `uuid` is not found in the `Persistence Manager`, the check is evaluated as `False`.  

_**NOTE 2:**_ 
When the `Persistence Manager` retieves a given `value` at a given `uuid`, it should return the `value` and delete the couple, to prevent repeated attempts.

#### S3.SERVICE FLOW example
Our cooking site registration operation can operate as follows:
1. A User clicks the registration button.

2. The website prompts a Registration Form: the last Form entry is a captcha-generating/refreshing button with an image box showing the captcha and a text field for user's guess. **The captcha has been generated via `GENERATE` request, and the returned `uuid` in the header of the response is used to pre-generate the URL of the next `VALIDATE` request**.

3. If the user refreshes the captcha, a new GET request is sent to endpoint 1, and **the returned `uuid` is used to update the URL for the next `VALIDATE` request**.

4. The user pushes the form submit button. Before proceeding with the registration, the website checks the VALIDATE response: **it fills the URL with the user `captcha_guess` and then performs the `VALIDATE` request**.

5. On response, website parses it and retrieves the check value: 
   * on `true`, it triggers the User registration process
   * on `false`, it stops the submission process, notifies the user about the failed attempt and proceed with the action planned in case of error (e.g., requesting the user to guess on another captcha)

#### S4. CAPTCHA
#### S5. TEXT Generator
#### S6. PERSISTENCY Managers
##### S6.1) Local Cache
##### S6.2) Redis
#### S7. ENVironmental VARiables Management
#### S8. TESTING
