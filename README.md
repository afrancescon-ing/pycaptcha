

## Assignment

Your company is behind an online forum about cooking, but the registration procedure is too easy for a bot to complete. You’re therefore asked to provide a backend service to work with captcha images. The service must be capable of generating captchas and validate them against the solution. You can find a definition of captcha on wikipedia: https://en.wikipedia.org/wiki/CAPTCHA

You’re responsible to design a complete solution and to actually code it in Python or Node.js (just use the language you’re more comfortable with). You must version this project with git and provide a public URL where we can check your solution. Please don’t put any reference to our company inside the repository.

Some constraints:
* provide a README.md file with clear instructions about how we can test your service in a local development environment;
* the communication protocol will be HTTP. We expect one route to provide the CAPTCHA and a second route to validate it. You’re free to design as you like, but you’re asked to provide documentation for both of the endpoints;
* this service is meant to operate inside a micro-services architecture and must be shipped inside a docker image;

Some suggestions:
* use either Fastify for node.js, or FastAPI for python;
* automated unit tests for the project are a plus;
* typing your code (typescript or typed python checked with mypy) is considered a plus;
* using an external database for persistency is a plus, but even an in memory solution is ok;

You have two weeks starting from today to deliver your assignment. When you’re done, please reply to this email with a working link to the project repository.

# Used libs
```
pip install fastapi uvicorn mypy captcha
```
* [FastAPI](https://fastapi.tiangolo.com/)
* [uvicorn](https://www.uvicorn.org/)
* [mypy](https://pypi.org/project/mypy/)
* [captcha](https://pypi.org/project/captcha/)


