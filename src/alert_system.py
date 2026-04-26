from voice_module import speak

def trigger_alert(risk, attack):

    print("\n[ALERT SYSTEM]\n")

    if risk >= 80:

        print(" HIGH RISK ATTACK DETECTED ")

        speak("Warning. High risk cyber attack detected")

    elif risk >= 50:

        print(" Medium Risk Detected")

        speak("Medium risk activity detected")

    else:

        print(" System Stable")

        speak("System is stable")