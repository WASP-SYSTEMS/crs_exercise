
## Task

Your task is to implement a simple CRS cosisting of one agent. This agent 
should be able to fix the vulnerability in the given challenge project.

## Setup

Setup python environment:
```bash
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

Setup challenge project:
```bash
git clone -b crs_exercise --single-branch https://github.com/WASP-SYSTEMS/mock-cp
cd mock-cp
make cpsrc-prepare
make docker-config-local
make docker-build
```

Now you are ready build your agent in `minimal_crs.py`.

**NOTE**: Execute your the CRS by running `python3 minimal_crs.py` in the root directory of this project to prevent import errors.

## Helpful links

- https://github.com/langchain-ai/langgraph/blob/main/docs/docs/how-tos/tool-calling.ipynb