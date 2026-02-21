#!/bin/bash
# find_origin.sh - ASTRO Origin IP Hunter
TARGET="tv8.lk21official.cc"
# Potential IPs from Censys/Passive DNS
IP_LIST="104.21.59.235 172.67.185.109"

echo "[*] TARGET: $TARGET"
echo "[*] Starting Origin Scan..."

for IP in $IP_LIST; do
    echo -n "[*] Testing $IP... "
    # Send request with Host Header directly to the IP
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" -k -H "Host: $TARGET" https://$IP/ --connect-timeout 5)

    if [ "$STATUS" == "200" ] || [ "$STATUS" == "301" ]; then
        echo -e "
[+] POTENTIAL ORIGIN FOUND: $IP (Status: $STATUS)"
        echo " -> Access: https://$IP/ (Accept Cert Risk)"
    else
        echo "[-] GUARDED (Status: $STATUS)"
    fi
done
