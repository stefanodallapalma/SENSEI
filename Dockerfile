FROM python:3.7.1

RUN mkdir /ANITA
COPY /ANITA/python/requirements.txt /ANITA/requirements.txt

WORKDIR /ANITA/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install connexion[swagger-ui]

COPY /ANITA /ANITA

WORKDIR /ANITA/
RUN ls
WORKDIR /ANITA/resources/
RUN ls

WORKDIR /ANITA/python/
RUN ls