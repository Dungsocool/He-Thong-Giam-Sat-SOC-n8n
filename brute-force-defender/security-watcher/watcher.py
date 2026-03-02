import os
import time
import re
import logging
import docker
import requests
from collections import defaultdict, deque

# ==========================================
# CAU HINH HE THONG
# ==========================================
LOG_FILE = "/var/log/nginx/access.log"
BLOCK_FILE = "/etc/nginx/block_ips.conf"
NGINX_CONTAINER = "demo_nginx_server"

THRESHOLD = 10          
WINDOW_SIZE = 60        
TARGET_STATUS = "403"   

# Doc bien tu .env
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

try:
    docker_client = docker.from_env()
    logger.info("Ket noi Docker Socket thanh cong.")
except Exception as e:
    logger.error(f"Khong the ket noi Docker Socket: {e}")
    exit(1)

failed_attempts = defaultdict(deque)
blocked_ips_cache = set()

def load_blocked_ips_to_memory():
    if os.path.exists(BLOCK_FILE):
        with open(BLOCK_FILE, 'r') as f:
            for line in f:
                match = re.search(r'deny\s+([0-9\.]+);', line)
                if match:
                    blocked_ips_cache.add(match.group(1))
    logger.info(f"Da nap {len(blocked_ips_cache)} IP vao RAM.")

def send_telegram_alert(ip):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        logger.error("DEBUG: Thieu Token/ChatID trong file .env")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": f"🚨 [CANH BAO] Da chan IP: {ip}\nLy do: Brute Force Honeypot."
    }
    
    logger.info(f"--- Bat dau gui tin Telegram cho IP {ip} ---")
    try:
        res = requests.post(url, json=payload, timeout=10)
        logger.info(f"Status Code: {res.status_code}")
        logger.info(f"Response Body: {res.text}")
        if res.status_code == 200:
            logger.info("Gui Telegram THANH CONG!")
        else:
            logger.error("Gui Telegram THAT BAI! Kiem tra Token/ChatID.")
    except Exception as e:
        logger.error(f"LOI KET NOI TELEGRAM: {e}")
    logger.info("--- Ket thuc luong Telegram ---")

def block_ip(ip):
    if ip in blocked_ips_cache:
        return

    logger.warning(f"PHAT HIEN TAN CONG: Dang chan IP {ip}...")
    try:
        with open(BLOCK_FILE, 'a') as f:
            f.write(f"deny {ip};\n")
        blocked_ips_cache.add(ip)
    except Exception as e:
        logger.error(f"Loi ghi file: {e}")
        return

    try:
        container = docker_client.containers.get(NGINX_CONTAINER)
        if container.exec_run("nginx -s reload").exit_code == 0:
            logger.info(f"Da reload Nginx. IP {ip} da bi khoa.")
            send_telegram_alert(ip)
            # === 2 DÒNG BẠN CẦN CHÈN THÊM VÀO ĐÂY ===
            webhook_url = "https://dung-n8n-lab.nport.link/webhook/Canh-Bao-Attack"
            os.system(f'curl -s -X POST {webhook_url}')
            # ========================================
    except Exception as e:
        logger.error(f"Loi Docker Exec: {e}")

def monitor_logs():
    load_blocked_ips_to_memory()
    while not os.path.exists(LOG_FILE):
        logger.info("Dang cho file log...")
        time.sleep(2)
        
    f = open(LOG_FILE, 'r')
    f.seek(0, 2)
    current_inode = os.stat(LOG_FILE).st_ino
    log_pattern = re.compile(r'^(\S+) - - \[.*?\] ".*?" (\d{3})')
    logger.info("Bat dau quet log thoi gian thuc...")

    while True:
        line = f.readline()
        if not line:
            try:
                if os.stat(LOG_FILE).st_ino != current_inode:
                    logger.warning("Log rotated. Mo lai file moi.")
                    f.close()
                    f = open(LOG_FILE, 'r')
                    current_inode = os.stat(LOG_FILE).st_ino
                    continue
            except: pass
            time.sleep(0.1)
            continue
            
        match = log_pattern.search(line)
        if match:
            ip, status = match.group(1), match.group(2)
            if status == TARGET_STATUS:
                now = time.time()
                failed_attempts[ip].append(now)
                while failed_attempts[ip] and failed_attempts[ip][0] < now - WINDOW_SIZE:
                    failed_attempts[ip].popleft()
                
                count = len(failed_attempts[ip])
                logger.info(f"IP {ip} -> Loi {status} ({count}/{THRESHOLD})")
                if count >= THRESHOLD:
                    block_ip(ip)
                    failed_attempts[ip].clear()

if __name__ == "__main__":
    monitor_logs()
