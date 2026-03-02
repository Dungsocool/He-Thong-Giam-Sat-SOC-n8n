# Dùng bản slim để tối ưu dung lượng
FROM python:3.10-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Copy requirements và cài đặt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy mã nguồn
COPY watcher.py .

# Chạy script (thêm -u để Python in log ra terminal ngay lập tức mà không buffer)
CMD ["python", "-u", "watcher.py"]
