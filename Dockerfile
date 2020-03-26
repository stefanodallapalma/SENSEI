FROM python:3.7.1

ENV FLASK_APP anita.py
ENV FLASK_RUN_HOST 0.0.0.0

EXPOSE 5000

RUN mkdir /ANITA
COPY /ANITA /ANITA

WORKDIR /ANITA/python/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt