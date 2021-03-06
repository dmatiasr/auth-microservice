FROM python:3.10.0b1-slim-buster

RUN apt update


COPY ./authenticator /opt/authenticator
WORKDIR /opt/authenticator


RUN apt install -y build-essential libssl-dev libffi-dev python-dev
RUN apt install -y python3-pip 
RUN pip install -r requirements.txt


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]


