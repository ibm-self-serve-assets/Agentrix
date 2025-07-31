from beeai_framework.agents.react.agent import ReActAgent
from beeai_framework.memory import TokenMemory
from beeai_framework.memory.token_memory import TokenMemory
from beeai_framework.emitter import Emitter, EventMeta
from beeai_framework.errors import FrameworkError
from src.core.llm_provider import LLMProvider

from src.tools.get_workorder_description_tool import fetch_workorder_description
from src.tools.get_inventory_item_and_storelocation_detail_tool import maximo_get_item_storelocation_details
from src.tools.post_inventory_tool import post_multiple_inventory


def process_agent_events(data, event: EventMeta) -> None:
    """Process agent events and log appropriately"""

    if event.name == "error":
        print("Agent 🤖 : ", FrameworkError.ensure(data.error).explain())
    elif event.name == "retry":
        print("Agent 🤖 : ", "retrying the action...")
    elif event.name == "update":
        print(f"Agent({data.update.key}) 🤖 : ", data.update.parsed_value)
    elif event.name == "start":
        print("Agent 🤖 : ", "starting new iteration")
    elif event.name == "success":
        print("Agent 🤖 : ", "success")
    else:
        pass

def observer(emitter: Emitter) -> None:
    emitter.on("*.*", process_agent_events)

def get_beeai_framework_agent() -> ReActAgent:

    llm_provider = LLMProvider()
    llm = llm_provider.get_llm("watsonx", model="meta-llama/llama-3-3-70b-instruct")

    return ReActAgent(
        llm=llm, 
        tools=[fetch_workorder_description,maximo_get_item_storelocation_details,post_multiple_inventory], 
        memory=TokenMemory(llm)
    )
