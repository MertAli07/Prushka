import os
from dotenv import load_dotenv

from typing import Annotated
from typing_extensions import TypedDict
from PIL import Image

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import MemorySaver


load_dotenv()

class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]

def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

def print_graph(graph):
    try:
        graph_png = graph.get_graph().draw_mermaid_png()
        with open("/tmp/graph.png", "wb") as f:
            f.write(graph_png)
        img = Image.open("/tmp/graph.png")
        img.show()
    except Exception as e:
        print(e)
        pass

def stream_graph_updates(user_input: str, thread_id: str = "1"):
    config = {"configurable": {"thread_id": thread_id}}
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}, config=config):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)

llm = ChatOllama(
    model="llama3.2"
)

checkpointer = MemorySaver()

graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile(checkpointer=checkpointer)

while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        stream_graph_updates(user_input, "1")
    except:
        # fallback if input() is not available
        user_input = "What do you know about LangGraph?"
        print("User: " + user_input)
        stream_graph_updates(user_input)
        break
