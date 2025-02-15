#!/usr/bin/with-contenv bash
set -e

echo "Starting Wake-on-LAN Listener add-on..."

# Run the main Python script under the correct user
exec s6-setuidgid root python3 /app/main.py
