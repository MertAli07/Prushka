import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
    print(voice.id)
    engine.setProperty('voice', voices[0].id)
