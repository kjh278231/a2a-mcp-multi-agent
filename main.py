import os
from crewai import Crew, Agent, Task
from crewai.project import CrewBase, task, agent, crew
from env import (
    OPENAI_API_KEY,
    GOOGLE_API_KEY,
    NAVER_API_CLIENT_ID,
    NAVER_API_SECRET_KEY,
)
from tools import web_search_tool, global_news_rss_tool, korean_news_rss_tool

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

FETCH_NEWS_COUNT = 10


@CrewBase
class NewsCrew:

    @agent
    def research_specialist_agent(self) -> Agent:
        return Agent(
            role="리서치 전문가 (Research Specialist)",
            goal="최신 뉴스 아티클 RSS를 최대한 많이 수집한다",
            backstory="""
            당신은 세계적인 뉴스 통신사에서 20년간 근무한 베테랑 리서치 전문가입니다.
            다양한 소스(Google News RSS, 국내외 주요 언론사)를 샅샅이 뒤져서
            관련성이 높고 최신의 핫한 뉴스 기사를 찾아내는 전문가입니다.
            RSS 피드를 통해 실시간으로 업데이트되는 뉴스를 수집하고,
            중복을 제거하여 가장 가치 있는 정보만을 선별합니다.
            """,
            llm="openai/o4-mini",
            verbose=True,
            tools=[korean_news_rss_tool, global_news_rss_tool],
        )

    @agent
    def senior_editor_agent(self) -> Agent:
        return Agent(
            role="수석 편집자 (Senior Editor)",
            goal="리서치 전문가가 수집한 뉴스 아티클을 검토하여 가장 가치 있는 정보를 선별한다",
            backstory="""
            당신은 세계적인 뉴스 통신사에서 30년간 근무한 수석 편집자입니다.
            수많은 뉴스 기사를 검토하고, 그 중에서 가장 가치 있고 독자들에게 중요한 정보를 선별하는 전문가입니다.
            리서치 전문가가 수집한 뉴스 아티클을 꼼꼼히 검토하여, 중복된 정보나 중요하지 않은 내용을 제거하고,
            독자들에게 가장 유익한 뉴스를 선정하는 역할을 맡고 있습니다.
            """,
            llm="openai/o4-mini",
            verbose=True,
        )

    @agent
    def news_curator_agent(self) -> Agent:
        return Agent(
            role="뉴스 큐레이터 (News Curator)",
            goal="수석 편집자가 선별한 뉴스 아티클을 바탕으로 독자들에게 가장 유익한 뉴스를 선정한다",
            backstory="""
            당신은 세계적인 뉴스 통신사에서 15년간 근무한 뉴스 큐레이터입니다.
            수석 편집자가 선별한 뉴스 아티클을 바탕으로, 독자들에게 가장 유익한 뉴스를 선정하는 전문가입니다.
            다양한 관점에서 뉴스를 분석하고, 독자들이 관심을 가질 만한 주제를 중심으로 뉴스를 큐레이션하는 역할을 맡고 있습니다.
            """,
            llm="openai/o4-mini",
            verbose=True,
            tools=[web_search_tool],
        )

    #############################################
    @task
    def research_global_news_task(self) -> Task:
        return Task(
            agent=self.research_specialist_agent(),
            description=f"""
            글로벌 뉴스 RSS 소스에서 최신 뉴스 기사를 수집합니다.

            **필수 작업 순서 (반드시 따라야 함):**

            1. **첫 번째로 global_news_rss_tool()을 호출**하여 실제 RSS 데이터를 가져와야 합니다.
            2. **도구 호출 결과를 기다리고 받은 실제 데이터만 사용**해야 합니다.
            3. **절대로 임의의 뉴스나 예시 데이터를 생성하지 마세요.**
            4. RSS 도구에서 받은 데이터를 중요도와 관련성에 따라 정렬하세요 (최신순 우선).
            5. 중복된 기사를 제거하세요.
            6. 상위 {FETCH_NEWS_COUNT}개의 가장 핫한 이슈 기사를 선별하세요.

            **경고: 이 작업은 실제 뉴스 수집이므로 반드시 global_news_rss_tool을 호출해야 하며,
            그 이전 날짜의 가짜 뉴스를 만들어내는 것은 절대 금지됩니다.
            RSS 도구는 현재의 실제 뉴스를 제공합니다.**
            """,
            expected_output="""
            다음 형식의 JSON 리스트:
            [
                {
                    "title": "기사 제목",
                    "link": "기사 URL",
                    "summary": "기사 요약",
                    "published": "발행 날짜",
                    "source": "뉴스 소스",
                    "importance_score": "1-10 중요도 점수"
                }
            ]
            최대 {FETCH_NEWS_COUNT}개의 글로벌 뉴스 기사 목록
            """,
            output_file="output/global_news.json",
        )

    @task
    def research_korea_news_task(self) -> Task:
        return Task(
            agent=self.research_specialist_agent(),
            description=f"""
            한국 뉴스 RSS 소스에서 최신 뉴스 기사를 수집합니다.

            **필수 작업 순서 (반드시 따라야 함):**

            1. **첫 번째로 korean_news_rss_tool()을 호출**하여 실제 RSS 데이터를 가져와야 합니다.
            2. **도구 호출 결과를 기다리고 받은 실제 데이터만 사용**해야 합니다.
            3. **절대로 임의의 뉴스나 예시 데이터를 생성하지 마세요.**
            4. RSS 도구에서 받은 데이터를 중요도와 관련성에 따라 정렬하세요 (최신순 우선).
            5. 중복된 기사를 제거하세요.
            6. 상위 {FETCH_NEWS_COUNT}개의 가장 핫한 이슈 기사를 선별하세요.

            **경고: 이 작업은 실제 뉴스 수집이므로 반드시 korean_news_rss_tool을 호출해야 하며,
            그 이전 날짜의 가짜 뉴스를 만들어내는 것은 절대 금지됩니다.
            RSS 도구는 현재의 실제 뉴스를 제공합니다.**
            """,
            expected_output="""
            다음 형식의 JSON 리스트:
            [
                {
                    "title": "기사 제목",
                    "link": "기사 URL",
                    "summary": "기사 요약",
                    "published": "발행 날짜",
                    "source": "뉴스 소스",
                    "importance_score": "1-10 중요도 점수"
                }
            ]
            최대 {FETCH_NEWS_COUNT}개의 한국 뉴스 기사 목록
            """,
            output_file="output/korea_news.json",
        )

    #############################################
    @task
    def edit_and_summarize_articles_task(self) -> Task:
        return Task(
            agent=self.senior_editor_agent(),
            description="""
            리서치 에이전트가 수집한 글로벌 뉴스와 한국 뉴스 기사들의 실제 본문을 추출하고 요약합니다.

            **필수 작업 순서:**

            1. **이전 Task 결과 활용**:
               - research_global_news_task와 research_korea_news_task에서 수집된 모든 뉴스 기사 데이터를 사용합니다.
               - 각 기사의 link 필드에 있는 URL에 접근하여 실제 기사 본문을 추출합니다.

            2. **기사 본문 추출**:
               - 각 뉴스 링크에 접속하여 기사의 실제 본문 내용을 추출합니다.
               - 광고, 관련 기사, 댓글 등 불필요한 내용은 제외하고 핵심 기사 내용만 추출합니다.
               - 제목, 날짜, 본문, 출처를 명확히 구분하여 추출합니다.

            3. **내용 요약 및 번역**:
               - 영어 기사는 한국어로 자연스럽게 번역합니다.
               - 각 기사의 핵심 내용을 2-3문장으로 요약합니다.
               - 원문의 의미를 훼손하지 않으면서 명확하고 간결하게 정리합니다.

            4. **전체 기사 처리**:
               - 수집된 모든 기사에 대해 작업을 수행합니다 (선별하지 말고 전체 처리).
               - 각 기사마다 동일한 품질로 처리합니다.
               - 접속 불가능한 링크는 건너뛰고, 가능한 기사들만 처리합니다.

            **중요 지침:**
            - 실제 웹사이트에 접속하여 기사 본문을 가져와야 합니다.
            - 기존 RSS 요약문에 의존하지 말고 전체 기사를 읽고 요약하세요.
            - 모든 외국어 기사는 한국어로 번역하세요.
            - 일관된 형식으로 모든 기사를 처리하세요.
            """,
            expected_output="""
            다음 형식의 JSON 리스트:
            [
                {
                    "original_title": "원본 기사 제목",
                    "title": "번역된 기사 제목 (한국어)",
                    "published_date": "발행 날짜",
                    "source": "출처",
                    "category": "카테고리 (정치/경제/사회/국제/스포츠/문화 등)",
                    "original_summary": "원본 RSS 요약",
                    "full_content_summary": "실제 기사 본문 기반 상세 요약 (한국어, 2-3문장)",
                    "key_points": ["핵심 포인트 1", "핵심 포인트 2", "핵심 포인트 3"],
                    "article_url": "기사 원본 URL",
                    "importance_score": "1-10 중요도 점수"
                }
            ]
            글로벌 뉴스와 한국 뉴스 모든 기사의 상세 분석 결과
            """,
            output_file="output/edited_articles.json",
        )

    #############################################
    @task
    def curate_final_news_task(self) -> Task:
        return Task(
            agent=self.news_curator_agent(),
            description="""
            편집된 모든 뉴스 기사들을 분석하여 가장 중요하고 적절한 10개의 뉴스를 선별하고 최종 리포트를 작성합니다.

            **필수 작업 순서:**

            1. **이전 Task 결과 활용**:
               - edit_and_summarize_articles_task에서 생성된 모든 편집 완료된 기사 데이터를 분석합니다.
               - 각 기사의 중요도 점수, 카테고리, 내용을 종합적으로 평가합니다.

            2. **뉴스 선별 기준**:
               - 중요도 점수가 양호한 기사들을 우선 고려합니다 (7점 이상 우선)
               - 글로벌 뉴스는 전체의 30% 정도 (3개)로 제한합니다
               - 한국 뉴스는 전체의 70% 정도 (7개)로 구성합니다
               - 다양한 카테고리의 균형을 맞춥니다 (정치/경제/사회/국제 등)
               - 시의성과 사회적 파급효과를 고려합니다

            3. **최종 리포트 작성**:
               - 선별된 10개 기사를 보기 좋게 정리합니다
               - 각 기사별로 헤드라인, 요약, 원문 소스, 출처를 명확히 표시합니다
               - 전체적인 뉴스 동향에 대한 간단한 요약을 추가합니다
               - 독자가 이해하기 쉬운 형태로 구성합니다

            **선별 우선순위:**
            1. 중요도 점수 (7점 이상)
            2. 시의성 (최신성)
            3. 사회적 파급효과
            4. 카테고리 다양성
            5. 글로벌/국내 뉴스 비중 (3:7)
            """,
            expected_output="""
            다음과 같은 형식의 최종 뉴스 리포트 (TXT 형식):

            ============================================
                        오늘의 주요 뉴스 리포트
                        [날짜: YYYY-MM-DD]
            ============================================

            📊 **뉴스 브리핑 요약**
            - 글로벌 뉴스: 3건 (30%)
            - 국내 뉴스: 7건 (70%)
            - 주요 이슈: [전체적인 동향 요약]

            ============================================
                            📰 주요 뉴스
            ============================================

            [1] 🌍 [카테고리] 헤드라인
            📅 발행일: YYYY-MM-DD
            📰 출처: 언론사명
            🔗 원문: URL

            📝 요약:
            [핵심 내용 요약 2-3문장]

            💡 핵심 포인트:
            • 핵심 포인트 1
            • 핵심 포인트 2
            • 핵심 포인트 3

            ────────────────────────────────────────

            [반복...]

            ============================================
                        📋 전체 뉴스 동향 분석
            ============================================

            **오늘의 주요 이슈:**
            [선별된 10개 뉴스를 바탕으로 한 전체적인 동향 분석 및 요약]

            **카테고리별 분포:**
            - 정치: X건
            - 경제: X건
            - 사회: X건
            - 국제: X건
            - 기타: X건

            **주목할 만한 트렌드:**
            [전반적인 뉴스 트렌드 및 패턴 분석]

            ============================================
            """,
            output_file="output/curated_news.txt",
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.research_specialist_agent(),
                self.senior_editor_agent(),
                self.news_curator_agent(),
            ],
            tasks=[
                self.research_global_news_task(),
                self.research_korea_news_task(),
                self.edit_and_summarize_articles_task(),
                self.curate_final_news_task(),
            ],
            verbose=True,
        )


NewsCrew().crew().kickoff()
