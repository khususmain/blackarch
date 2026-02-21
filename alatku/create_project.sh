#!/bin/bash
PROJECT_NAME=$1
GDRIVE_PATH="/workspaces/blackarch/gdrive/HACKING"

if [ -z "$PROJECT_NAME" ]; then
    echo -e "\e[31m[-] Usage: ./create_project.sh <project_name>\e[0m"
    exit 1
fi

TARGET_DIR="$GDRIVE_PATH/$PROJECT_NAME"

echo -e "\e[32m[+] [ASTRO] Initializing project: $PROJECT_NAME\e[0m"

if [ ! -d "$TARGET_DIR" ]; then
    mkdir -p "$TARGET_DIR/scans"
    mkdir -p "$TARGET_DIR/exploits"
    mkdir -p "$TARGET_DIR/loot"
    echo -e "\e[32m[+] Project structure created at: $TARGET_DIR\e[0m"
else
    echo -e "\e[33m[!] Project directory already exists.\e[0m"
fi

# Create a local symlink for easy access
if [ ! -L "$PROJECT_NAME" ]; then
    ln -s "$TARGET_DIR" "$PROJECT_NAME"
    echo -e "\e[32m[+] Symlink created: ./$PROJECT_NAME -> $TARGET_DIR\e[0m"
fi

echo -e "\n\e[34m[STATUS REPORT]\e[0m"
ls -R "$TARGET_DIR"
echo -e "\e[32m[+] Project $PROJECT_NAME is ready for deployment.\e[0m"
