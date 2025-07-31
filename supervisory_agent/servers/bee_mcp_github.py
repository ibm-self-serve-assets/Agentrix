import asyncio
import logging
import os
import sys
import traceback
from typing import Any

from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from beeai_framework.agents import AgentExecutionConfig
from beeai_framework.agents.react import ReActAgent
from beeai_framework.backend import ChatModel, ChatModelParameters
from beeai_framework.emitter import Emitter, EventMeta
from beeai_framework.errors import FrameworkError
from beeai_framework.logger import Logger
from beeai_framework.memory import TokenMemory
from beeai_framework.tools import AnyTool
from beeai_framework.tools.mcp import MCPTool
from servers.helpers import ConsoleReader
from src.core.llm_provider import LLMProvider

# Load environment variables
load_dotenv()

reader = ConsoleReader()

# Configure logging - using DEBUG instead of trace
logger = Logger("app", level=logging.DEBUG)

# Create server parameters for stdio connection
server_params = StdioServerParameters(
    command="npx",
    args=["-y", "@modelcontextprotocol/server-github"],
    env={
        "GITHUB_PERSONAL_ACCESS_TOKEN": os.environ["GITHUB_PERSONAL_ACCESS_TOKEN"],
        "PATH": os.getenv("PATH", default=""),
    },
)


async def create_agent(session: ClientSession) -> ReActAgent:
    """Create and configure the agent with tools and LLM"""

    llm_provider = LLMProvider()
    llm = llm_provider.get_llm("openai", model="gpt-3.5-turbo")
    
    # Configure tools
    tools = await MCPTool.from_client(session)
    print("Discovered tools:")
    for tool in tools:
        print(f"- {tool.name}")

    # Create agent with memory and tools
    agent = ReActAgent(llm=llm, tools=tools, memory=TokenMemory(llm))
    return agent


def process_agent_events(data: Any, event: EventMeta) -> None:
    """Process agent events and log appropriately"""

    if event.name == "error":
        reader.write("Agent 🤖 : ", FrameworkError.ensure(data.error).explain())
    elif event.name == "retry":
        reader.write("Agent 🤖 : ", "retrying the action...")
    elif event.name == "update":
        reader.write(f"Agent({data.update.key}) 🤖 : ", data.update.parsed_value)
    elif event.name == "start":
        reader.write("Agent 🤖 : ", "starting new iteration")
    elif event.name == "success":
        reader.write("Agent 🤖 : ", "success")
    else:
        pass


def observer(emitter: Emitter) -> None:
    emitter.on("*.*", process_agent_events)


async def get_agent(prompt) -> ReActAgent:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()
        agent = await create_agent(session)
        response = await agent.run(
            prompt=prompt,
            execution=AgentExecutionConfig(max_retries_per_step=3, total_max_retries=10, max_iterations=20),
        ).observe(observer)
    
        return response

async def get_agent_response(prompt: str):
    return await get_agent(prompt)