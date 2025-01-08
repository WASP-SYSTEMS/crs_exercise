from pathlib import Path
from langchain_openai import ChatOpenAI
from project.project import AixccProject

# NOTE: The following project defintion makes the interaction with the challenge
#       project you are supposed to patch much, much easier. You ONLY need to use
#       the public methods.

project = AixccProject(
    project_path=Path("mock-cp"),
    src_path_rel=Path("src/samples")
)

# NOTE: To better understand what is happening here, please read
#       https://github.com/langchain-ai/langgraph/blob/main/docs/docs/how-tos/tool-calling.ipynb

# Here you can define your tools
tools = []

# We use an openai model
model_with_tools = ChatOpenAI(
    model="gpt-4o-2024-11-20", temperature=0
).bind_tools(tools)

# You can implement your agent here