FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y zstd

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY . .

CMD gunicorn main:app --bind 0.0.0.0:8080
