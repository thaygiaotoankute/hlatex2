FROM python:3.10.0-slim

WORKDIR /app

# Cài đặt zstd để giải quyết vấn đề "invalid gzip header"
RUN apt-get update && apt-get install -y zstd

COPY . .
RUN pip install -r requirements.txt
RUN pip install gunicorn

ENV PORT=8080
ENV FLY_APP_NAME=true

CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:8080"]  # Đảm bảo dùng app:app
