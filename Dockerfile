FROM python:3.7.1

RUN apt-get update && apt-get install default-jdk
RUN mkdir /ANITA
COPY /ANITA/python/requirements.txt /ANITA/requirements.txt

WORKDIR /ANITA/python/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install connexion[swagger-ui]

COPY /ANITA /ANITA
