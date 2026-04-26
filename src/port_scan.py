import subprocess

def scan_ports():
    print("\n[INFO] Scanning ports...")

    try:
        result = subprocess.run(
            ["nmap", "-p", "1-1000", "127.0.0.1"],
            capture_output=True,
            text=True
        )

        output = result.stdout

        open_ports = []

        for line in output.split("\n"):
            if "/tcp" in line and "open" in line:
                parts = line.split()
                port = parts[0]
                service = parts[2] if len(parts) > 2 else "unknown"

                open_ports.append(f"{port} ({service})")

        print("\n[INFO] Open Ports Detected:")
        for p in open_ports:
            print(" -", p)

        return open_ports

    except Exception as e:
        print("[ERROR] Nmap error:", e)
        return []



# TEST RUN 

if __name__ == "__main__":
    print("TESTING PORT SCANNER")

    ports = scan_ports()

    print("\nFINAL OUTPUT:", ports)