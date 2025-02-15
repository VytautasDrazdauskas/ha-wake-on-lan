import time
import json
import logging
import wakeonlan
import subprocess
import psutil
import shutil
from scapy.all import sniff, IP

# Load configuration
CONFIG_FILE = "/data/options.json"
logging.basicConfig(level=logging.INFO)

last_wake_time = 0

def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Failed to load config: {e}")
        return None

def get_active_interface():
    """Auto-detect an active network interface."""
    interfaces = psutil.net_if_addrs()
    for iface in interfaces:
        if iface != "lo":  # Ignore loopback interface
            logging.info(f"Using detected network interface: {iface}")
            return iface
    return "eth0"  # Fallback to eth0

def is_host_reachable(target_ip):
    """Check if the target PC is reachable at startup."""
    if not shutil.which("ping"):
        logging.error("Ping command not found in the container. Make sure 'iputils-ping' is installed.")
        return False

    try:
        result = subprocess.run(
            ["ping", "-c", "2", target_ip],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if result.returncode == 0:
            logging.info(f"PC {target_ip} is already online at startup.")
            return True
        else:
            logging.info(f"PC {target_ip} is not reachable at startup.")
            return False
    except Exception as e:
        logging.error(f"Ping error: {e}")
        return False

def is_host_awake(target_ip):
    """Check if the target PC is awake using ping."""
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
        logging.info("Skipping WoL: Target PC is already online.")
        return

    logging.info(f"Sending WoL packet to {mac_address}")
    wakeonlan.send_magic_packet(mac_address)
    last_wake_time = current_time

def build_sniff_filter(target_ip, ports):
    """Builds a Scapy filter string for multiple ports."""
    if not ports or not isinstance(ports, list) or len(ports) == 0:
        return f"dst host {target_ip}"  # If no ports are specified, sniff all traffic

    port_filter = " or ".join([f"port {p}" for p in ports if isinstance(p, int)])
    return f"dst host {target_ip} and ({port_filter})"

def packet_callback(packet):
    """Handle detected network packets."""
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

    target_ip = config["target_ip"]
    mac_address = config["mac_address"]
    cooldown_seconds = config.get("cooldown_seconds", 300)

    # Check if the PC is reachable at startup
    if is_host_reachable(target_ip):
        logging.info(f"Skipping WoL at startup: PC {target_ip} is online.")
    else:
        logging.info(f"PC {target_ip} is offline at startup. Waiting for traffic to trigger WoL.")

    network_interface = get_active_interface()
    ports = config.get("ports", [])  # Get ports from config, default to empty (all traffic)
    sniff_filter = build_sniff_filter(target_ip, ports)

    logging.info(f"Listening on {network_interface} with filter: {sniff_filter}")

    sniff(iface=network_interface, filter=sniff_filter, prn=packet_callback, store=0)

if __name__ == "__main__":
    main()
