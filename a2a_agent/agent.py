# a2a_agent/agent.py
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents.remote_a2a_agent import (
    AGENT_CARD_WELL_KNOWN_PATH,
    RemoteA2aAgent,
)
from google.adk.tools.agent_tool import AgentTool


lina_agent = RemoteA2aAgent(
    name="LinaAgent",
    description="공감과 위로를 중심으로 답하는 Lina입니다.",
    agent_card=f"http://localhost:8001{AGENT_CARD_WELL_KNOWN_PATH}",
)

hwana_agent = RemoteA2aAgent(
    name="HwanaAgent",
    description="팩트 기반으로 직설적인 반론과 점검을 제공하는 Hwana입니다.",
    agent_card=f"http://localhost:8002{AGENT_CARD_WELL_KNOWN_PATH}",
)

root_agent = Agent(
    name="A2ADiscussionAgent",
    description="Lina와 Hwana 원격 A2A 에이전트가 서로 의견을 주고받게 조율하는 진행자 에이전트입니다.",
    model=LiteLlm("openai/gpt-4o"),
    instruction="""
당신은 두 원격 A2A 에이전트의 토론을 진행하는 moderator입니다.

사용자 요청을 받으면 반드시 아래 순서로 진행합니다.
1. `LinaAgent`를 호출해서 공감적이고 사용자 친화적인 1차 의견을 받습니다.
2. `HwanaAgent`를 호출하면서 사용자의 원래 요청과 LinaAgent의 1차 의견을 함께 전달합니다. HwanaAgent에는 빠진 사실, 약한 논리, 현실적인 반론을 점검하라고 요청합니다.
3. 다시 `LinaAgent`를 호출하면서 HwanaAgent의 반론을 전달하고, 공감은 유지하되 반론을 반영한 수정 의견을 요청합니다.
4. 마지막으로 moderator인 당신이 세 응답을 종합해서 최종 답변을 작성합니다.

규칙:
- LinaAgent와 HwanaAgent를 모두 최소 1회 이상 호출하기 전에는 최종 답변하지 않습니다.
- 두 에이전트의 응답을 그대로 길게 붙여넣지 말고, 핵심 차이와 합의점을 요약합니다.
- 최종 답변에는 `Lina 관점`, `Hwana 관점`, `종합 결론`을 짧게 구분합니다.
- 원격 A2A 서버가 연결되지 않으면 어떤 agent card URL에 연결 실패했는지 명확히 말하고, 사용자가 띄워야 할 서버 명령을 알려줍니다.
""",
    tools=[
        AgentTool(agent=lina_agent),
        AgentTool(agent=hwana_agent),
    ],
)
