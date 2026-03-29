import os

def speak(text):
    print(f"🤖 VANTAGE: {text}")
    # Uses Mac's built-in ultra fast TTS - no lag!
    os.system(f'say "{text}"')