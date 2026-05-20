# hwana/agent.py
import os

from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from env import OPENAI_API_KEY
from .prompt import INSTRUCTION


os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

username = "사용자"
formatted_instruction = INSTRUCTION.format(username=username)

root_agent = Agent(
    name="hwana",
    instruction=formatted_instruction,
    model=LiteLlm("openai/gpt-4o"),
)

app = to_a2a(root_agent, port=8002)
