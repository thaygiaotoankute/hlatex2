FROM python:3.10-slim-bullseye

WORKDIR /app

# Cài đặt các dependencies và dọn dẹp trong cùng một layer
RUN apt-get update && apt-get install -y --no-install-recommends zstd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Thiết lập biến môi trường Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

# Copy requirements và cài đặt dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Tạo user không phải root để tăng bảo mật
RUN groupadd -r appuser && useradd --no-log-init -r -g appuser appuser

# Copy code ứng dụng
COPY . .

# Chuyển sang user không phải root
USER appuser

# Expose port
EXPOSE 8080

# Start command
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080"]
