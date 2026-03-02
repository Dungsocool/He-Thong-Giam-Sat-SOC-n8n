#!/bin/bash

# Vi dung network_mode: host, bot goi qua localhost port 8080 cua may ao
HONEYPOT_URL="http://localhost:8080/admin-login"
HOME_URL="http://localhost:8080/"

echo "============================================="
echo "[*] ATTACKER BOT DANG KHOI DONG..."
echo "============================================="
sleep 3 

count=1
while true; do
    STATUS_HONEYPOT=$(curl -s -o /dev/null -w "%{http_code}" "$HONEYPOT_URL")
    STATUS_HOME=$(curl -s -o /dev/null -w "%{http_code}" "$HOME_URL")
    
    if [ "$STATUS_HOME" = "200" ]; then
        echo "[$count] Honeypot: $STATUS_HONEYPOT | Trang chu: $STATUS_HOME (Chua bi chan)"
    elif [ "$STATUS_HOME" = "403" ]; then
        echo "[$count] Honeypot: $STATUS_HONEYPOT | Trang chu: $STATUS_HOME (DA BI BLOCK!)"
    else
        echo "[$count] Dang ket noi..."
    fi

    count=$((count + 1))
    sleep 0.2
done
