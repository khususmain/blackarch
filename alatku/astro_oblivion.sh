#!/bin/bash

# ASTRO OBLIVION PROTOCOL (TIER 5)
# This script performs aggressive anti-forensics cleaning.

echo "[*] INITIATING OBLIVION PROTOCOL..."

# 1. Clear Bash History from memory and disk
history -c
rm -f ~/.bash_history
touch ~/.bash_history
ln -sf /dev/null ~/.bash_history

# 2. Shred Logs (Overwrite 3 times with random data)
echo "[*] Shredding logs..."
find /var/log -type f -name "*.log" -exec shred -u -n 3 {} \; 2>/dev/null
find /tmp -type f -name "*.log" -exec shred -u -n 3 {} \; 2>/dev/null

# 3. Clear Temp Directories (Safe Mode)
rm -rf /tmp/tmp* 2>/dev/null
rm -rf /var/tmp/* 2>/dev/null

# 4. Timestomping (Set all files in workspace to a generic past date)
# This confuses timeline analysis.
echo "[*] Timestomping artifacts..."
find /workspaces/blackarch -exec touch -d "2022-01-01 00:00:00" {} \; 2>/dev/null

# 5. Lock Critical Files (Immutable)
# Note: May require privileged container mode
# chattr +i /workspaces/blackarch/astro_sentinel.py 2>/dev/null

echo "[+] OBLIVION COMPLETE. SYSTEM CLEAN."
