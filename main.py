from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3.2"
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant.",
        ),
        ("human", "{input}"),
    ]
)

chain = prompt | llm
result = chain.invoke(
    {
        "input": "I love programming.",
    }
)

print(result)