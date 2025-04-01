import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
import speech_recognition as sr
import pyttsx3

# Initialize the LLM
llm = ChatOllama(model="llama3.2")

# Define the prompt
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Your name is Prushka. You are a helpful assistant."),
        ("human", "{input}"),
    ]
)

# Define the output parser
output_parser = StrOutputParser()

# Initialize text-to-speech engine
# brew install portaudio python-pyaudio

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
    
def speak_text(text):
    engine = pyttsx3.init()  # Initialize locally to avoid threading issues
    engine.say(text)
    engine.runAndWait()

# Streamlit UI
st.set_page_config(page_title="LLM Chatbot", layout="wide")

st.sidebar.title("Settings")
st.sidebar.write("This chatbot is powered by Llama3.2 using LangChain.")

st.title("🤖 Prushka: Multi-agent Personal Chatbot - Powered by LLMs")
user_input = st.text_area("Enter your message:", "", height=100)

if st.button("🎤 Speak Question"):
    user_input = recognize_speech()
    st.text_area("Recognized Speech:", user_input, height=100)
    if user_input.strip():
        chain = prompt | llm | output_parser
        result = chain.invoke({"input": user_input})
        st.subheader("Response:")
        st.write(result)
        speak_text(result)
    else:
        st.warning("Please speak your question.")

if st.button("Generate Response"):
    if user_input.strip():
        chain = prompt | llm | output_parser
        result = chain.invoke({"input": user_input})
        st.subheader("Response:")
        st.write(result)
        speak_text(result)
    else:
        st.warning("Please enter a message before generating a response.")

# Streamlit UI
# st.set_page_config(page_title="LLM Chatbot", layout="wide")

# st.sidebar.title("Settings")
# st.sidebar.write("This chatbot is powered by Llama3.2 using LangChain.")

# st.title("🤖 Prushka: Multi-agent Personal Chatbot - Powered by LLMs")
# user_input = st.chat_input("Ask Anything")

# if user_input:
#     with st.chat_message("user"):
#         st.write(user_input)

#     with st.spinner("Generating response..."):
#         chain = prompt | llm | output_parser
#         result = chain.invoke({"input": user_input})
#         st.subheader("Response:")
#         st.write(result)
# else:
#     st.warning("Please enter a message before generating a response.")