"""
ARNIDS - AI Powered Adversarial Robust Network Intrusion Detection System

Developed by: Chaitanya Jain
GitHub: https://github.com/chaitanyajain26

Copyright (c) 2026 Chaitanya Jain

Licensed under the MIT License.
"""

import joblib
import pandas as pd

from feature_extraction import extract_features
from adversarial import add_noise
from port_scan import scan_ports
from llama_explain import get_explanation
from llama_chat import ask_llama

# Live capture  + Alert
from live_capture import start_live_capture
from alert_system import trigger_alert

# Voice
from voice_module import speak

print("\n[INFO] ARNIDS FULL SYSTEM STARTED...")

# LOAD MODEL

model = joblib.load("models/custom_model.pkl")
scaler = joblib.load("models/custom_scaler.pkl")


# MODE SELECTION

print("""
=========================
SELECT ANALYSIS MODE
=========================

1. Live Packet Capture
2. PCAP File Analysis

""")

mode = input("Enter choice (1 or 2): ")


# FEATURE EXTRACTION


# LIVE MODE
if mode == "1":

    print("\n[INFO] LIVE CAPTURE MODE SELECTED")

    # Change interface if needed
    features = start_live_capture(interface="Wi-Fi")

#  FILE MODE
elif mode == "2":

    print("\n[INFO] PCAP FILE MODE SELECTED")

    pcap_file = "data/raw/pcap/traffic.pcap"

    features = extract_features(pcap_file)

# INVALID OPTION
else:

    print("\n[ERROR] Invalid Choice")
    exit()

# FIX FEATURE WARNING

columns = [
    'total_packets',
    'avg_packet_size',
    'max_packet_size',
    'protocol_count'
]

features_df = pd.DataFrame(features, columns=columns)


# ADVERSARIAL TEST

print("\n[INFO] Applying adversarial noise...")

noisy_features = add_noise(features)

noisy_df = pd.DataFrame(noisy_features, columns=columns)


# SCALE FEATURES

features_scaled = scaler.transform(features_df)
noisy_scaled = scaler.transform(noisy_df)


# PREDICTION

pred_normal = model.predict(features_scaled)[0]
pred_noisy = model.predict(noisy_scaled)[0]


# PORT SCAN

ports = scan_ports()


# SMART ALERT SYSTEM 

if pred_normal != "BENIGN":

    print("\n ALERT: ATTACK DETECTED!")

elif any("445" in p or "135" in p for p in ports):

    print("\n⚠ WARNING: System exposed (risky ports open!)")

else:

    print("\n System Normal")

# =========================
# RISK SCORE
# =========================
if pred_normal == "DDoS":

    risk_score = 90

elif pred_normal == "PortScan":

    risk_score = 70

elif pred_normal == "Brute Force":

    risk_score = 60

elif any("445" in p or "135" in p for p in ports):

    risk_score = 50

else:

    risk_score = 20

print("\nRISK SCORE:", risk_score, "%")


# TRIGGER ALERT SYSTEM 
trigger_alert(risk_score, pred_normal)


# SECURITY WARNINGS

print("\n[SECURITY WARNINGS]")

for p in ports:

    if "445" in p:
        print("WARNING: SMB port (445) vulnerable to ransomware!")

    if "22" in p:
        print("WARNING: SSH port (22) brute-force risk!")

    if "80" in p:
        print("WARNING: HTTP port (80) web attack risk!")

    if "135" in p:
        print("WARNING: RPC port (135) remote exploit risk!")

    if "902" in p:
        print("WARNING: Port 902 may expose virtualization services!")

    if "912" in p:
        print("WARNING: Port 912 may expose mesh services!")


# RESULTS

print("\n[RESULT] Normal Prediction:", pred_normal)
print("[RESULT] Adversarial Prediction:", pred_noisy)


# FIX AI CONTEXT

if pred_normal == "BENIGN":

    if any("445" in p or "135" in p for p in ports):

        context_attack = "No active attack detected but system vulnerable due to risky open ports"

    else:

        context_attack = "Normal Traffic"

else:

    context_attack = pred_normal


# LLaMA EXPLANATION

print("\n[INFO] Generating AI Explanation...")

explanation = get_explanation(
    context_attack,
    features,
    ports
)


# SAVE REPORT

with open("report.txt", "w", encoding="utf-8") as f:

    f.write("=== ARNIDS REPORT ===\n\n")

    f.write(f"Mode: {mode}\n")
    f.write(f"Attack: {context_attack}\n")
    f.write(f"Risk Score: {risk_score}%\n")

    f.write("\n=== OPEN PORTS ===\n")

    for p in ports:
        f.write(f"{p}\n")

    f.write("\n=== AI ANALYSIS ===\n")
    f.write(explanation)

print("\n Report saved as report.txt")


# FINAL OUTPUT

print("\n=========================")
print("AI EXPLANATION")
print("=========================\n")

print(explanation)


#  VOICE SUMMARY

print("\n[INFO] Speaking AI Analysis...")

voice_summary = f"""
Analysis completed.

Risk score is {risk_score} percent.

Detected condition is {context_attack}.

Risky ports include 135 and 445.

Please review the detailed AI report for mitigation steps.
"""

speak(voice_summary)


# INTERACTIVE AI CHAT 

print("\n=========================")
print("AI CYBER ASSISTANT ACTIVE")
print("=========================")

print("\nAsk anything about:")
print("- open ports")
print("- security risks")
print("- attack prevention")
print("- system protection")
print("- firewall security")
print("- ransomware risks")

print("\nType 'exit' to stop.\n")

#  CONTEXT FOR AI
chat_context = f"""
Attack: {context_attack}

Risk Score: {risk_score}

Open Ports:
{ports}

AI Analysis:
{explanation}
"""

while True:

    user_query = input("\nYou: ")

    if user_query.lower() == "exit":

        print("\n[INFO] AI Assistant Closed")

        speak("Cyber assistant stopped")

        break

    
    # AI RESPONSE
 
    ai_response = ask_llama(user_query, chat_context)

    print("\nAI:\n")
    print(ai_response)

    
    # VOICE RESPONSE 
  
    short_response = ai_response[:300]

    speak(short_response)









