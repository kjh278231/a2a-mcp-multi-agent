# lina/agent.py
import os
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from .prompt import INSTRUCTION
from env import OPENAI_API_KEY

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

username = "수강생"
formatted_instruction = INSTRUCTION.format(username=username)

root_agent = Agent(
    name="lina",
    instruction=formatted_instruction,
    model=LiteLlm("openai/gpt-4o"),
)

### A2A — 핵심 2줄! ###
from google.adk.a2a.utils.agent_to_a2a import to_a2a

app = to_a2a(root_agent, port=8001)
# 에이전트를 HTTP 서버로 감싸서 A2A 서버로 만듦
# Agent Card(/.well-known/agent.json)도 자동 생성
