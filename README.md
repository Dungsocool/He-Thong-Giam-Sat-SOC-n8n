# 🛡️ Telegram SOC Command Center: Hệ Thống Giám Sát n8n & Phòng Thủ Brute-Force

Một hệ thống lab giả lập bằng Docker chuyên dụng, biến **Telegram thành Trung tâm Điều hành An ninh mạng (SOC)**. Hệ thống kết hợp giữa phòng thủ chủ động bằng Python và tự động hóa cảnh báo bằng n8n, giúp quản trị viên giám sát Uptime trực tiếp từ điện thoại từ đó chặn đứng các cuộc tấn công Brute-Force .

# 🛡️ Video

https://drive.google.com/file/d/1AKJ5XQbnb54aVJU6TYBKPSRw9uGVZF_D/view?usp=sharing

## 💡 Giới thiệu Hệ Sinh Thái

Hệ thống được nâng cấp toàn diện với 2 luồng hoạt động chính, bổ trợ chặt chẽ cho nhau:
1. **🟢 Luồng Giám Sát Sức Khỏe (Uptime Monitoring bằng n8n):** Quản trị viên chủ động gõ lệnh `/healthy` trên Telegram. n8n sẽ đi "khám bệnh" server Nginx và báo cáo trạng thái (Sống/Chết) ngay lập tức. Khi thụ động nhận cảnh báo lập tức sẽ báo cho Quản trị viên .
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
Đây là "Bộ não" trung tâm của hệ thống, sử dụng nền tảng tự động hóa n8n để liên kết máy chủ với Telegram của Quản trị viên. Nó hoạt động với 2 nhiệm vụ song song: kiểm tra sức khỏe máy chủ chủ động và nhận báo động thụ động , lập tức báo cho Quản trị viên .

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
curl -fsSL https://get.docker.com | sudo sh
3) Phân quyền để chạy Docker không cần gõ sudo liên tục
sudo usermod -aG docker $USER
newgrp docker
4) Tải toàn bộ mã nguồn hệ thống về máy
git clone https://github.com/Dungsocool/He-Thong-Giam-Sat-SOC-n8n
5) cd He-Thong-Giam-Sat-SOC-n8n/n8n-monitoring
6)curl -fsSL [https://deb.nodesource.com/setup_20.x](https://deb.nodesource.com/setup_20.x) | sudo -E bash -
sudo apt-get install -y nodejs
sudo npm install -g nport
7) Mở 1 Terminal chạy song song
sudo nport 5678 -s soc-n8n-cua-ban
8)
sudo docker compose up -d
9) Sau bước 7, 8 đăng nhập vào giao diện Web n8n
(bạn có thể sửa tên đăng nhập trong /He-Thong-Giam-Sat-SOC-n8n/n8n-monitoring/docker-compose.yml )
https://soc-n8n-cua-ban.nport.link
10) Import "Bản thiết kế" (File JSON)
Thay vì phải kéo thả, tự vẽ lại luồng từ đầu, bạn chỉ cần nạp cấu hình đã được làm sẵn:
Tải .json nằm trong thư mục n8n-monitoring của kho GitHub này về máy tính.
Trên giao diện web n8n, nhìn sang menu bên trái, chọn Workflows ➡️ Bấm Add Workflow.
Nhìn lên góc trên cùng, bấm vào nút Menu (biểu tượng 3 dấu gạch ngang) ➡️ Chọn Import from File và tải lên lần lượt  file JSON đó.

11) Cấu hình định danh Bot Telegram
Để Bot biết phải gửi tin nhắn cho ai, bạn cần cấu hình lại 2 thông số sau trong các luồng vừa tải lên:
Click đúp vào các cục Node có tên Telegram.
Credential: Tạo mới kết nối và dán mã TELEGRAM_TOKEN của con Bot bạn đang quản lý vào.
Chat ID: Xóa dòng chữ DIEN_CHAT_ID và điền dãy số ID Telegram thật của bạn vào. ➡️ Bấm Save.

12) Kích hoạt & Lấy link Webhook
Gạt công tắc ở góc phải trên cùng của màn hình n8n sang trạng thái Active (công tắc chuyển màu xanh lá) cho cả 2 luồng.
Mở Node Webhook (trong luồng báo động), click đúp vào nó, chuyển sang tab Production URL.

```
## 📸 Hình ảnh Demo
<img width="1919" height="817" alt="image" src="https://github.com/user-attachments/assets/a2b96f34-dce8-451f-b404-dc3411669e44" />
<img width="1625" height="228" alt="image" src="https://github.com/user-attachments/assets/b68dd3c2-1311-44c6-bca7-d26e84ab3978" />
<img width="1844" height="987" alt="image" src="https://github.com/user-attachments/assets/bcf86de0-3f2e-4835-929a-2daf2568aeb4" />

<img width="1915" height="1079" alt="image" src="https://github.com/user-attachments/assets/db28a2c0-3329-4c3e-9374-7ec2f017cde4" />

# 🎯 Kiểm tra hoạt động của hệ thống (Testing)

Sau khi hệ thống n8n đã lên sóng với đường link NPort xịn sò, giờ là lúc chúng ta "thử lửa" xem luồng cảnh báo có thực sự chạy mượt mà không nhé!


**🚀 Bài Test 1: Bắn cảnh báo giả lập bằng curl** 
curl -X POST <> 
<img width="1912" height="924" alt="image" src="https://github.com/user-attachments/assets/7aa66c1f-bedf-43f6-86e2-7288c2854687" />
Thay  <> bằng Production URL của bạn .
🎉 Ngay lập tức, điện thoại của bạn sẽ rung lên với tin nhắn cảnh báo. Nếu bạn nhận được tin nhắn, xin chúc mừng, hệ thống Core của bạn đã hoạt động hoàn hảo!
<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/41ebb722-37d0-41aa-808b-4e95d97be8f5" />



**🚧 Bài Test 2: Gõ lệnh /healthy kiểm tra Nginx (Chờ Phần 2 để hoàn thiện)**
Trong luồng giám sát (Monitor Workflow) bạn vừa import, có một tính năng rất ngầu: Hễ bạn mở Telegram gõ lệnh /healthy, n8n sẽ đi kiểm tra xem máy chủ Nginx có đang sống không.

Thử ngay bây giờ bạn sẽ thấy gì?
Vì ở Phần 1 này chúng ta chưa hề cài đặt Nginx, nên n8n sẽ không tìm thấy server. Nó sẽ lập tức rẽ sang nhánh Lỗi và bắn cho bạn một tin nhắn Màu Đỏ 🔴:
🔴 BÁO ĐỘNG KHẨN Nginx không phản hồi (Mất kết nối)!
<img width="887" height="886" alt="image" src="https://github.com/user-attachments/assets/72c16c28-cab0-4e96-b738-6a114f6c7a74" />
👉 Đừng lo lắng, đây là một bài test THÀNH CÔNG! Nó chứng tỏ nhánh báo lỗi của n8n hoạt động cực kỳ nhạy bén.
Làm sao để có tin nhắn Màu Xanh 🟢?
Để hệ thống hoàn chỉnh và gõ /healthy trả về trạng thái bình thường (Server đang chạy tốt), chúng ta cần thiết lập Reverse Proxy.
⏩ Hẹn gặp lại các bạn ở Phần 2: Cài đặt Nginx & Tối ưu luồng SOC nhé!
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

1) cd  ~/He-Thong-Giam-Sat-SOC-n8n/brute-force-defender

2) sudo nano .env  # (Ghi chú: Điền TELEGRAM_TOKEN và TELEGRAM_CHAT_ID của bạn vào đây)

3) curl -s "https://api.telegram.org/bot<TOKEN_CUA_BAN>/sendMessage?chat_id=<ID_CUA_BAN>&text=Test_ket_noi_thanh_cong!"
        ( "Ping" thử Telegram    {"ok":true, "result":{...}}   là thành công )

4) sudo docker compose down && docker compose up --build

🧹 Dọn dẹp hệ thống (Reset)
Để tắt hệ thống và xóa sạch danh sách IP đã bị chặn (chuẩn bị cho lần test tiếp theo), hãy chạy 2 lệnh sau:

sudo docker-compose down

sudo sh -c 'echo -n > shared_config/block_ips.conf'

```

## 📸 Hình ảnh Demo
<img width="1919" height="1041" alt="image" src="https://github.com/user-attachments/assets/6c0a336c-4c77-4de6-bd4a-a274dd401c18" />


<img width="1613" height="545" alt="START" src="https://github.com/user-attachments/assets/0e488fc5-a659-4858-beb8-9cb1a7c6395b" />

<img width="1323" height="640" alt="gui request" src="https://github.com/user-attachments/assets/cb69633a-4412-4ab3-b54f-90b54717b179" >

<img width="1919" height="1044" alt="image" src="https://github.com/user-attachments/assets/e2af69b3-ca7a-4aae-9068-e9c1274b906c" />

<img width="830" height="156" alt="image" src="https://github.com/user-attachments/assets/0a04adea-36f7-4349-bab3-1a425a4e803b" />



## 🎯 BÀI KIỂM TRA TOÀN DIỆN: "THỬ LỬA" HỆ THỐNG SOC 🚀

Bây giờ hệ thống của bạn đã được trang bị đầy đủ: **n8n** (Core xử lý), **NPort** (Đường hầm Internet) và **Nginx** (Lá chắn Reverse Proxy). Hãy cùng chạy kịch bản test thực tế dưới đây để thấy sự kỳ diệu của tự động hóa nhé!

## 🟢 Kịch bản 1: Giám sát chủ động (Ping Health Check)
Thay vì ngồi chờ lỗi xảy ra, SOC xịn là phải biết tự đi "khám bệnh" hệ thống. Chúng ta sẽ dùng Bot Telegram để hỏi thăm sức khỏe của máy chủ Nginx.
**Trước khi tiến hành kiểm thử, bạn cần đảm bảo môi trường Nginx "sạch" và n8n có thể kết nối thuận lợi. Hãy thực hiện các bước chuẩn bị sau:**

sudo sh -c 'echo -n > shared_config/block_ips.conf'

Mặc định Nginx sẽ báo lỗi 403 nếu thư mục web trống. Hãy tạo một file mặc định để khi n8n kiểm tra (Health check), Nginx sẽ trả về mã 200 OK (xác nhận hệ thống khỏe mạnh):

echo "He thong phong thu dang hoat dong!" > ~/He-Thong-Giam-Sat-SOC-n8n/brute-force-defender/nginx-server/html/index.html
sudo docker ps ( kiểm tra dịch vụ nginx)
sudo docker restart demo_nginx_server (khởi động lại dịch vụ nginx)

Thực hiện: Cầm điện thoại lên, mở đoạn chat với Bot Telegram của bạn và gõ lệnh:
/healthy

Kết quả: Lúc này, n8n sẽ tự động chạy luồng Monitor, "chạy ù" ra kiểm tra Nginx. Vì Nginx của chúng ta đang hoạt động cực kỳ mượt mà, n8n sẽ trả về cho bạn một tin nhắn an tâm:
🟢: HEALTHY Trạng thái OK! Hệ thống Nginx đang chạy mượt mà
<img width="1552" height="176" alt="image" src="https://github.com/user-attachments/assets/1edd85a8-62a4-48a4-bcd9-22da3a471c11" />

<img width="1919" height="1042" alt="image" src="https://github.com/user-attachments/assets/ec11645b-8ec2-48c7-b795-92486e088a0a" />


## 🔴 Kịch bản 2: "Rút phích cắm" - Giả lập Server Sập (Server Down)
Bài test để xem độ nhạy bén của hệ thống khi có biến cố mạng, chúng ta sẽ tự tay tắt con server Nginx.
Rút phích cắm Nginx: Mở MobaXterm và gõ lệnh tắt server Nginx đột ngột:

Bash
sudo docker stop demo_nginx_server

Kiểm tra phản ứng: Cầm điện thoại lên và gõ lại lệnh /healthy.
Kết quả: Ngay lập tức, n8n không tìm thấy Nginx. Nó sẽ rẽ nhánh luồng dữ liệu sang trạng thái Error và hú còi báo động:
🔴: BÁO ĐỘNG KHẨN Nginx không phản hồi (Mất kết nối)!
<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/b3a89368-6522-41e8-9ee3-c5bc3cb095ea" />


Cứu sống lại (Hồi sinh): 

Bash
sudo docker start demo_nginx_server

Gõ lại /healthy trên Telegram, bạn sẽ thấy nó xanh 🟢 trở lại. 
<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/0c0a3be7-96a9-4d4e-85c3-19a37107047a" />

