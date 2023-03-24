# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
WORKDIR /file_server_docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
EXPOSE 5000

COPY . .

CMD [ "flask", "run" ]