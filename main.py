from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from sqlite_db import sql_db
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain import hub
from langgraph.prebuilt import create_react_agent

llm = ChatOllama(
    model="llama3.2"
)

sql_toolkit = SQLDatabaseToolkit(db=sql_db, llm=llm)

prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")
system_message = prompt_template.format(dialect="SQLite", top_k=5)

agent_executor = create_react_agent(llm, sql_toolkit.get_tools(), prompt=system_message)

example_query = "Who are the top 3 best selling artists?"

query = "Which country's customers spent the most?"

events = agent_executor.stream(
    {"messages": [("user", query)]},
    stream_mode="values",
)
for event in events:
    event["messages"][-1].pretty_print()

