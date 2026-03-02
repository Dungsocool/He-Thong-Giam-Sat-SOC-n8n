# 🛡️ Brute-Force Defender Lab


Một hệ thống lab giả lập hoàn chỉnh dựa trên Docker, cho phép mô phỏng các cuộc tấn công Brute-Force/DDoS quy mô nhỏ và tự động phát hiện, ngăn chặn IP của kẻ tấn công theo thời gian thực.

---

## 📑 Mục lục
- [Giới thiệu](#-giới-thiệu)
- [Cơ chế hoạt động](#-cơ-chế-hoạt-động)
- [Cấu trúc dự án](#-cấu-trúc-dự-án)
- [Yêu cầu hệ thống](#-yêu-cầu-hệ-thống)
- [Hướng dẫn sử dụng](#-hướng-dẫn-sử-dụng)

---

## 💡 Giới thiệu

**Brute-Force Defender** là một bài lab an toàn thông tin được thiết kế để giúp bạn hiểu rõ cách thức một hệ thống phát hiện và phản hồi lại các lưu lượng truy cập bất thường. Dự án bao gồm 3 thành phần chính:
1. **Nginx Web Server**: Mục tiêu bị tấn công.
2. **Attacker Bot**: Kịch bản giả lập tấn công liên tục.
3. **Security Watcher**: Hệ thống phòng ngự chủ động (Blue Team) bằng Python.

---

## ⚙️ Cơ chế hoạt động

1. `attacker-bot` liên tục gửi các request (curl) đến `nginx-server`.
2. `nginx-server` ghi nhận lại toàn bộ lịch sử truy cập vào file `access.log`.
3. `security-watcher` liên tục theo dõi (tail) file log này. Nếu phát hiện một IP gửi quá số lượng request cho phép trong một khoảng thời gian ngắn:
   - Ghi IP đó vào file `block_ips.conf`.
   - Ra lệnh reload lại cấu hình Nginx.
4. Kể từ lúc đó, Nginx sẽ trả về lỗi `403 Forbidden` cho mọi request từ IP của kẻ tấn công.

---

## 📂 Cấu trúc dự án

```text 
brute-force-defender/
├── docker-compose.yml       # File điều phối trung tâm
├── README.md                # Tài liệu hướng dẫn
├── nginx-server/            # Môi trường Web Server
│   ├── Dockerfile
│   ├── nginx.conf           # Cấu hình Nginx gốc
│   ├── block_ips.conf       # Danh sách IP bị cấm (Blacklist)
│   └── html/                # Web giả lập (index, login, 404)
├── security-watcher/        # Module giám sát (Blue Team)
│   ├── Dockerfile
│   ├── requirements.txt
│   └── watcher.py           # Core logic: check log, ban IP, reload Nginx
└── attacker-bot/            # Module giả lập tấn công (Red Team)
    ├── Dockerfile
    └── attack.sh            # Script spam request liên tục

---
---

#
🛠️ Yêu cầu hệ thống## 
Để chạy được lab này, máy của bạn cần cài đặt sẵn:

Docker

Docker Compose

🚀 Hướng dẫn sử dụng
Bước 1: Clone kho lưu trữ
Bash
git clone [https://github.com/your-username/brute-force-defender.git](https://github.com/your-username/brute-force-defender.git)
cd brute-force-defender
Bước 2: Khởi động hệ thống
Sử dụng Docker Compose để build và chạy toàn bộ các container cùng lúc:

Bash
docker-compose up --build
Bước 3: Quan sát quá trình (Logs)
Ngay khi các container khởi động, bạn sẽ thấy trên terminal:

attacker-bot bắt đầu "dội bom" request vào Nginx.

security-watcher phân tích log và in ra thông báo phát hiện tấn công.

security-watcher thêm IP của bot vào danh sách đen và reload Nginx.

attacker-bot bắt đầu nhận mã lỗi 403 Forbidden thay vì 200 OK.

Bước 4: Dọn dẹp
Sau khi test xong, bạn có thể tắt và xóa các container bằng lệnh:

Bash
docker-compose down
⚠️ Cảnh báo
LƯU Ý: Hệ thống này được tạo ra HOÀN TOÀN VÌ MỤC ĐÍCH GIÁO DỤC (EDUCATIONAL PURPOSES ONLY). Vui lòng không sử dụng các script tấn công (attack.sh) lên các hệ thống thực tế hoặc các máy chủ mà bạn không có quyền sở hữu/được phép kiểm thử. Tác giả không chịu trách nhiệm cho bất kỳ hành vi lạm dụng công cụ nào vi phạm pháp luật.
