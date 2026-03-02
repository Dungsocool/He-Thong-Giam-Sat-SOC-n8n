
# Dùng Alpine Linux làm base image
FROM alpine:latest

# Cài đặt curl và bash
RUN apk add --no-cache curl bash

# Thiết lập thư mục làm việc
WORKDIR /app

# Copy kịch bản tấn công vào container
COPY attack.sh .

# Cấp quyền thực thi cho script
RUN chmod +x attack.sh

# Chạy kịch bản khi container khởi động
CMD ["./attack.sh"]
