import subprocess
import time
import os
from datetime import datetime
import re

last_strengths = {}
log_dir = "wifi_logs"
os.makedirs(log_dir, exist_ok=True)

def sanitize_mac(mac):
    return mac.replace(":", "_").replace("-", "_")

def parse_windows_wifi():
    result = subprocess.run(["netsh", "wlan", "show", "networks", "mode=bssid"],
                            capture_output=True, text=True)
    lines = result.stdout.splitlines()
    wifi_data = []

    mac = None

    for line in lines:
        line = line.strip()
        if "BSSID" in line:
            mac_match = re.search(r"BSSID \d+\s*:\s*([\w:-]+)", line)
            if mac_match:
                mac = mac_match.group(1)
        elif "Signal" in line:
            signal_match = re.search(r"Signal\s*:\s*(\d+)%", line)
            if signal_match and mac:
                signal_percent = int(signal_match.group(1))
                signal_dbm = int((signal_percent / 2) - 100)
                wifi_data.append((mac, signal_dbm))
                mac = None

    if not wifi_data:
        print("DEBUG: No Wi-Fi data parsed.")
        print(result.stdout)

    return wifi_data


def log_change(mac, signal):
    filename = sanitize_mac(mac) + ".txt"
    path = os.path.join(log_dir, filename)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] Signal strength: {signal} dBm\n"
    with open(path, "a") as f:
        f.write(log_line)
    print(f"Logged for {mac}: {signal} dBm")

def log_changes(new_data, filter_mac=None):
    global last_strengths
    for mac, signal in new_data:

        mac_norm = mac.lower()
        if filter_mac and mac_norm != filter_mac.lower():
            continue
        
        log_change(mac, signal)
        last_strengths[mac_norm] = signal

if __name__ == "__main__":
    scan_interval = input("Enter scan interval in seconds (default 2): ").strip()
    try:
        scan_interval = float(scan_interval)
    except ValueError:
        scan_interval = 2

    filter_mac = input("Enter MAC address to filter (leave empty to scan all): ").strip()
    if filter_mac == "":
        filter_mac = None

    try:
        while True:
            scan_results = parse_windows_wifi()
            if not scan_results:
                print("No Wi-Fi networks found. Make sure Wi-Fi is enabled.")
            else:
                if filter_mac:
                    print(f"Filtering for MAC: {filter_mac}")
                log_changes(scan_results, filter_mac=filter_mac)
            time.sleep(scan_interval)

    except KeyboardInterrupt:
        print("\nScan stopped by user.")
