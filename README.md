# 🛡️ Telegram SOC Command Center: Hệ Thống Giám Sát n8n & Phòng Thủ Brute-Force

Một hệ thống lab giả lập bằng Docker chuyên dụng, biến **Telegram thành Trung tâm Điều hành An ninh mạng (SOC)**. Hệ thống kết hợp giữa phòng thủ chủ động bằng Python và tự động hóa cảnh báo bằng n8n, giúp quản trị viên giám sát Uptime từ đó chặn đứng các cuộc tấn công Brute-Force trực tiếp từ điện thoại.

## 💡 Giới thiệu Hệ Sinh Thái

Hệ thống được nâng cấp toàn diện với 2 luồng hoạt động chính, bổ trợ chặt chẽ cho nhau:
1. **🟢 Luồng Giám Sát Sức Khỏe (Uptime Monitoring bằng n8n):** Quản trị viên chủ động gõ lệnh `/healthy` trên Telegram. n8n sẽ đi "khám bệnh" server Nginx và báo cáo trạng thái (Sống/Chết) ngay lập tức.
2. **🔴 Luồng Phòng Thủ & Báo Động (Security IDS/IPS):** Script Python (`watcher.py`) liên tục quét log Nginx. Khi phát hiện IP có dấu hiệu quét lỗi 403 vượt ngưỡng, nó tự động khóa IP ở tầng Nginx, đồng thời kích hoạt Webhook của n8n để bắn **còi báo động khẩn cấp** về Telegram.

## 📂 Cấu trúc dự án

Dự án được quy hoạch chuẩn Microservices với 2 thư mục cốt lõi:

```text
He-Thong-Giam-Sat-SOC-n8n/
├── README.md
├── brute-force-defender/           # Hệ thống phòng thủ cốt lõi
│   ├── docker-compose.yml
│   ├── .env.example                # File mẫu cấu hình Token Telegram
│   ├── nginx-server/               # Web Server mục tiêu (Honeypot)
│   ├── security-watcher/           # Script Python phân tích log & gọi Webhook
│   └── attacker-bot/               # Script giả lập hacker (attack.sh)
└── n8n-monitoring/                 # Bộ não tự động hóa
    ├── n8n-health-check.json       # Sơ đồ n8n: Xử lý lệnh /healthy
    └── n8n-webhook-alert.json      # Sơ đồ n8n: Nhận báo động từ Python
```


## 🤖 PHẦN 1: HỆ THỐNG GIÁM SÁT & CẢNH BÁO (n8n Monitoring)

### 💡 Giới thiệu
Đây là "Bộ não" trung tâm của hệ thống, sử dụng nền tảng tự động hóa n8n để liên kết máy chủ với Telegram của Quản trị viên. Nó hoạt động với 2 nhiệm vụ song song: kiểm tra sức khỏe máy chủ chủ động và nhận báo động thụ động.

### ⚙️ Kiến trúc & Luồng hoạt động (Workflow)
1. **Luồng Giám Sát (Active Health Check):**
   - Quản trị viên gõ lệnh `/healthy` vào bot Telegram.
   - n8n nhận lệnh ➡️ Kích hoạt Node HTTP Request để "ping" tới trang chủ Nginx.
   - Trả về tin nhắn **Xanh 🟢** nếu server ổn định, hoặc **Đỏ 🔴** nếu Nginx sập (mất kết nối).
2. **Luồng Báo Động (Passive Alert):**
   - Lắng nghe Webhook 24/7 chờ tín hiệu từ hệ thống phòng thủ.
   - Ngay khi nhận được dữ liệu (POST request) báo cáo có IP bị khóa, n8n lập tức bắn tin nhắn 🚨 **BÁO ĐỘNG KHẨN** về Telegram.

### 🚀 Hướng dẫn Cài đặt & Sử dụng (n8n)

```bash
1) Cập nhật hệ thống và cài đặt Git, Curl
sudo apt-get update && sudo apt-get install -y git curl

2) Cài đặt Docker & Docker Compose tự động bằng Official Script
curl -fsSL [https://get.docker.com](https://get.docker.com) | sudo sh

3) Phân quyền để chạy Docker không cần gõ sudo liên tục
sudo usermod -aG docker $USER
newgrp docker
4) Tải toàn bộ mã nguồn hệ thống về máy
git clone [https://github.com/Dungsocool/He-Thong-Giam-Sat-SOC-n8n.git](https://github.com/Dungsocool/He-Thong-Giam-Sat-SOC-n8n.git)
cd He-Thong-Giam-Sat-SOC-n8n/
1)Mở Terminal của máy ảo và chạy lệnh sau để tải & khởi động máy chủ n8n (chạy ngầm):

sudo docker run -d --restart unless-stopped --name n8n -p 5678:5678 -v n8n_data:/home/node/.n8n docker.n8n.io/n8nio/n8n
2) Đăng nhập vào giao diện Web n8n


Gõ đường dẫn sau vào thanh địa chỉ: http://<IP_MÁY_ẢO_CỦA_BẠN>:5678
(Ví dụ nếu chạy local: http://localhost:5678 hoặc http://192.168.14.128:5678).


3) Import "Bản thiết kế" (File JSON)
Thay vì phải kéo thả, tự vẽ lại luồng từ đầu, bạn chỉ cần nạp 2 cấu hình đã được làm sẵn:

Tải 2 file .json nằm trong thư mục n8n-monitoring của kho GitHub này về máy tính.

Trên giao diện web n8n, nhìn sang menu bên trái, chọn Workflows ➡️ Bấm Add Workflow.

Nhìn lên góc trên cùng, bấm vào nút Menu (biểu tượng 3 dấu gạch ngang) ➡️ Chọn Import from File và tải lên lần lượt 2 file JSON đó.

4) Cấu hình định danh Bot Telegram
Để Bot biết phải gửi tin nhắn cho ai, bạn cần cấu hình lại 2 thông số sau trong các luồng vừa tải lên:

Click đúp vào các cục Node có tên Telegram.

Credential: Tạo mới kết nối và dán mã TELEGRAM_TOKEN của con Bot bạn đang quản lý vào.

Chat ID: Xóa dòng chữ DIEN_CHAT_ID_CUA_SEP_VAO_DAY và điền dãy số ID Telegram thật của bạn vào. ➡️ Bấm Save.

5) Kích hoạt & Lấy link Webhook

Gạt công tắc ở góc phải trên cùng của màn hình n8n sang trạng thái Active (công tắc chuyển màu xanh lá) cho cả 2 luồng.

Mở Node Webhook (trong luồng báo động), click đúp vào nó, chuyển sang tab Production URL.

```

## 🛡️ PHẦN 2: HỆ THỐNG PHÒNG THỦ (Brute-Force Defender)

## 💡 Giới thiệu

Hệ thống được thiết kế tối giản với 3 thành phần cốt lõi:
* **Nginx Server (Mục tiêu):** Web Server chạy honeypot, ghi nhận mọi truy cập rác vào file log.
* **Attacker Bot (Kẻ tấn công):** Script tự động liên tục "bắn" request lỗi vào server để giả lập tấn công.
* **Security Watcher (Phòng thủ & Cảnh báo):** Trái tim của hệ thống. Script Python quét log Nginx liên tục (real-time). Khi phát hiện IP có dấu hiệu tấn công, nó sẽ tự động khóa IP đó và **đặc biệt: bắn ngay một cảnh báo chi tiết về điện thoại của bạn qua Telegram**.

## ⚙️ Kiến trúc & Luồng hoạt động (Workflow)

1. **Ghi Log:** Attacker Bot gửi request -> Nginx Server trả lỗi 403/404 và ghi trực tiếp vào `access.log`.
2. **Đọc Log:** Security Watcher sử dụng kỹ thuật "tail -f" để quét file log theo thời gian thực.
3. **Block IP:** Nếu phát hiện 1 IP vi phạm vượt ngưỡng (ví dụ: 10 lỗi/phút), Watcher tự động ghi IP đó vào danh sách đen (`block_ips.conf`) và ép Nginx reload để cắt đứt kết nối.
4. **Báo động (Telegram):** Ngay khoảnh khắc IP bị block, Watcher sẽ gọi API để gửi tin nhắn thông báo khẩn cấp đến Telegram của quản trị viên.

## 📂 Cấu trúc dự án

```text
phongthu/
├── docker-compose.yml
├── README.md
├── .env                            # Lưu TELEGRAM_TOKEN và TELEGRAM_CHAT_ID
├── nginx-server/
│   ├── Dockerfile
│   └── nginx.conf
├── security-watcher/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── watcher.py                  # Script phân tích log & gửi Telegram
├── attacker-bot/
│   ├── Dockerfile
│   └── attack.sh
├── shared_logs/                    # Chứa access.log của Nginx
└── shared_config/
    └── block_ips.conf              # Danh sách IP bị chặn (ACL)

```

## 🚀 Hướng dẫn Cài đặt & Sử dụng

Để chạy được hệ thống, máy ảo của bạn cần có Git và Docker. Thay vì cài đặt thủ công phức tạp, hãy chạy lần lượt các lệnh tự động sau:

```bash
# 1. Cập nhật hệ thống và cài đặt Git, Curl
sudo apt-get update && sudo apt-get install -y git curl

# 2. Cài đặt Docker & Docker Compose tự động bằng Official Script
curl -fsSL https://get.docker.com | sudo sh

# 3. Phân quyền để chạy Docker không cần gõ sudo liên tục
sudo usermod -aG docker $USER
newgrp docker

4) git clone https://github.com/Dungsocool/brute-force-defender.git
1) cd brute-force-defender/

) sudo nano .env  # (Ghi chú: Điền TELEGRAM_TOKEN và TELEGRAM_CHAT_ID của bạn vào đây)

7) curl -s "https://api.telegram.org/bot<TOKEN_CUA_BAN>/sendMessage?chat_id=<ID_CUA_BAN>&text=Test_ket_noi_thanh_cong!"
        ( "Ping" thử Telegram    {"ok":true, "result":{...}}   là thành công )

8) sudo docker compose down && docker compose up --build

🧹 Dọn dẹp hệ thống (Reset)
Để tắt hệ thống và xóa sạch danh sách IP đã bị chặn (chuẩn bị cho lần test tiếp theo), hãy chạy 2 lệnh sau:

sudo docker-compose down

sudo sh -c 'echo -n > shared_config/block_ips.conf'

```

## 📸 Hình ảnh Demo
<img width="1613" height="545" alt="START" src="https://github.com/user-attachments/assets/0e488fc5-a659-4858-beb8-9cb1a7c6395b" />

<img width="1323" height="640" alt="gui request" src="https://github.com/user-attachments/assets/cb69633a-4412-4ab3-b54f-90b54717b179" />

<img width="1600" height="861" alt="1" src="https://github.com/user-attachments/assets/17428dc2-b4c3-44ed-ba1e-0e46b004838b" />
