FROM python:3.8.11
ENV PYTHONUNBUFFERED 1

RUN apt-get update -y && apt-get upgrade --fix-missing -y
RUN apt-get update && apt-get install -y \
    gdal-bin


RUN pip install --upgrade pip

RUN mkdir /code
ADD . /code/

WORKDIR /code/
RUN pip install -r requirements/local.pip
