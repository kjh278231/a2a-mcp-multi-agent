# Sequential_Thinking_agent/agent.py
import os
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
from .prompt import INSTRUCTION, DESCRIPTION
from env import OPENAI_API_KEY

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

MODEL = LiteLlm("openai/gpt-4o")

root_agent = Agent(
    model=MODEL,
    name="sequential_thinking",
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        MCPToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="npx",
                    args=["-y", "@modelcontextprotocol/server-sequential-thinking"],
                ),
                timeout=15,
            )
        )
    ],
)
