import time
import json
import logging
import wakeonlan
import subprocess
from scapy.all import sniff, IP

# Load configuration from Home Assistant's UI options
CONFIG_FILE = "/data/options.json"
logging.basicConfig(level=logging.INFO)

last_wake_time = 0

def load_config():
    """Load user-configured settings from Home Assistant's UI."""
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Failed to load config: {e}")
        return None

def is_host_awake(target_ip):
    """Check if PC is already online using ping."""
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

def wake_device(mac_address, cooldown_seconds):
    """Send a Wake-on-LAN (WoL) packet if needed."""
    global last_wake_time
    current_time = time.time()

    if current_time - last_wake_time < cooldown_seconds:
        logging.info("Skipping WoL: Cooldown period active.")
        return

    if is_host_awake(mac_address):
        logging.info("Skipping WoL: PC is already online.")
        return

    logging.info(f"Sending WoL packet to {mac_address}")
    wakeonlan.send_magic_packet(mac_address)
    last_wake_time = current_time

def packet_callback(packet):
    """Check incoming packets and wake up PC if needed."""
    config = load_config()
    if not config:
        return

    target_ip = config["target_ip"]
    mac_address = config["mac_address"]
    cooldown_seconds = config.get("cooldown_seconds", 300)

    if packet.haslayer(IP) and packet[IP].dst == target_ip:
        logging.info(f"Network activity detected to {target_ip}")
        wake_device(mac_address, cooldown_seconds)

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
