FROM python:3.7.1

RUN apt-get update && apt-get install -y default-jdk && apt-get install -y curl && apt-get install -y jq
RUN mkdir /ANITA
COPY /ANITA/python/requirements.txt /ANITA/requirements.txt

WORKDIR /ANITA/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install connexion[swagger-ui]

WORKDIR /ANITA/python/
COPY /ANITA /ANITA
COPY sonarqube-test.sh /ANITA/python/sonarqube-test.sh
