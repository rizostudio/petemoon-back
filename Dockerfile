FROM python:3.10-slim-buster

WORKDIR /code

COPY requirements.txt .

RUN pip install --upgrade pip

RUN apt-get update && apt-get -y install libpq-dev gcc
RUN apt install -y wkhtmltopdf


RUN pip install -r requirements.txt

COPY . /code

