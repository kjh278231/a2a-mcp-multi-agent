import os
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from .prompt import INSTRUCTION
from env import OPENAI_API_KEY

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

OFFLINE = True  # True로 설정하면 로컬 모델 사용, False로 설정하면 OpenAI 모델 사용

if OFFLINE:
    MODEL = LiteLlm("ollama_chat/qwen3:8b")
else:
    MODEL = LiteLlm("openai/gpt-4o")


# 꼭 root agent 변수에 Agent 인스턴스를 담아야 함
root_agent = Agent(name="lina_agent", instruction=INSTRUCTION, model=MODEL)
