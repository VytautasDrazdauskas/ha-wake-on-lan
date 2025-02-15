# Wake-on-LAN Listener for Home Assistant

This Home Assistant add-on listens for network activity towards a specific PC and sends a Wake-on-LAN (WoL) magic packet if the PC is offline. This helps automatically wake up your PC when needed without keeping it on all the time.

## Features
- Listens for network packets sent to the PC's IP address.
- Wakes the PC only when it is offline.
- Implements a cooldown to prevent excessive wake-up attempts.
- Fully configurable via the Home Assistant UI.

## Installation

1. **Add Repository to Home Assistant:**
   - Navigate to **Settings > Add-ons > Add-on Store**.
   - Click the **three dots (⋮) > Repositories**.
   - Enter your repository URL:
     ```
     https://github.com/VytautasDrazdauskas/ha-wake-on-lan 
     ```
   - Click **Add** and refresh the page.

2. **Install the Add-on:**
   - Find **Wake-on-LAN Listener** in the Add-on Store.
   - Click **Install**.
   - Open the add-on, configure settings, and start it.

## Configuration

Configure the add-on from the **Home Assistant UI** under **Settings > Add-ons > Wake-on-LAN Listener > Configuration**.

| Option | Description |
|--------|-------------|
| `target_ip` | The PC's static IP address. |
| `mac_address` | The PC's MAC address for Wake-on-LAN. |
| `network_interface` | The network interface to monitor (e.g., `eth0`). |
| `cooldown_seconds` | The minimum time between wake-up attempts (default: 300 seconds). |

## How It Works
1. The add-on listens for network traffic directed at the PC.
2. If traffic is detected but the PC is offline, a WoL packet is sent.
3. A cooldown prevents repeated wake-up attempts.

## Logs & Debugging
Check logs in **Home Assistant > Settings > Add-ons > Wake-on-LAN Listener > Logs** to verify activity.

## License
This project is open-source and available under the MIT License.
