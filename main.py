import os
from crewai import Crew, Agent, Task
from crewai.project import CrewBase, task, agent, crew
from env import (
    OPENAI_API_KEY,
    GOOGLE_API_KEY,
    NAVER_API_CLIENT_ID,
    NAVER_API_SECRET_KEY,
)

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


@CrewBase
class ChatBotCrew:
    @agent
    def communication_agent(self) -> Agent:
        return Agent(
            role="전문 소통 분석가",
            goal="사용자의 질문을 심층적으로 분석하고, 가장 정확하고 유용한 정보를 찾아내어 전달한다.",
            backstory="""
            당신은 최첨단 AI 기술과 깊이 있는 데이터 분석 능력을 겸비한 전문 정보 분석가입니다.
            어떤 질문이든 그 본질을 파악하고, 웹 검색과 같은 강력한 도구를 활용하여
            사용자에게 가장 필요한 맞춤형 답변을 제공하는 것을 사명으로 삼고 있습니다.
            """,
            llm="openai/o4-mini",
            tools=[],
        )

    @task
    def communication_task(self) -> Task:
        return Task(
            agent=self.communication_agent(),
            description="""
            사용자로부터 받은 메시지('{message}')를 단계별로 분석합니다.
            1. 질문의 핵심 키워드와 숨은 의도를 파악합니다.
            2. 필요 시, 웹 검색 도구를 사용하여 관련 최신 정보를 찾습니다.
            3. 수집된 정보를 종합하여 사용자가 이해하기 쉬운 형태로 명확하고 친절한 답변을 생성합니다.
            """,
            expected_output="""
            사용자의 질문 의도에 완벽하게 부합하는, 명확하고 간결하며 친절한 톤의 한국어 답변.
            질문이 정보성 질문의 경우, 핵심 내용을 요약하고 신뢰할 수 있는 출처(URL)를 포함해야 합니다.
            분석 과정이나 단계별 설명 없이, 최종 답변만 출력하세요.
            """,
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            name="ChatBotCrew",
            agents=[self.communication_agent()],
            tasks=[self.communication_task()],
            verbose=True,
        )


def main():
    """터미널 무한 루프 챗봇"""
    print("=" * 60)
    print("CrewAI 챗봇이 시작됐습니다.")
    print("종료하려면 'exit', 'quit', '종료' 중 하나를 입력하세요.")
    print("(또는 Ctrl+C / Ctrl+D 로 즉시 종료 가능)")
    print("=" * 60)
    # Crew 인스턴스는 매 입력마다 새로 생성 (CrewBase 패턴)
    while True:
        try:
            user_message = input("\n나: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n챗봇을 종료합니다. 안녕히 가세요.")
            break

        # 빈 입력은 건너뛰기
        if not user_message:
            continue

        # 종료 명령
        if user_message.lower() in ("exit", "quit", "종료"):
            print("챗봇을 종료합니다. 안녕히 가세요.")
            break

        # CrewAI 실행 → 결과 출력
        result = ChatBotCrew().crew().kickoff(inputs={"message": user_message}).raw
        print(f"\n에이전트: {result}")


if __name__ == "__main__":
    main()
