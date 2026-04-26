import speech_recognition as sr
import pyttsx3
from llama_chat import ask_llama


# TEXT TO SPEECH 

def speak(text):
    try:
        engine = pyttsx3.init()   #  new engine every time (fixes freeze)

        engine.setProperty('rate', 170)
        engine.setProperty('volume', 1.0)

        print("\nAI:", text)

        engine.say(text)
        engine.runAndWait()

    except Exception as e:
        print("Speech Error:", e)



# LIST MICROPHONES

def list_mics():
    print("\nAvailable Microphones:")
    for i, mic in enumerate(sr.Microphone.list_microphone_names()):
        print(i, mic)


# SPEECH TO TEXT 

def listen(device_index=None):
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone(device_index=device_index) as source:
            print("\nListening... Speak now")

            #  noise handling
            recognizer.energy_threshold = 300
            recognizer.dynamic_energy_threshold = True

            recognizer.adjust_for_ambient_noise(source, duration=1)

            audio = recognizer.listen(
                source,
                timeout=10,
                phrase_time_limit=8
            )

            print("Processing...")

            text = recognizer.recognize_google(audio)
            print("You:", text)

            return text

    except sr.WaitTimeoutError:
        print("Timeout: No speech detected")
        return None

    except sr.UnknownValueError:
        print("Could not understand audio")
        return None

    except Exception as e:
        print("Mic Error:", e)
        return None



# MAIN VOICE SYSTEM 

def start_voice_chat():

    print("VOICE AI SYSTEM STARTED")
    print("Say 'exit' to stop\n")

    # Show mic list
    list_mics()

    #  CHANGE THIS AFTER CHECKING LIST
    mic_index = 0   #  try 0 / 1 / 2

    context = """
Attack: Potential Risk
Ports: 445, 135 open
"""

    while True:
        user_input = listen(device_index=mic_index)

        if user_input is None:
            continue

        if "exit" in user_input.lower():
            speak("Goodbye!")
            break

        #  AI response
        response = ask_llama(user_input, context)

        speak(response)



# RUN

if __name__ == "__main__":
    start_voice_chat()
