from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from sqlite_db import sql_db
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain import hub
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from langchain.agents import AgentExecutor

llm = ChatOllama(
    model="llama3.2",
    function_call="auto"
)

sql_toolkit = SQLDatabaseToolkit(db=sql_db, llm=llm)

prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")
system_message = prompt_template.format(dialect="SQLite", top_k=5)

sql_agent = create_react_agent(llm, tools=sql_toolkit.get_tools(), prompt=system_message)

example_query = "Who are the top 3 best selling artists?"

query = "Which country's customers spent the most?"

messages = sql_agent.invoke({"messages": [("human", query)]})

print(messages["messages"][-1].content)

# events = react_agent.stream(
#     {"messages": [("user", query)]},
#     stream_mode="values",
# )
# for event in events:
#     event["messages"][-1].pretty_print()