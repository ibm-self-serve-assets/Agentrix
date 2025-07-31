from collections.abc import AsyncGenerator
from functools import reduce
import asyncio
from acp_sdk import Message
from acp_sdk.models import MessagePart
from acp_sdk.server import Context, Server
from beeai_framework.agents.react import ReActAgent
from beeai_framework.backend.chat import ChatModel
from beeai_framework.memory import TokenMemory
from beeai_framework.utils.dicts import exclude_none
from src.core.llm_provider import LLMProvider
# from src.tools.get_unplanned_workorders_tool import fetch_workorder
from translation_tool import TranslationTool
from labor_tool import LaborTool
from inventory_tool import InventoryTool
from weather_tool import WeatherTool
from unplanned_workorder_tool import FetchUnplannedWorkorderTool
from dotenv import load_dotenv
from beeai_framework.agents.types import AgentExecutionConfig
from beeai_framework.backend.message import Message, SystemMessage
import re

server = Server()


@server.agent()
async def translation_spanish(input: list[Message]) -> AsyncGenerator:
    # llm = ChatModel.from_name("ollama:llama3.1:8b")
    llm_provider = LLMProvider()
    llm = llm_provider.get_llm("watsonx", model="meta-llama/llama-3-3-70b-instruct")

    agent = ReActAgent(llm=llm, tools=[], memory=TokenMemory(llm))
    response = await agent.run(prompt="Translate the given text to Spanish. The text is: " + str(input))

    yield MessagePart(content=response.result.text)


@server.agent()
async def get_workorder_agent(input: list[Message]) -> AsyncGenerator:
    # llm = ChatModel.from_name("ollama:llama3.1:8b")
    llm_provider = LLMProvider()
    llm = llm_provider.get_llm("watsonx", model="meta-llama/llama-3-3-70b-instruct")

    agent = ReActAgent(llm=llm, tools=[FetchUnplannedWorkorderTool()], memory=TokenMemory(llm))
    response = await agent.run(prompt="""
    You are a Maximo assistant. Your task is to get the list of unplanned work orders using the `fetch_workorder` tool.

    Call the tool once, and then respond to the user with a message like:
    "You can try with the following unplanned workorders: <tool_output>"

    Only use the actual output from the tool. Do not invent anything.
    """)

    yield MessagePart(content=response.result.text)


@server.agent()
async def labor_agent(input: list[Message]) -> AsyncGenerator:
    from apis.generation_labor import generate, generate_stream
    result = await generate( str(input))
    print("result of labor = ",result)
    # return result
    yield MessagePart(content=result)

@server.agent()
async def inventory_agent(input: list[Message]) -> AsyncGenerator:
    from apis.generation_inventory import generate, generate_stream
    result = await generate( str(input))
    print("result of inventory = ",result)
    # return result
    yield MessagePart(content=result)

@server.agent()
async def weather_agent(input: list[Message]) -> AsyncGenerator:
    from apis.generation_weather import generate, generate_stream
    result = await generate( str(input))
    print("result of weather = ",result)
    # return result
    yield MessagePart(content=result)


@server.agent()
async def translation_french(input: list[Message]) -> AsyncGenerator:
    # llm = ChatModel.from_name("ollama:llama3.1:8b")
    llm_provider = LLMProvider()
    llm = llm_provider.get_llm("watsonx", model="meta-llama/llama-3-3-70b-instruct")

    agent = ReActAgent(llm=llm, tools=[], memory=TokenMemory(llm))
    response = await agent.run(prompt="Translate the given text to French. The text is: " + str(input))

    yield MessagePart(content=response.result.text)

#  "instructions": """
#                             You're an expert in planning a workorder. Based on the user's intent, you must decide which agent to call:

#                             - If the user is asking about weather conditions or planning based on weather, call the `weather_agent` using the `WeatherTool`.
#                             - If the user is trying to plan or schedule labor for a workorder, call the `labor_agent` using the `LaborTool`.
#                             - If the user is trying to manage or check inventory requirements for a workorder, call the `inventory_agent` using the `InventoryTool`.

#                             Use the tools accordingly, and always respond with a user-friendly summary such as "Planning is done", "Inventory updated", or "Weather check complete" based on the agent response.
#                             """


#  "instructions": """
#                         You're an expert in planning a workorder. Based on the user's intent, you must decide which agent to call:

#                         - If the user is asking about weather conditions or planning based on weather, call the `weather_agent` using the `WeatherTool`.
#                         - If the user is trying to plan or schedule labor for a workorder, call the `labor_agent` using the `LaborTool`.
#                         - If the user is trying to manage or check inventory requirements for a workorder, call the `inventory_agent` using the `InventoryTool`.
#                         - If the user's query is related to planning or scheduling but **does not include any work order number**, call the `get_workorder_agent` using `FetchUnplannedWorkorderTool` to retrieve unplanned work orders first.

#                         Use the tools accordingly, and always respond with a user-friendly summary such as "Planning is done", "Inventory updated", "Weather check complete", or "Retrieved unplanned workorders" based on the agent response.
#                         """


@server.agent(name="router")
async def main_agent(input: list[Message], context: Context) -> AsyncGenerator:
    # llm = ChatModel.from_name("ollama:llama3.1:8b")
    llm_provider = LLMProvider()
    llm = llm_provider.get_llm("watsonx", model="meta-llama/llama-3-3-70b-instruct")
    labor_check= 0
    agent = ReActAgent(
        llm=llm,
        tools=[LaborTool(),InventoryTool(),WeatherTool(),FetchUnplannedWorkorderTool()], #TranslationTool()
        templates={
            "system": lambda template: template.update(
                defaults=exclude_none(
                    {
                        "instructions": """
You're an expert in planning a workorder. Based on the user's intent, you must decide which agent to call:

- If the user's query is related to planning or scheduling but **does not include any work order number**, call the `get_workorder_agent` using `FetchUnplannedWorkorderTool` to retrieve unplanned work orders first.
- If the user is asking about weather conditions or planning based on weather, call the `weather_agent` using the `WeatherTool`.
- If the user is trying to plan or schedule labor for a workorder, call the `labor_agent` using the `LaborTool`.
- If the user is trying to manage or check inventory requirements for a workorder, call the `inventory_agent` using the `InventoryTool`.

If **any agent fails to process the task** (e.g., labor is already assigned, inventory is already updated, or weather conditions are already checked), then as a fallback, **call the `get_workorder_agent` using `FetchUnplannedWorkorderTool`** to retrieve a new list of unplanned work orders.

In such cases, respond gracefully with a message like:
- "Labor is already assigned to workorder 1208. Please try with another workorder. Here are some unplanned workorders you can use: ..."
- "Inventory has already been updated for workorder 1452. Try with a different workorder. Here's a list of unplanned workorders: ..."
- "Weather is already checked and planning is complete for workorder 1320. Try another. Available unplanned workorders: ..."

Use the tools accordingly, and always respond with a user-friendly summary.
"""

                       ,
                        "role": "system",
                    }
                )
            )
        },
        memory=TokenMemory(llm),
    )

    prompt = reduce(lambda x, y: x + y, input)
    response = await agent.run(str(prompt))

    yield MessagePart(content=response.result.text)


server.run()


# import asyncio
# from acp_sdk import Message
# from acp_sdk.models import MessagePart  

# async def test_translation_french():
#     input_message = [
#         Message(parts=[MessagePart(content="hi good morning", content_type="text/plain")])
#     ]

#     # This returns an async generator
#     response_stream = translation_french(input=input_message)

#     # Consume it using async for
#     async for part in response_stream:
#         print("Response:", part.content)

# # Now run the test
# if __name__ == "__main__":
#     asyncio.run(test_translation_french())