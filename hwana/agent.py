# hwana/agent.py
import os
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from .prompt import INSTRUCTION
from env import OPENAI_API_KEY

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

username = "수강생"
formatted_instruction = INSTRUCTION.format(username=username)

root_agent = Agent(
    name="hwana",
    instruction=formatted_instruction,
    model=LiteLlm("openai/gpt-4o"),
)

### A2A — 똑같이 2줄! ###
from google.adk.a2a.utils.agent_to_a2a import to_a2a

app = to_a2a(root_agent, port=8002)
