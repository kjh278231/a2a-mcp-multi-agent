import os
import base64
from datetime import datetime
from crewai import Crew, Agent, Task
from crewai.project import CrewBase, task, agent, crew
from openai import OpenAI
from openai.types import ImagesResponse
from env import OPENAI_API_KEY

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
client = OpenAI(api_key=OPENAI_API_KEY)


@CrewBase
class PromptMakerCrew:
    @agent
    def prompt_maker_agent(self) -> Agent:
        return Agent(
            role="최고의 이미지 프롬프트 엔지니어",
            goal="사용자가 만들고 싶어하는 이미지의 의도를 철저하게 분석해서 이미지 생성 AI가 가장 잘 만들 수 있도록 하는 최고의 prompt를 만들어준다. 사용자가 한글로 작성해도 prompt는 영어로 하는게 더 좋기에 영어로 prompt를 만들어줘야 함 ",
            backstory="""
	            당신은 세계 최고의 이미지 생성 AI 프롬프트 엔지니어입니다.
							당신은 수년간 다양한 이미지 생성 모델(Midjourney, DALL-E, Stable Diffusion, Google Imagen)을 다루면서
							각 모델의 특성과 강점을 완벽히 이해하고 있습니다.

							당신의 전문성:
							1. 사용자의 모호한 요청을 명확하고 구체적인 시각적 설명으로 변환
							2. 예술 스타일, 촬영 기법, 조명, 색감, 구도 등 시각적 요소를 정교하게 표현
							3. 문화적, 역사적, 기술적 맥락을 프롬프트에 통합
							4. 반복적인 개선를 통해 사용자의 의도를 완벽히 구현

							당신은 항상:
							- 사용자의 요청을 깊이 있게 분석
							- 누락된 세부사항을 창의적으로 추가
							- 예술적 언어와 기술적 정확성을 결합
							- 결과 이미지가 전문가 수준의 시각적 품질을 갖도록 보장
							- 영어 프롬프트로만 최종 결과를 제공
						""",
            llm="openai/gpt-4o-mini",
            verbose=True,
        )

    @task
    def make_prompt_task(self) -> Task:
        return Task(
            description="사용자 요청: {message}\n\n사용자의 요청을 분석하여 이미지 생성 AI를 위한 최고의 영문 프롬프트를 작성하세요. 프롬프트는 다음을 포함해야 합니다:\n1. 주제와 초점\n2. 예술 스타일 및 미학\n3. 구도 및 관점\n4. 조명 조건\n5. 색감 팔레트\n6. 분위기 및 톤\n7. 세부 수준 및 품질 지정자\n\n최종 프롬프트만 제공하세요.",
            expected_output="영어로 작성된 상세하고 구체적인 이미지 생성 프롬프트",
            agent=self.prompt_maker_agent(),
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=True,
        )


def create_image(message: str):
    """
    사용자 입력으로부터 이미지를 생성합니다.

    Args:
        message (str): 사용자가 생성하고 싶은 이미지에 대한 설명
    """
    print(f"프롬프트 생성 중... (입력: {message})")

    # PromptMakerCrew를 통해 최고의 프롬프트 생성
    prompt_maker_crew = PromptMakerCrew().crew()
    prompt = prompt_maker_crew.kickoff(inputs={"message": message}).raw

    print(f"\n생성된 프롬프트:\n{prompt}\n")
    print("이미지 생성 중... (gpt-image-2)")

    # OpenAI 이미지 API 로 이미지 생성
    # 최신 모델을 쓰려면 model 만 "gpt-image-2" 로 바꾸면 된다
    # 나머지 파라미터·응답 형식은 동일하다.
    result: ImagesResponse = client.images.generate(
        model="gpt-image-2",
        prompt=prompt,
        size="1024x1024",
        quality="low",
    )
    image_b64 = result.data[0].b64_json

    # 생성된 이미지 저장 (base64 → PNG)
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"generated_image_sample.png"
    try:
        with open(filename, "wb") as f:
            f.write(base64.b64decode(image_b64))
        print(f"이미지가 저장되었습니다: {filename}")
    except Exception as e:
        print(f"이미지 저장 중 오류 발생: {e}")


# 실행 예제
if __name__ == "__main__":
    create_image("해변에 앉아있는 밀집모자 해적단")
