import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
from env import OPENAI_API_KEY, GOOGLE_API_KEY

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY


class AgentState(TypedDict):
    """
    에이전트 상태 정의
    - messages: 대화 메시지 리스트
    - user_query: 사용자의 원본 질문
    """

    messages: list
    user_query: str


# LangGraph 워크플로우 구성 함수
def create_langgraph_workflow():
    """
    LangGraph 워크플로우 생성
    START → analyze_query → generate_response → END
    """
    # 1. llm 인스턴스 생성
    model = ChatOpenAI(model="gpt-4o-mini")

    # 2 노드 정의
    ## 1. 질문분석 노드 : 시스템 메시지, 사용자 질문 준비
    def analyze_query_node(state: AgentState) -> AgentState:
        user_query = state["user_query"]

        return {
            "messages": [
                SystemMessage(
                    content="당신은 전문 AI 어시스턴트입니다. 사용자의 질문에 친절한 한국어 답변을 제공하세요."
                ),
                HumanMessage(content=user_query),
            ],
            "user_query": user_query,
        }

    ## 2. 응답생성 노드 : LLM에 메시지 전달 → 응답 생성
    def generate_response_node(state: AgentState) -> AgentState:
        messages = state["messages"]
        response = model.invoke(messages)
        return {
            "messages": [response],
            "user_query": state["user_query"],
        }

    workflow = StateGraph(AgentState)
    workflow.add_node("analyze_query", analyze_query_node)
    workflow.add_node("generate_response", generate_response_node)
    workflow.add_edge(START, "analyze_query")
    workflow.add_edge("analyze_query", "generate_response")
    workflow.add_edge("generate_response", END)
    return workflow.compile()


class LangGraphChatBot:
    def __init__(self):
        self.workflow = create_langgraph_workflow()

    def process_message(self, user_query: str) -> str:
        init_stage: AgentState = {
            "messages": [],
            "user_query": user_query,
        }
        try:
            result = self.workflow.invoke(init_stage)
            return str(result["messages"][0].content)  # 마지막 메시지(LLM 응답) 반환
        except Exception as e:
            print(f"Error occurred: {e}")
            return "에이전트 응답"


def main():
    """터미널 무한 루프 챗봇"""
    print("=" * 60)
    print("LangGraph 챗봇이 시작됐습니다.")
    print("종료하려면 'exit', 'quit', '종료' 중 하나를 입력하세요.")
    print("(또는 Ctrl+C / Ctrl+D 로 즉시 종료 가능)")
    print("=" * 60)

    # 챗봇 인스턴스 한 번만 생성 (workflow 컴파일도 한 번만 일어남)
    chatbot = LangGraphChatBot()

    while True:
        try:
            user_input = input("\n나: ").strip()
        except (EOFError, KeyboardInterrupt):
            # Ctrl+D 또는 Ctrl+C 로 종료
            print("\n\n챗봇을 종료합니다. 안녕히 가세요.")
            break

        # 빈 입력은 건너뛰기
        if not user_input:
            continue

        # 종료 명령
        if user_input.lower() in ("exit", "quit", "종료"):
            print("챗봇을 종료합니다. 안녕히 가세요.")
            break

        # LangGraph 워크플로우 통과 → 응답 출력
        response = chatbot.process_message(user_input)
        print(f"\n에이전트: {response}")


if __name__ == "__main__":
    main()
