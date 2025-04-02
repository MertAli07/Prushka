import pyttsx3

def speak_text(text):
    engine = pyttsx3.init()  # Initialize locally to avoid threading issues
    engine.say(text)
    engine.runAndWait()