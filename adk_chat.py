import asyncio
from google.adk import Runner
from google.genai import types
from google.adk.agents import BaseAgent
from google.adk.sessions import InMemorySessionService

session_service = InMemorySessionService()


async def async_chat(
    message: str,
    agent: BaseAgent,
    user_id: str = "default_user",
    app_name: str = "default_app",
    session_id="default_session",
):
    result = ""

    await session_service.create_session(
        app_name=app_name, session_id=session_id, user_id=user_id
    )

    runner = Runner(app_name=app_name, agent=agent, session_service=session_service)

    event = runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=types.Content(parts=[types.Part(text=message)], role="user"),
    )

    async for response in event:
        if (
            response.content
            and response.content.role == "model"
            and response.content.parts
        ):
            for part in response.content.parts:
                if part.text:
                    result = part.text
    return result


def chat(
    message: str,
    agent: BaseAgent,
    user_id: str = "default_user",
    app_name: str = "default_app",
    session_id: str = "default_session",
):
    return asyncio.run(
        async_chat(
            message=message,
            agent=agent,
            user_id=user_id,
            app_name=app_name,
            session_id=session_id,
        )
    )
