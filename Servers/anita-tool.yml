FROM python:3.7-alpine

RUN mkdir /ANITA
COPY ../ANITA/ /ANITA/

ENV FLASK_APP anita.py
ENV FLASK_RUN_HOST 0.0.0.0

RUN apk add --no-cache gcc musl-dev linux-headers
RUN ls