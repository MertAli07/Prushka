# brew install portaudio python-pyaudio
import streamlit as st
import speech_recognition as sr

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        with st.spinner("Listening... Please speak now."):
            recognizer.adjust_for_ambient_noise(source, duration=2)  # Adjust longer
            try:
                audio = recognizer.listen(source, phrase_time_limit=10)  # Remove timeout
                
                # Save audio to check if it's being captured correctly
                with open("test_audio.wav", "wb") as f:
                    f.write(audio.get_wav_data())

                # Try recognition with debug mode
                result = recognizer.recognize_google(audio, show_all=True)
                
                if not result:
                    return "No speech recognized. Try speaking louder or closer."
                
                return result["alternative"][0]["transcript"] if "alternative" in result else "Speech not clear."

            except sr.UnknownValueError:
                return "Could not understand the audio."
            except sr.RequestError:
                return "Speech recognition service is unavailable."
            except Exception as e:
                return f"Error: {str(e)}"