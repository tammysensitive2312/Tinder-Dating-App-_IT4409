# Sử dụng image Python chính thức làm base image
FROM python:3.11-slim

# Đặt thư mục làm việc trong container
WORKDIR /app

# Sao chép file requirements.txt vào container
COPY requirements.txt .

# Cài đặt các phụ thuộc từ requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn vào container
COPY src/ src/

# Đặt biến môi trường để Flask biết file chính
ENV FLASK_APP=src/main/app.py

# Mở cổng 5000 để Flask chạy
EXPOSE 5000

# Lệnh chạy ứng dụng Flask khi container khởi động
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]