import os
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.models.lite_llm import LiteLlm
from env import OPENAI_API_KEY
from .prompt import DESCRIPTION, INSTRUCTION
from .sub_agents.content_planner.agent import content_planner_agent
from .sub_agents.content_maker.agent import content_maker_agent
from .sub_agents.video_composer.agent import video_composer_agent
from google.genai import types
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


def before_model_call_back(llm_request: LlmRequest, callback_context: CallbackContext):
    """
    [Note]
    https://google.github.io/adk-docs/callbacks/#introduction-what-are-callbacks-and-why-use-them
    callback에 뭘 return하느냐에 따라 모든게 달라진다. (오버라이딩)
    prompt validation 할때 쓴다고 보면됨
    """
    print(
        f"Agent {callback_context.agent.name} is about to call the model with input: {callback_context.tool_context.input}"
    )
    history = llm_request.contents
    last_message = history[-1]
    if last_message and last_message.parts and last_message.role == "user":
        text = str(last_message.parts[0].text)
        if "hello" in text:  # hello라고 사용자가 말하면 필터 기능
            return LlmResponse(
                content=types.Content(
                    parts=[
                        types.Part(text="Sorry I can't help with that."),
                    ],
                    role="model",
                )
            )
    return None  # default


root_agent = Agent(
    name="ShortsCreatorAgent",
    model=LiteLlm(model="openai/gpt-4o"),
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        AgentTool(agent=content_planner_agent),
        AgentTool(agent=content_maker_agent),
        AgentTool(agent=video_composer_agent),
    ],
)
