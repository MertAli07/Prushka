import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from speech_to_text import recognize_speech
from text_to_speech import speak_text
from general_utils import choose_llm

# Initialize the LLM
llm = choose_llm("ollama", "gemma3_1b")

# Define the prompt
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Your name is Prushka. You are a helpful assistant."),
        ("human", "{input}"),
    ]
)

# Define the output parser
output_parser = StrOutputParser()

# Streamlit UI
st.set_page_config(page_title="Prushka", layout="wide")

with st.sidebar:
    st.sidebar.title("Settings")
    st.sidebar.write("This chatbot is powered by Llama3.2 using LangChain.")
    chat_mode = st.sidebar.selectbox("Chat Mode", ["Text", "Voice"])
    respond_with_voice = st.sidebar.checkbox("Respond with Voice")
    

st.title("🤖 Prushka: Multi-agent Personal Chatbot - Powered by LLMs")

user_input = ""

if chat_mode == "Text":
    user_input = st.chat_input("Ask Anything")
elif chat_mode == "Voice":
    if st.button("🎤 Speak Question"):
        user_input = recognize_speech()

if user_input:
    with st.chat_message("user"):
        st.write(user_input)

    with st.spinner("Generating response..."):
        chain = prompt | llm | output_parser
        result = chain.invoke({"input": user_input})
        with st.chat_message("assistant"):
            st.write(result)
        if respond_with_voice:
            speak_text(result)
else:
    with st.chat_message("assistant"):
        st.write("How are you?")