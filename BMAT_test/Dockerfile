FROM python:latest

ADD . /app/src
WORKDIR /app/src

RUN mkdir -p /var/log/django && touch /var/log/django/debug.log
RUN pip install -r requirements.txt

EXPOSE 8000