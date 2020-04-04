FROM python:latest

ADD . /app/src
WORKDIR /app/src

RUN mkdir -p /var/log/django && touch /var/log/django/debug.log
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]

EXPOSE 8000