
## Task

Your task is to implement a simple CRS consisting of one LLM tool-calling agent. This agent 
should be able to fix the vulnerability in the given challenge project.

## Requirements

- docker >= 24.0.5
- python >= 3.10
- GNU make >= 4.3
- yq >= 4 (https://github.com/mikefarah/yq/)

Me, when I have to build `yq` from source: (ノ ゜Д゜)ノ ︵ ┻━┻

Maybe you can find the right pre build binaries at the release page.

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

Now you are ready implement your agent in `minimal_crs.py`.

**NOTE**: Execute your the CRS by running `python3 minimal_crs.py` in the root directory of this project to prevent import errors.

## Helpful links

- https://github.com/langchain-ai/langgraph/blob/main/docs/docs/how-tos/tool-calling.ipynb