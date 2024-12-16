from pathlib import Path
from langchain_openai import ChatOpenAI
from project.project import AixccProject

OPENAI_API_BASE = ""
OPENAI_API_KEY = ""

# NOTE: The follwing project defintion makes the interaction with the challenge
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

# set up model to work with our server
model = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    openai_api_base=OPENAI_API_BASE,
    api_key=OPENAI_API_KEY,
    model_kwargs={
        "extra_body": {
            "metadata": {
                "generation_name": "ishaan-generation-langchain-client",
                "generation_id": "langchain-client-gen-id22",
                "trace_id": "langchain-client-trace-id22",
                "trace_user_id": "langchain-client-user-id2",
            }
        },
    },
).bind_tools(tools)

# You can implement your agent here