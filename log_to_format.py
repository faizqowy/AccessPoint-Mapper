import argparse
import os
import csv
from collections import defaultdict

log_dir = "wifi_logs"

def read_logs():
    timestamps = defaultdict(dict)
    mac_addresses = set()

    for filename in os.listdir(log_dir):
        if filename.endswith(".txt"):
            mac = filename.replace("_", ":").replace(".txt", "")
            mac_addresses.add(mac)
            with open(os.path.join(log_dir, filename), "r") as f:
                for line in f:
                    if "]" in line:
                        timestamp, signal = line.strip().split("] ")
                        timestamp = timestamp.strip("[]")
                        signal_value = signal.split(":")[-1].strip().replace(" dBm", "")
                        timestamps[timestamp][mac] = signal_value
    return timestamps, sorted(mac_addresses)

def convert_to_csv_filtered(timestamps, macs, output_path):
    if not os.path.exists('results/'):
        os.makedirs('results/')
    output_path = os.path.join('results/', output_path)
    with open(output_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        header = ["Timestamp"] + macs
        writer.writerow(header)

        for timestamp in sorted(timestamps.keys()):
            row = [timestamp]
            valid = True
            for mac in macs:
                value = timestamps[timestamp].get(mac)
                if value is None:
                    valid = False
                    break
                row.append(value)
            if valid:
                writer.writerow(row)

    print(f"Converted logs saved to CSV (complete rows only): {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Wi-Fi log files to filtered CSV.")
    parser.add_argument("format", choices=["csv"], help="Output format: only 'csv' is supported in this layout.")
    parser.add_argument("-o", "--output", help="Output file name (default: filtered_output.csv)", default="filtered_output.csv")

    args = parser.parse_args()

    timestamps, macs = read_logs()

    if not timestamps:
        print("No logs found in wifi_logs/")
        exit()

    convert_to_csv_filtered(timestamps, macs, args.output)
