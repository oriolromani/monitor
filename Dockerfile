FROM ubuntu:latest

RUN apt-get update && apt-get install -y python3-pip

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt --no-cache-dir

ADD . /code/

WORKDIR /code