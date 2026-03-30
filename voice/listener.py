import speech_recognition as sr

recognizer = sr.Recognizer()
recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 1.2

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.3)
        try:
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            print("Timeout - no speech detected")
            return None

    try:
        text = recognizer.recognize_google(audio, language="en-IN")
        print(f"You: {text}")
        return text
    except sr.UnknownValueError:
        print(" Could not understand")
        return None
    except sr.RequestError:
        print(" Network error")
        return None