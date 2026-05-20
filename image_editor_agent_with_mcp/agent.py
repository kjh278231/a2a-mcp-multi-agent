# image_editor_agent_with_mcp/agent.py
import os
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
from .prompt import INSTRUCTION, DESCRIPTION
from env import OPENAI_API_KEY

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

MODEL = LiteLlm("openai/gpt-4o")

root_agent = Agent(
    model=MODEL,
    name="image_editor",
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        MCPToolset(
            connection_params=StreamableHTTPConnectionParams(
                url="http://localhost:5000/mcp"
            )
        )
    ],
)
