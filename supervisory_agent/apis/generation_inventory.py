import asyncio
from typing import AsyncGenerator
import uuid
import time
import logging
import json
import re
from dotenv import load_dotenv
from beeai_framework.agents.types import AgentExecutionConfig
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

    from src.agents.get_inventory_agent import get_beeai_framework_agent, observer
   

    # Extract number after "wonum"
    match = re.search(r'\b\d+\b', prompt)

    if match:
        wonum = match.group(0)
    else:
        wonum = None

    if not wonum:
        summary = "Missing wonum , Work order number is required."
        return summary
    

    agent = get_beeai_framework_agent()

    workorder_description_prompt = f"""
    Retrieve and summarize the following information for work order **{wonum}** from Maximo:
    - Work order number
    - Description

    Respond with a clear and complete sentence in this format:
    "Work order {wonum} has the description: <Description> and SiteID: <SiteId> ."
    """

    description_response = await agent.run(
        workorder_description_prompt,
        execution=AgentExecutionConfig(
            max_retries_per_step=3,
            total_max_retries=10,
            max_iterations=10,
            # tools=maximo_get_location
        )
    ).observe(observer)

    print("description response from maximo tool = ",description_response)
    description_summary = '\n'.join([m.text for m in description_response.result.content])


    # inventory_prompt = f"""
    # Provide a concise list of 4 to 5 specific materials for fixing the {coords['description']} issue. Ensure that these materials will guarantee a successful repair by the technician at the customer's location. The response should only include the material names in an array format, without any additional descriptions or details or spaces after comma.
    # """
    inventory_prompt = f"""
    Provide a concise list of 4 to 5 specific materials for fixing the {description_summary} issue without using any tool. Ensure that these materials will guarantee a successful repair by the technician at the customer's location. The response should only include the material names in an array format, without any additional descriptions or details or spaces after comma.
    """
    inventory_response = await agent.run(
                            inventory_prompt,
                            execution=AgentExecutionConfig(
                                max_retries_per_step=3,
                                total_max_retries=10,
                                max_iterations=20
                            )
                        ).observe(observer)
    
    print("inventory response = ",inventory_response)
    inventory_summary = ''.join([m.text for m in inventory_response.result.content])

    store_location_prompt = f"""
    You are given a list of item descriptions required to resolve a work order issue {inventory_summary}.
    Now Get item detail and store locations for these items.
    """

    store_location_response = await agent.run(
                            store_location_prompt,
                            execution=AgentExecutionConfig(
                                max_retries_per_step=3,
                                total_max_retries=10,
                                max_iterations=20
                            )
                        ).observe(observer)
    
    print("store location response = ",store_location_response)
    store_location_summary = ''.join([m.text for m in store_location_response.result.content])

    post_inventory_prompt = f"""
    You are given a list of item dictionaries: {store_location_summary}

    Each item has 'itemnum' and 'location'. Use this list **as-is** for the `items_with_locations` field.

    Get `wonum` and `siteid` from: {description_summary}.
    and update these details in maximo.
    """

    post_inventory_response = await agent.run(
                            post_inventory_prompt,
                            execution=AgentExecutionConfig(
                                max_retries_per_step=3,
                                total_max_retries=10,
                                max_iterations=20
                            )
                        ).observe(observer)
    
    print("post inventory response = ",post_inventory_response)
    post_inventory_summary = ''.join([m.text for m in post_inventory_response.result.content])
    
    summary = description_summary + inventory_summary + post_inventory_summary

    return summary
