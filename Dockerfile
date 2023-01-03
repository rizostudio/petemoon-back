FROM python:3.9-slim-buster

WORKDIR /petemoon-back

COPY requirements/production.txt ./requirements

RUN pip install --upgrade pip

RUN apt-get update && apt-get upgrade -y

RUN pip install -r requirements/production.txt

COPY . /petemoon-back

EXPOSE 8000