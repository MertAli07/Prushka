import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

# Initialize the LLM
llm = ChatOllama(model="llama3.2")

# Define the prompt
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        ("human", "{input}"),
    ]
)

# Streamlit UI
st.set_page_config(page_title="LLM Chatbot", layout="wide")

st.sidebar.title("Settings")
st.sidebar.write("This chatbot is powered by Llama3.2 using LangChain.")

st.title("🤖 Prushka: Multi-agent Personal Chatbot - Powered by LLMs")
user_input = st.text_area("Enter your message:", "", height=100)

if st.button("Generate Response"):
    if user_input.strip():
        chain = prompt | llm
        result = chain.invoke({"input": user_input})
        st.subheader("Response:")
        st.write(result)
    else:
        st.warning("Please enter a message before generating a response.")