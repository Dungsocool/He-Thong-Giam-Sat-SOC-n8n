# 🛡️ Telegram SOC Command Center: n8n Monitoring & Brute-Force Defense System

A dedicated Docker-based simulation lab that turns **Telegram into a Cyber Security Operations Center (SOC)**. The system combines proactive defense using Python with alerting automation using n8n, enabling administrators to monitor Uptime directly from their phone and completely shut down Brute-Force attacks.

# 📸 Video

https://drive.google.com/file/d/1AKJ5XQbnb54aVJU6TYBKPSRw9uGVZF_D/view?usp=sharing

## 💡 Ecosystem Introduction

The system is comprehensively upgraded with 2 core, mutually supporting workflows:
1. **🟢 Health Monitoring Workflow (Uptime Monitoring via n8n):** The administrator actively types the `/healthy` command on Telegram. n8n will perform a health check on the Nginx server and report its status (Up/Down) immediately. It will also immediately notify the Administrator when passively receiving alerts.
2. **🔴 Defense & Alerting Workflow (Security IDS/IPS):** A Python script (`watcher.py`) continuously scans Nginx logs. When it detects an IP demonstrating a pattern of exceeding the 403 error threshold, it automatically blocks the IP at the Nginx layer, while simultaneously triggering the n8n Webhook to fire an **emergency alarm** to Telegram.

## 📂 Project Structure

The project is structured following standard Microservices design with 2 core directories:

```text
He-Thong-Giam-Sat-SOC-n8n/
├── README.md
├── brute-force-defender/           # Core defense system
│   ├── docker-compose.yml
│   ├── .env.example                # Configuration template for Telegram Token
│   ├── nginx-server/               # Target Web Server (Honeypot)
│   ├── security-watcher/           # Python script to analyze logs & trigger Webhooks
│   └── attacker-bot/               # Script to simulate attackers (attack.sh)
└── n8n-monitoring/                 # Automation brain
    ├── n8n-health-check.json       # n8n diagram: Processing /healthy command
    └── n8n-webhook-alert.json      # n8n diagram: Receiving alerts from Python
```


## 🤖 PART 1: AUTOMATION & ALERT SYSTEM (n8n Monitoring)

### 💡 Introduction
This is the central "Brain" of the system, leveraging the n8n automation platform to link the server with the Administrator's Telegram. It functions with two parallel tasks: active server health checks and passive alert reception, immediately notifying the Administrator.

### ⚙️ Architecture & Workflow
1. **Active Health Check Workflow:**
   - The administrator types the `/healthy` command in the Telegram bot.
   - n8n receives the command ➡️ Triggers the HTTP Request Node to "ping" the Nginx homepage.
   - Returns a green message **🟢** if the server is stable, or a red message **🔴** if Nginx is down (connection lost).
2. **Passive Alert Workflow:**
   - Listens to the Webhook 24/7 waiting for signals from the defense system.
   - The moment data (POST request) reporting a blocked IP is received, n8n immediately fires an 🚨 **URGENT ALARM** message to Telegram.

### 🚀 Installation & Usage Guide (n8n)

```bash
# 1) Update the system and install Git, Curl
sudo apt-get update && sudo apt-get install -y git curl

# 2) Automatically install Docker & Docker Compose using the Official Script
curl -fsSL https://get.docker.com | sudo sh

# 3) Grant permissions to run Docker without typing sudo repeatedly
sudo usermod -aG docker $USER
newgrp docker

# 4) Clone the repository
git clone https://github.com/Dungsocool/He-Thong-Giam-Sat-SOC-n8n
cd He-Thong-Giam-Sat-SOC-n8n/n8n-monitoring

# 5) Install NodeJS and nport
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
sudo npm install -g nport

# 6) Open a parallel Terminal and run
sudo nport 5678 -s your-soc-n8n

# 7) Start n8n container
sudo docker compose up -d

# 8) Log in to the n8n Web interface
# (You can modify the username in /He-Thong-Giam-Sat-SOC-n8n/n8n-monitoring/docker-compose.yml)
# Visit: https://your-soc-n8n.nport.link

# 9) Import "Blueprints" (JSON Files)
# Instead of dragging, dropping, and drawing the workflow from scratch, you can simply load the pre-built configuration:
# Download the .json files located in the n8n-monitoring directory of this GitHub repo to your computer.
# On the n8n web interface, go to the left menu, select Workflows ➡️ Click Add Workflow.
# Look at the top right corner, click on the Menu button (3 horizontal lines icon) ➡️ Select Import from File and upload those JSON files one by one.

# 10) Configure Telegram Bot Credentials
# For the Bot to know who to send messages to, you need to configure 2 parameters in the imported workflows:
# Double click on the Nodes named Telegram.
# Credential: Create a new connection and paste your Bot's TELEGRAM_TOKEN.
# Chat ID: Delete the placeholder text and enter your real Telegram Chat ID. ➡️ Click Save.

# 11) Activate & Obtain Webhook Link
# Toggle the switch in the top right corner of the n8n screen to Active (switch turns green) for both workflows.
# Open the Webhook Node (in the alert workflow), double click it, and switch to the Production URL tab.
```

## 📸 Demo Images
<img width="1919" height="817" alt="image" src="https://github.com/user-attachments/assets/a2b96f34-dce8-451f-b404-dc3411669e44" />
<img width="1625" height="228" alt="image" src="https://github.com/user-attachments/assets/b68dd3c2-1311-44c6-bca7-d26e84ab3978" />
<img width="1844" height="987" alt="image" src="https://github.com/user-attachments/assets/bcf86de0-3f2e-4835-929a-2daf2568aeb4" />

<img width="1915" height="1079" alt="image" src="https://github.com/user-attachments/assets/db28a2c0-3329-4c3e-9374-7ec2f017cde4" />

# 🎯 Testing the System

After the n8n system is live with your NPort link, it's time to "test fire" and see if the alert workflow runs smoothly!

**🚀 Test 1: Simulating an Alert Using curl**
```bash
curl -X POST <YOUR_PRODUCTION_URL>
```
<img width="1912" height="924" alt="image" src="https://github.com/user-attachments/assets/7aa66c1f-bedf-43f6-86e2-7288c2854687" />
*Replace `<YOUR_PRODUCTION_URL>` with your actual Production URL.*

🎉 Immediately, your phone will vibrate with an alert message. If you receive the message, congratulations, your Core system is working perfectly!
<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/41ebb722-37d0-41aa-808b-4e95d97be8f5" />

**🚧 Test 2: Typing `/healthy` to Check Nginx (Awaiting Part 2 to Complete)**
In the Monitor Workflow you just imported, there is a very cool feature: whenever you open Telegram and type `/healthy`, n8n will check if the Nginx server is alive.

What will you see if you try it right now?
Since we haven't installed Nginx in Part 1 yet, n8n won't find the server. It will immediately take the Error branch and send you a Red message 🔴:
`🔴 URGENT ALARM: Nginx is not responding (Connection Lost)!`
<img width="887" height="886" alt="image" src="https://github.com/user-attachments/assets/72c16c28-cab0-4e96-b738-6a114f6c7a74" />
👉 Don't worry, this is a SUCCESSFUL test! It proves that n8n's error reporting branch is extremely sensitive.

How to get a Green message 🟢?
To make the system complete and have `/healthy` return a normal status (Server running well), we need to set up a Reverse Proxy.
⏩ See you in Part 2: Installing Nginx & Optimizing the SOC Workflow!

---

## 🛡️ PART 2: DEFENSE SYSTEM (Brute-Force Defender)

## 💡 Introduction

The system is designed to be minimalist with 3 core components:
* **Nginx Server (Target):** Web Server running a honeypot, logging all junk traffic to the access log.
* **Attacker Bot (Attacker):** An automated script continuously "firing" failing requests at the server to simulate an attack.
* **Security Watcher (Defense & Alerting):** The heart of the system. A Python script that scans Nginx logs continuously in real-time. When it detects an IP showing signs of an attack, it automatically blocks that IP and, **most importantly: instantly fires a detailed alert to your phone via Telegram**.

## ⚙️ Architecture & Workflow

1. **Log Recording:** The Attacker Bot sends requests -> The Nginx Server returns a 403/404 error and logs directly into `access.log`.
2. **Log Reading:** The Security Watcher uses the "tail -f" technique to scan log files in real-time.
3. **Block IP:** If an IP is found violating a threshold (e.g., 10 errors/minute), the Watcher automatically writes that IP to a blacklist (`block_ips.conf`) and forces Nginx to reload to cut off the connection.
4. **Alert (Telegram):** The exact moment an IP is blocked, the Watcher calls the API to send an emergency notification to the administrator's Telegram.

## 📂 Project Structure

```text
phongthu/
├── docker-compose.yml
├── README.md
├── .env                            # Saves TELEGRAM_TOKEN and TELEGRAM_CHAT_ID
├── nginx-server/
│   ├── Dockerfile
│   └── nginx.conf
├── security-watcher/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── watcher.py                  # Script for log analysis & Telegram alerting
├── attacker-bot/
│   ├── Dockerfile
│   └── attack.sh
├── shared_logs/                    # Contains Nginx's access.log
└── shared_config/
    └── block_ips.conf              # Blocked IP list (ACL)
```

## 🚀 Installation & Usage Guide

To run the system, your virtual machine needs to have Git and Docker installed. Instead of complex manual setups, run the following automated commands in sequence:

```bash
# 1) Navigate to the defender directory
cd  ~/He-Thong-Giam-Sat-SOC-n8n/brute-force-defender

# 2) Edit env file
sudo nano .env  # (Note: Enter your TELEGRAM_TOKEN and TELEGRAM_CHAT_ID here)

# 3) Test Telegram connection
curl -s "https://api.telegram.org/bot<YOUR_TOKEN>/sendMessage?chat_id=<YOUR_ID>&text=Test_connection_successful!"
# (Telegram "Ping" test: {"ok":true, "result":{...}} means successful)

# 4) Start the environment
sudo docker compose down && docker compose up --build
```

### 🧹 System Cleanup (Reset)
To shut down the system and clear all blocked IP lists (preparing for the next test run), execute these 2 commands:

```bash
sudo docker-compose down
sudo sh -c 'echo -n > shared_config/block_ips.conf'
```

## 📸 Demo Images
<img width="1919" height="1041" alt="image" src="https://github.com/user-attachments/assets/6c0a336c-4c77-4de6-bd4a-a274dd401c18" />

<img width="1613" height="545" alt="START" src="https://github.com/user-attachments/assets/0e488fc5-a659-4858-beb8-9cb1a7c6395b" />

<img width="1323" height="640" alt="gui request" src="https://github.com/user-attachments/assets/cb69633a-4412-4ab3-b54f-90b54717b179" >

<img width="1919" height="1044" alt="image" src="https://github.com/user-attachments/assets/e2af69b3-ca7a-4aae-9068-e9c1274b906c" />

<img width="830" height="156" alt="image" src="https://github.com/user-attachments/assets/0a04adea-36f7-4349-bab3-1a425a4e803b" />

---

## 🎯 COMPREHENSIVE TEST: "TEST FIRING" THE SOC SYSTEM 🚀

Now your system is fully equipped: **n8n** (Core processor), **NPort** (Internet tunnel), and **Nginx** (Reverse Proxy shield). Let's run a real-world test scenario to see the magic of automation!

## 🟢 Scenario 1: Proactive Monitoring (Ping Health Check)
Instead of waiting for errors to occur, a great SOC actively "diagnoses" the system's health. We will use the Telegram Bot to check the status of the Nginx server.

**Before testing, make sure your Nginx environment is "clean" and n8n can connect easily. Complete the following preparation steps:**

```bash
sudo sh -c 'echo -n > shared_config/block_ips.conf'
```

By default, Nginx returns a 403 error if the web directory is empty. Let's create a default file so that when n8n performs its health check, Nginx returns a `200 OK` status (confirming system health):

```bash
echo "He thong phong thu dang hoat dong!" > ~/He-Thong-Giam-Sat-SOC-n8n/brute-force-defender/nginx-server/html/index.html
sudo docker ps # (Check Nginx service status)
sudo docker restart demo_nginx_server # (Restart Nginx service)
```

**Execution:** Pick up your phone, open your chat with the Telegram Bot, and type the command:
`/healthy`

**Result:** At this point, n8n automatically runs the Monitor workflow, immediately checking Nginx. Since Nginx is running extremely smoothly, n8n returns a reassuring message:
`🟢: HEALTHY Status OK! Nginx system is running smoothly`

<img width="1552" height="176" alt="image" src="https://github.com/user-attachments/assets/1edd85a8-62a4-48a4-bcd9-22da3a471c11" />
<img width="1919" height="1042" alt="image" src="https://github.com/user-attachments/assets/ec11645b-8ec2-48c7-b795-92486e088a0a" />

---

## 🔴 Scenario 2: "Pulling the Plug" - Simulating Server Outage (Server Down)
To test the responsiveness of the system during a network incident, we will manually stop the Nginx server.

**Pulling the Plug on Nginx:** Open MobaXterm and run the command to abruptly stop the Nginx server:
```bash
sudo docker stop demo_nginx_server
```

**Check Response:** Pick up your phone and type the command `/healthy` again.

**Result:** Immediately, n8n cannot find Nginx. It redirects the workflow path to the Error state and sounds the alarm:
`🔴: URGENT ALARM: Nginx is not responding (Connection Lost)!`

<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/b3a89368-6522-41e8-9ee3-c5bc3cb095ea" />

**Reviving the Server:**
```bash
sudo docker start demo_nginx_server
```

Type `/healthy` on Telegram again, and you'll see it turn green 🟢 once more.
<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/0c0a3be7-96a9-4d4e-85c3-19a37107047a" />
