"""
ARNIDS - AI Powered Adversarial Robust Network Intrusion Detection System

Developed by: Chaitanya Jain
GitHub: https://github.com/chaitanyajain26

Copyright (c) 2026 Chaitanya Jain

Licensed under the MIT License.
"""


import subprocess

def start_live_capture(interface="Wi-Fi", packet_count=10):

    print("\n[INFO] Starting Live Packet Capture...")

    command = [
        "tshark",
        "-i", interface,
        "-c", str(packet_count),
        "-T", "fields",
        "-e", "frame.len",
        "-e", "_ws.col.Protocol"
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        packets = result.stdout.splitlines()

        print("\n[LIVE TRAFFIC]\n")

        total_packets = 0
        total_size = 0

        for i, packet in enumerate(packets):

            parts = packet.split("\t")

            if len(parts) >= 2:

                size = float(parts[0])
                protocol = parts[1]

                print(f"Packet {i+1}: Size={size}, Protocol={protocol}")

                total_packets += 1
                total_size += size

        avg_size = total_size / total_packets if total_packets > 0 else 0

        features = [[
            total_packets,
            avg_size,
            1518.0,
            total_size
        ]]

        print("\n[INFO] Live Features:", features)

        return features

    except Exception as e:
        print("[ERROR]", e)

        return [[0,0,0,0]]


# =========================
# TEST
# =========================
if __name__ == "__main__":

    start_live_capture()