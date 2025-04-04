from atlassian import Jira
import os

# Initialize the Jira connection
jira = Jira(
    url=os.getenv("JIRA_INSTANCE_URL"),
    username="mertaliyalcin07@gmail.com",
    password=os.getenv("JIRA_API_TOKEN"),
    cloud=True if os.getenv("JIRA_CLOUD", "false").lower() == "true" else False
)

def test_jira_connection():
    try:
        # Try to fetch all visible projects
        projects = jira.get_all_projects(included_archived=None, expand=False)
        test = jira.get_all_sprint(board_id=1)
        print(projects)
    except Exception as e:
        print("❌ Failed to connect to Jira:")
        print(e)

def test_get_specific_project(project_key="SCRUM"):
    try:
        project = jira.get_project(project_key)
        if project:
            print(f"✅ Successfully fetched project '{project_key}': {project['name']}")
        else:
            print(f"⚠️ Could not find project with key: {project_key}")
    except Exception as e:
        print("❌ Failed to fetch project:")
        print(e)

# test_jira_connection()
test_jira_connection()