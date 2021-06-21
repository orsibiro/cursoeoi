# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster
WORKDIR /app1

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "manage.py", "runserver", "127.0.0.1:8000"]
