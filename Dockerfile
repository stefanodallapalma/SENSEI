FROM python:3.7.1

RUN apt-get update && apt-get install -y default-jdk
RUN mkdir /ANITA
COPY /ANITA/python/requirements.txt /ANITA/requirements.txt

WORKDIR /ANITA/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install connexion[swagger-ui]

WORKDIR /ANITA/python/
COPY /ANITA /ANITA