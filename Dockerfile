FROM python:3.10-slim

COPY ./requirements.txt /tmp

RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt

RUN useradd -m -d /proj -s /bin/bash app
COPY . /proj
WORKDIR /proj
RUN chown -R app:app /proj/*
USER app
