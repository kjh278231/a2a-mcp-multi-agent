import os
import base64
from datetime import datetime
from crewai import Crew, Agent, Task
from crewai.project import CrewBase, task, agent, crew
from openai import OpenAI
from env import OPENAI_API_KEY

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
client = OpenAI(api_key=OPENAI_API_KEY)


@CrewBase
class EditImagePromptMakerCrew:
    @agent
    def edit_prompt_maker_agent(self) -> Agent:
        return Agent(
            role="최고의 이미지 편집 프롬프트 엔지니어",
            goal="사용자가 기존 이미지에 대해 원하는 편집 의도를 철저하게 분석해서 이미지 편집 AI가 가장 잘 수행할 수 있도록 하는 최고의 편집 프롬프트를 만들어준다. 사용자가 한글로 작성해도 프롬프트는 영어로 하는게 더 좋기에 영어로 프롬프트를 만들어줘야 함",
            backstory="""당신은 세계 최고의 이미지 편집 프롬프트 엔지니어입니다.
당신은 수년간 다양한 이미지 편집 AI 모델(Inpainting, Image-to-Image 변환)을 다루면서
각 모델의 특성과 강점을 완벽히 이해하고 있습니다.

당신의 전문성:
1. 사용자의 편집 요청을 명확하고 정확한 편집 지시사항으로 변환
2. 편집 영역을 정확히 파악하고 설명
3. 원본 이미지와의 일관성과 매끄러운 통합을 보장하는 지시사항 작성
4. 색감, 조명, 스타일의 일관성을 유지하면서 편집
5. 반복적인 개선을 통해 사용자의 의도를 완벽히 구현

당신은 항상:
- 사용자의 편집 요청을 깊이 있게 분석
- 편집해야 할 구체적인 영역과 방식을 명확히 지정
- 원본 이미지의 스타일과 품질 유지
- 편집 부분이 자연스럽게 통합되도록 보장
- 영어 프롬프트로만 최종 결과를 제공""",
            llm="openai/gpt-4o-mini",
            verbose=True,
        )

    @task
    def make_edit_prompt_task(self) -> Task:
        return Task(
            description="사용자의 이미지 편집 요청: {message}\n\n사용자가 기존 이미지에 대해 원하는 편집을 분석하여 이미지 편집 AI를 위한 최고의 영문 프롬프트를 작성하세요. 프롬프트는 다음을 포함해야 합니다:\n1. 편집할 영역의 명확한 지정\n2. 원하는 변경 사항의 구체적 설명\n3. 유지해야 할 원본 요소\n4. 조명, 색감, 스타일의 일관성 지시\n5. 매끄러운 통합 방법\n\n최종 프롬프트만 제공하세요.",
            expected_output="영어로 작성된 상세하고 구체적인 이미지 편집 프롬프트",
            agent=self.edit_prompt_maker_agent(),
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=True,
        )


def edit_image(image_path: str, edit_request: str):
    """
    로컬 이미지 파일을 편집합니다.

    Args:
        image_path (str): 편집할 이미지의 로컬 파일 경로
        edit_request (str): 사용자의 편집 요청 설명
    """
    print(f"편집 프롬프트 생성 중... (요청: {edit_request})")

    # EditImagePromptMakerCrew를 통해 편집 프롬프트 생성
    edit_prompt_maker_crew = EditImagePromptMakerCrew().crew()
    edit_prompt = edit_prompt_maker_crew.kickoff(inputs={"message": edit_request}).raw

    print(f"\n생성된 편집 프롬프트:\n{edit_prompt}\n")
    print("이미지 편집 중... (gpt-image-2)")

    # OpenAI 이미지 API 로 이미지 편집 (원본 이미지를 파일로 전달)
    with open(image_path, "rb") as image_file:
        result = client.images.edit(
            model="gpt-image-2",
            image=image_file,
            prompt=edit_prompt,
            size="1024x1024",
        )
    image_b64 = result.data[0].b64_json

    # 편집된 이미지 저장 (base64 → PNG)
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"edited_image_{current_time}.png"
    try:
        with open(filename, "wb") as f:
            f.write(base64.b64decode(image_b64))
        print(f"편집된 이미지가 저장되었습니다: {filename}")
    except Exception as e:
        print(f"이미지 저장 중 오류 발생: {e}")


# 실행 예제
if __name__ == "__main__":
    # 7번 image_creator.py 로 생성한 이미지 파일을 입력으로 사용
    edit_image("generated_image_sample.png", "하늘을 더 선명한 파란색으로 변경해주세요")
