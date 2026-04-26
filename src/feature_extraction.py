"""
ARNIDS - AI Powered Adversarial Robust Network Intrusion Detection System

Developed by: Chaitanya Jain
GitHub: https://github.com/chaitanyajain26

Copyright (c) 2026 Chaitanya Jain

Licensed under the MIT License.
"""

import os
import numpy as np



import subprocess
import numpy as np
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
def extract_features(pcap_file):
    print("\n[INFO] Starting Feature Extraction...")
    print("[INFO] File:", pcap_file)

    if not os.path.exists(pcap_file):
        print("[ERROR] File not found!")
        return [[0, 0, 0, 0]]

    try:
        command = [
            "tshark",
            "-r", pcap_file,
            "-T", "fields",
            "-e", "frame.len",
            "-e", "_ws.col.Protocol"
        ]

        print("[INFO] Running tshark...")

        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        if result.stderr:
            print("[TSHARK ERROR]:", result.stderr)

        output = result.stdout.strip().split("\n")

        packet_lengths = []
        protocols = []

        print("[INFO] Processing packets...")

        for i, line in enumerate(output):
            if not line:
                continue

            parts = line.split("\t")

            try:
                length = int(parts[0])
                protocol = parts[1] if len(parts) > 1 else "UNKNOWN"

                packet_lengths.append(length)
                protocols.append(protocol)

            except:
                continue

            if i < 5:
                print(f"Packet {i+1}: Length={length}, Protocol={protocol}")

        if len(packet_lengths) == 0:
            print("[WARNING] No packets found!")
            return [[0, 0, 0, 0]]

        total_packets = len(packet_lengths)
        avg_packet_size = np.mean(packet_lengths)
        max_packet_size = np.max(packet_lengths)

        tcp_count = protocols.count("TCP")
        udp_count = protocols.count("UDP")

        features = [[
            float(total_packets),
            float(avg_packet_size),
            float(max_packet_size),
            float(tcp_count + udp_count)
        ]]

        print("\n[INFO] Total Packets:", total_packets)
        print("[INFO] Features Extracted:", features)

        return features

    except Exception as e:
        print("[ERROR]", e)
        return [[0, 0, 0, 0]]


# =========================
# FORCE TEST RUN
# =========================
print("\n TEST RUN STARTED ")

file_path = "data/raw/pcap/traffic.pcap"

features = extract_features(file_path)

print("\nFINAL OUTPUT:", features)

