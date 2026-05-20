# a2a_agent/agent.py
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents.remote_a2a_agent import (
    RemoteA2aAgent,
    AGENT_CARD_WELL_KNOWN_PATH,
)

lina_agent = RemoteA2aAgent(
    name="LinaAgent",
    description="공감과 위로 중심의 따뜻한 Lina입니다.",
    agent_card=f"http://localhost:8001{AGENT_CARD_WELL_KNOWN_PATH}",
)

hwana_agent = RemoteA2aAgent(
    name="HwanaAgent",
    description="팩트 기반으로 따끔하게 혼내주는 Hwana입니다.",
    agent_card=f"http://localhost:8002{AGENT_CARD_WELL_KNOWN_PATH}",
)

root_agent = Agent(
    name="HelperAgent",
    description="친구들이 함께 이야기하는 롤플레잉 에이전트입니다.",
    model=LiteLlm("openai/gpt-4o"),
    sub_agents=[lina_agent, hwana_agent],
)
