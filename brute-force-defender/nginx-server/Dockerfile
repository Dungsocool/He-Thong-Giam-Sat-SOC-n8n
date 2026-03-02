# Sử dụng base image Nginx Alpine siêu nhẹ
FROM nginx:alpine

# Xóa cấu hình mặc định
RUN rm /etc/nginx/conf.d/default.conf

# Copy cấu hình Nginx tùy chỉnh vào container
COPY nginx.conf /etc/nginx/nginx.conf

# TẠO SẴN file block_ips.conf rỗng
# Bước này cực kỳ quan trọng để Nginx không bị crash khi khởi động
# nếu lệnh include trong nginx.conf gọi đến một file không tồn tại.
RUN touch /etc/nginx/block_ips.conf && \
    chmod 644 /etc/nginx/block_ips.conf

# Thư mục web gốc (có thể mount file html vào đây sau)
WORKDIR /usr/share/nginx/html
