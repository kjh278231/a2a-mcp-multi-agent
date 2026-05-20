import os
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from .prompt import INSTRUCTION
from .tools import search_recipe
from env import OPENAI_API_KEY

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# MODEL = LiteLlm("ollama_chat/gemma4:e4b") --> Tool Calling 지원 X

MODEL = LiteLlm("openai/gpt-4o")

root_agent = Agent(
    name="recipe_agent",
    instruction=INSTRUCTION,
    model=MODEL,
    tools=[search_recipe],  # RAG 검색 함수를 도구로 등록
)
