FROM python:latest

COPY requirements.txt /requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt
