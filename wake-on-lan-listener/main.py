import time
import json
import logging
import wakeonlan
import subprocess
from scapy.all import sniff, IP

# Load configuration
CONFIG_FILE = "/data/options.json"
logging.basicConfig(level=logging.INFO)

# Cooldown time in seconds
COOLDOWN_TIME = 300  # 5 minutes
last_wake_time = 0

def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Failed to load config: {e}")
        return None

def is_host_awake(target_ip):
    """Check if the GameStreamNAS is awake using ping."""
    try:
        result = subprocess.run(
            ["ping", "-c", "1", target_ip],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return result.returncode == 0
    except Exception as e:
        logging.error(f"Ping error: {e}")
        return False

def wake_device(mac_address):
    """Send a WoL packet to the GameStreamNAS."""
    global last_wake_time
    current_time = time.time()

    if current_time - last_wake_time < COOLDOWN_TIME:
        logging.info("Skipping WoL: Cooldown period active.")
        return

    if is_host_awake(mac_address):
        logging.info("Skipping WoL: GameStreamNAS is already online.")
        return

    logging.info(f"Sending WoL packet to {mac_address}")
    wakeonlan.send_magic_packet(mac_address)
    last_wake_time = current_time

def packet_callback(packet):
    """Handle detected network packets."""
    config = load_config()
    if not config:
        return

    target_ip = config["target_ip"]
    mac_address = config["mac_address"]

    if packet.haslayer(IP) and packet[IP].dst == target_ip:
        logging.info(f"Network activity detected to {target_ip}")
        wake_device(mac_address)

def main():
    config = load_config()
    if not config:
        logging.error("No valid config found. Exiting.")
        return

    network_interface = config["network_interface"]
    logging.info(f"Listening for packets on {network_interface}...")

    sniff(iface=network_interface, filter=f"dst host {config['target_ip']}", prn=packet_callback, store=0)

if __name__ == "__main__":
    main()
