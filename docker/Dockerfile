# Docker image to run lastest version of pycatpcha
# https://github.com/afrancescon-ing/pycaptcha
# Author: Antonio Francescon, 2024

FROM ubuntu:22.04
RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install -y curl
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get install -y python3.9
RUN apt-get install -y python3-pip
RUN pip install fastapi uvicorn mypy captcha redis httpx pytest
RUN apt-get install python3.9-venv python3.9-dev -y
RUN apt-get install -y git

RUN cd home; git clone https://github.com/afrancescon-ing/pycaptcha.git
CMD ["python3","/home/pycaptcha/pycaptcha.py"]
EXPOSE 8000