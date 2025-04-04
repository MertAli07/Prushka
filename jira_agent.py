import os
from dotenv import load_dotenv

from langchain.agents import AgentType, initialize_agent
from langchain_community.agent_toolkits.jira.toolkit import JiraToolkit
from langchain_community.utilities.jira import JiraAPIWrapper
from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq


load_dotenv()

# llm = ChatOllama(
#     model="llama3.2",
#     function_call="auto"
# )

llm = ChatGroq(
    model="llama-3.3-70b-versatile"
)

jira = JiraAPIWrapper(
    jira=os.getenv("JIRA_URL"),
    jira_username=os.getenv("JIRA_USERNAME"),
    jira_api_token=os.getenv("JIRA_API_TOKEN"),
    jira_cloud=os.getenv("JIRA_CLOUD")
)

jira_toolkit = JiraToolkit.from_jira_api_wrapper(jira)

jira_agent = initialize_agent(
    jira_toolkit.get_tools(), 
    llm, 
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
    verbose=True,
    handle_parsing_errors=True
    # max_iterations=5
)

res = jira_agent.run("create a task with title 'test123' and description 'test description' on project SCRUM")

print(res)