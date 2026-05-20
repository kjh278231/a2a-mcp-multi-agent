from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from .prompt import DESCRIPTION, INSTRUCTION
from .tools import compose_video

video_composer_agent = Agent(
    name="VideoComposerAgent",
    model=LiteLlm(model="openai/gpt-4o"),
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    output_key="video_composer_output",
    tools=[
        compose_video,
    ],
)
