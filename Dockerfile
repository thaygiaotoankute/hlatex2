FROM python:3.10.0-slim

# Cài đặt zstd
RUN apt-get update && apt-get install -y zstd

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
RUN pip install gunicorn

EXPOSE 8080
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080"]
