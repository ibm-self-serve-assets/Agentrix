import asyncio
from typing import AsyncGenerator
import uuid
import time
import logging
import json
import re
from datetime import datetime, timedelta
from dotenv import load_dotenv
from beeai_framework.agents.types import AgentExecutionConfig
from src.tools.weather_tool import weather_tool
from src.tools.maximo_location_tool import maximo_get_location
from src.tools.maximo_post_workorder_dates_tool import update_workorder_tool
from beeai_framework.backend.message import (
    Message,
    SystemMessage,
)

load_dotenv()


# Configure logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def format_resp(struct: dict) -> str:
    """
    Formats the response as a string in the required format.

    Parameters
    ----------
    struct : dict
        The structured data to format.

    Returns
    -------
    str
        The formatted string.
    """
    return "data: " + json.dumps(struct) + "\n\n"


async def generate_stream(query, thread_id, model) -> AsyncGenerator[str, None]:
    """
    Generates a streaming response for a given query.

    Simulates a stream of events while processing the input query, yielding updates every 3 seconds,
    and sends the final result upon completion.

    Parameters
    ----------
    query : str
        The input query to process.
    thread_id : str
        The unique identifier of the thread.
    model : str
        The name of the model being used.

    Yields
    ------
    AsyncGenerator[str, None]
        A formatted event string for each step of the process.
    """
    gen_task = asyncio.create_task(generate(query))
    while not gen_task.done():

        current_timestamp = int(time.time())
        event = {
            "id": str(uuid.uuid4()),
            "object": "thread.run.step.delta",
            "created": current_timestamp,
            "thread_id": thread_id,
            "model": model,
            "choices": [
                {
                    "delta": {
                        "content": "",
                        "role": "system",
                    }
                }
            ],
        }
        event = format_resp(event)
        logger.info("Sending event content: " + event)

        yield event

        await asyncio.sleep(1)

    # Once gen_response is done, add the result to the stream
    result = await gen_task
    current_timestamp = int(time.time())
    event = {
        "id": str(uuid.uuid4()),
        "object": "thread.message.delta",
        "created": current_timestamp,
        "thread_id": thread_id,
        "model": model,
        "choices": [
            {
                "delta": {
                    "content": result,
                    "role": "assistant",
                }
            }
        ],
    }
    formatted_event = format_resp(event)
    yield formatted_event


async def generate(input_text: str) -> str:
    """
    Simulates a full processing function that generates a response.

    Parameters
    ----------
    input_text : str
        The input text to process.

    Returns
    -------
    str
        The generated response.
    """
    prompt = input_text

    from src.agents.get_agent import get_beeai_framework_agent, observer

    # Extract number from query
    match = re.search(r'\b\d+\b', prompt)

    if match:
        wonum = match.group(0)
    else:
        wonum = None

    if not wonum:
        summary = "Missing wonum , Work order number is required."
        return summary

    agent = get_beeai_framework_agent()

    # workorder_prompt = f"Get the location, city, latitude, and longitude for work order number {wonum} from Maximo ."
    workorder_prompt = f"""
    Retrieve and summarize the following information for work order **{wonum}** from Maximo:
    - Location
    - City
    - Latitude
    - Longitude

    Respond with a clear and complete sentence in this format:
    "Work order {wonum} is located at <Location>, <City> (Latitude: <Latitude>, Longitude: <Longitude>)."
    """


    # Run the agent using the maximo_location_tool
    location_response = await agent.run(
        workorder_prompt,
        execution=AgentExecutionConfig(
            max_retries_per_step=3,
            total_max_retries=10,
            max_iterations=20,
            # tools=maximo_get_location
        )
    ).observe(observer)

    print("location response from maximo tool = ",location_response)
    location_summary = '\n'.join([m.text for m in location_response.result.content])



    # weather_prompt = f"Give the weather forecast of {coords['CITY']} for given {coords['LONGITUDEX']} and {coords['LATITUDEY']} coordinates."
    # weather_prompt = f"Give the weather forecast of {location_response} coordinates."
    weather_prompt = f"""
    Using the provided coordinates from the location summary ({location_response}), generate a weather summary.

    Respond with a sentence like:
    "The current weather at <City> is <temperature>°C, with a wind speed of <wind speed> m/s."
    """

    weather_response = await agent.run(
            weather_prompt,
            execution=AgentExecutionConfig(
                max_retries_per_step=3,
                total_max_retries=10,
                max_iterations=20,
                # tools=weather_tool
            )
        ).observe(observer)
    
    weather_summary = '\n'.join([m.text for m in weather_response.result.content])
    
    # summary_prompt = f"The weather forecast is:\n{weather_response}\n\nBased on this, should we schedule the work order or delay it?"
    summary_prompt = f"""
        You are helping to determine if a work order should proceed based on weather conditions.

        Here is the weather forecast:
        {weather_response}

        Your response should include:
        1. A clear decision based on these rules:
            - If **heavy rain**, **storms**, **wind speeds above 10 m/s**, or **temperature below 5°C or above 40°C** → conclude: "Delay the work order."
            - Otherwise → conclude: "Schedule the work order."

        Example format:
        "Based on the current weather conditions, it is recommended to <schedule or delay> the work order."
        """



    summary_response = await agent.run(
        summary_prompt,
        execution=AgentExecutionConfig(
            max_retries_per_step=3,
            total_max_retries=10,
            max_iterations=20
        )
    ).observe(observer)

    summary = '\n'.join([m.text for m in summary_response.result.content])
    print("final summary after all agents = ",summary)

    # update_prompt = f"""
    # Based on the earlier decision: **{summary_response}** for work order **{wonum}**, follow these rules:

    # - If the decision is **schedule**, then:
    # - Set `sched_start` as today's UTC date and time.
    # - Set `sched_finish` as the date and time exactly **3 days after** `sched_start`.

    # - If the decision is **delay**, then:
    # - Determine the **next good date** (based on recent weather analysis or default to 5 days later) for `sched_start`.
    # - Set `sched_finish` as the date and time **3 days after** this `sched_start`.

    # Now use the tool `update_workorder_tool` to update the work order schedule in Maximo. Provide the input in this format:

    #     [wonum],[sched_start],[sched_finish]

    # Respond only with the result of the tool execution.
    # """

    update_prompt = f"""
    Based on the earlier decision (**{summary_response}**) for work order **{wonum}**, determine the updated scheduling dates:

    - If the decision is to **schedule**, set:
    - `Scheduled Start Date` as today's UTC date.
    - `Scheduled Finish Date` exactly 3 days after the start date.

    - If the decision is to **delay**, then:
    - Find the next good weather date (or default to 5 days later).
    - Set the `Scheduled Start Date` to that date.
    - Set the `Scheduled Finish Date` 3 days after that.

    After updating in Maximo, return the response in this full sentence format:
    "<tool execution result>.  \n
    Scheduled Start Date: <sched_start>  
    Scheduled Finish Date: <sched_finish>. "
    """


    update_response = await agent.run(
        update_prompt,
        execution=AgentExecutionConfig(
            max_retries_per_step=3,
            total_max_retries=10,
            max_iterations=5,
            # tools=update_workorder_tool
        )
    ).observe(observer)

    update_summary = '\n'.join([m.text for m in update_response.result.content])

    if weather_summary or location_summary or update_summary:
        final_summary = location_summary + weather_summary +  summary + update_summary
        print("final summary after all agents = ",final_summary)
    else:
        final_summary = "Agent execution did not return any output. Check input or agent responses."
    return final_summary
     
