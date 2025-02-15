#!/bin/bash
set -e

echo "Starting Wake-on-LAN Listener add-on..."

# Run the main Python script
exec python3 /app/main.py
