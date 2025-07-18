import os
from dotenv import load_dotenv

from typing import Annotated
from typing_extensions import TypedDict
from PIL import Image

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import MemorySaver
from langchain.tools.retriever import create_retriever_tool
from langchain_mongodb.vectorstores import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings
from langgraph.prebuilt import ToolNode


load_dotenv()

class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]

# def chatbot(state: State):
#     return {"messages": [llm.invoke(state["messages"])]}

from langchain_core.messages import AIMessage, HumanMessage

def chatbot(state: State):
    response = llm.invoke(state["messages"])
    
    print("⛏️ LLM returned:", response)
    print("📦 Type of LLM response:", type(response))

    # Wrap if needed
    if not isinstance(response, AIMessage):
        response = AIMessage(content=str(response))

    return {"messages": state["messages"] + [response]}


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

    initial_state = {
        "messages": [HumanMessage(content=user_input)]
    }

    for event in graph.stream(initial_state, config=config):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)

llm = ChatOllama(
    model="llama3.2"
)

# Instantiate the vector store
vector_store = MongoDBAtlasVectorSearch.from_connection_string(
  connection_string = os.getenv("MONGODB_ATLAS_URI"), # Atlas cluster or local deployment URI
  namespace = "sample_mflix.embedded_movies",  # Database and collection name
  embedding = OpenAIEmbeddings(model="text-embedding-ada-002"), # Embedding model to use
  index_name = "vector_index",                      # Name of the vector search index
)

# vector_store.create_vector_search_index(dimensions=1536)

retriever = vector_store.as_retriever()
retriever_tool = create_retriever_tool(
    retriever,
    "vector_search_retriever", # Tool name
    "Retrieve relevant documents from the collection" # Tool description
)

retriever_node = ToolNode([retriever_tool])

graph_builder = StateGraph(State)
# graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("vector_search_retriever", retriever_node)

# graph_builder.add_edge(START, "chatbot")
# graph_builder.add_edge("chatbot", END)

graph_builder.add_edge(START, "vector_search_retriever")
# graph_builder.add_edge("vector_search_retriever", "chatbot")
graph_builder.add_edge("vector_search_retriever", END)

graph = graph_builder.compile()

# res = retriever_tool.run("What is the name of the movie?")

results = vector_store.similarity_search(
    "what is a movie about Young Pauline", k=2
)

for res in results:
    print(f"* {res.page_content} [{res.metadata}]")

# while True:
#     try:
#         user_input = input("User: ")
#         if user_input.lower() in ["quit", "exit", "q"]:
#             print("Goodbye!")
#             break
#         stream_graph_updates(user_input, "1")
#     except Exception as e:
#         # fallback if input() is not available
#         print(e)
#         break
