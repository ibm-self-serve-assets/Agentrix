from beeai_framework.agents.react.agent import ReActAgent
from beeai_framework.memory import TokenMemory
from beeai_framework.memory.token_memory import TokenMemory
from beeai_framework.emitter import Emitter, EventMeta
from beeai_framework.errors import FrameworkError
from src.core.llm_provider import LLMProvider

from src.tools.weather_tool import weather_tool
from src.tools.maximo_location_tool import maximo_get_location
from src.tools.maximo_post_workorder_dates_tool import update_workorder_tool


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

def get_beeai_framework_weather_agent() -> ReActAgent:

    llm_provider = LLMProvider()
    llm = llm_provider.get_llm("watsonx", model="meta-llama/llama-3-3-70b-instruct")

    return ReActAgent(
        llm=llm, 
        tools=[weather_tool,maximo_get_location,update_workorder_tool], 
        memory=TokenMemory(llm)
    )

def get_beeai_framework_summary_agent() -> ReActAgent:

    llm_provider = LLMProvider()
    llm = llm_provider.get_llm("watsonx", model="meta-llama/llama-3-3-70b-instruct")

    return ReActAgent(
        llm=llm, 
        tools=[], 
        memory=TokenMemory(llm)
    )