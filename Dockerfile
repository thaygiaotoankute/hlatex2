FROM python:3.10.0-slim

WORKDIR /app

# Cài đặt zstd để giải quyết vấn đề "invalid gzip header"
RUN apt-get update && apt-get install -y zstd

# Sao chép và cài đặt requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Sao chép tất cả file dự án
COPY . .

# Thiết lập biến môi trường
ENV PORT=8080
ENV FLY_APP_NAME=true
ENV PYTHON_VERSION=3.10.0

# Chạy ứng dụng với Gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080"]
