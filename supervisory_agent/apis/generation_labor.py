import asyncio
from typing import AsyncGenerator
import uuid
import time
import logging
import json
import re
import ast
from dotenv import load_dotenv
from beeai_framework.agents.types import AgentExecutionConfig
from beeai_framework.backend.message import Message, SystemMessage

load_dotenv()

# Configure logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def format_resp(struct: dict) -> str:
    return "data: " + json.dumps(struct) + "\n\n"

async def generate_stream(query, thread_id, model) -> AsyncGenerator[str, None]:
    gen_task = asyncio.create_task(generate(query))
    while not gen_task.done():
        event = {
            "id": str(uuid.uuid4()),
            "object": "thread.run.step.delta",
            "created": int(time.time()),
            "thread_id": thread_id,
            "model": model,
            "choices": [{"delta": {"content": "", "role": "system"}}],
        }
        yield format_resp(event)
        await asyncio.sleep(1)

    result = await gen_task
    final_event = {
        "id": str(uuid.uuid4()),
        "object": "thread.message.delta",
        "created": int(time.time()),
        "thread_id": thread_id,
        "model": model,
        "choices": [{"delta": {"content": result, "role": "assistant"}}],
    }
    yield format_resp(final_event)

async def generate(input_text: str) -> str:
    from src.agents.get_labor_agent import get_beeai_framework_agent, observer

    # Extract number after "wonum"
    match = re.search(r'\b\d+\b', input_text)

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
    - SiteId

    Respond with a clear and complete sentence in this format:
    "Work order {wonum} has the description: <Description> and SiteID: <SiteId> ."
    """

    description_response = await agent.run(
        workorder_description_prompt,
        execution=AgentExecutionConfig(
           max_retries_per_step=1,
            total_max_retries=1,
            max_iterations=2,
            # tools=maximo_get_location
        )
    ).observe(observer)

    print("description response from maximo tool = ",description_response)
    description_summary = '\n'.join([m.text for m in description_response.result.content])

    craft_list_prompt = """
    Retrieve the list of available crafts from Maximo. 
    For each craft, include:
    - Craft code
    - Craft description

    Respond as a list in the following format:
    - <craft_code>: <description>
    """

    craft_list_response = await agent.run(
        craft_list_prompt,
        execution=AgentExecutionConfig(
            max_retries_per_step=1,
            total_max_retries=1,
            max_iterations=2,
            # tools=maximo_get_location
        )
    ).observe(observer)

    print("craft list from maximo tool = ",craft_list_response)
    craft_list_summary = '\n'.join([m.text for m in craft_list_response.result.content])


    # Step 3: Get available crafts
    # craft_data = agent_maximo.getCraftDetails()
    # logger.debug("Craft details: %s", craft_data)

    # Step 4: Ask LLM to select best craft
    craft_prompt = f"""
    Given the craft data {craft_list_summary}, select only one best-suited craft for resolving this issue: "{description_summary}".
    Return the response strictly in format:Selected craft: <craft_code> — <reason for selection>
    """

    craft_response = await agent.run(
        craft_prompt,
        execution=AgentExecutionConfig(
            max_retries_per_step=1,
            total_max_retries=1,
            max_iterations=2,
        )
    ).observe(observer)

    print("selected craft for description = ",craft_response)
    craft_summary = '\n'.join([m.text for m in craft_response.result.content])

    # try:
    #     craft_string = ''.join([m.text for m in craft_response.result.content])
    #     selected_craft = ast.literal_eval(craft_string)[0]
    # except Exception:
    #     return "⚠️ Failed to parse selected craft. Please refine your craft selection logic."

    # logger.info(f"Selected craft: {selected_craft}")

    labor_prompt = f""" You have a selected craft obtained from Maximo {craft_summary}. Your task is to find a labor resource that is associated with this craft in Maximo. Use the selected craft to query available labor records and extract the most relevant labor code.

    Return only the labor code of the first or best-matching labor associated with the selected craft.
    """

    labor_response = await agent.run(
        labor_prompt,
        execution=AgentExecutionConfig(
            max_retries_per_step=1,
            total_max_retries=1,
            max_iterations=2,
        )
    ).observe(observer)

    print("selected labor for selected craft= ",labor_response)
    labor_summary = '\n'.join([m.text for m in labor_response.result.content])
    # labor_assigned = False
    # if labor_assigned == "False":
    labor_summary = '\n'.join([m.text for m in labor_response.result.content])

    add_labor_prompt = f""" You have a valid labor code and the details of a work order {description_summary}. Your task is to assign this labor {labor_summary} to the given work order in Maximo.
    Use the work order number, site ID, and labor code to perform the assignment
    Note : Just do one iteration for assignment and if it is unsuccessful then just give summary of error."""

    add_labor_response = await agent.run(
        add_labor_prompt,
        execution=AgentExecutionConfig(
            max_retries_per_step=1,
            total_max_retries=1,
            max_iterations=2,
        )
    ).observe(observer)

    # labor_assigned = True

    print("add labor= ",add_labor_response)
    add_labor_summary = '\n'.join([m.text for m in add_labor_response.result.content])
    # else:
    #     add_labor_summary = "Labor is already assigned."


    # labor_assigned = True  # Set the flag so it doesn't run again

    # add_labor_prompt = f"""You have a valid labor code and the details of a work order {description_summary}. Your task is to assign this labor {labor_summary} to the given work order in Maximo.

    # Use the work order number, site ID, and labor code to perform the assignment.just do one iteration for assignment and if it is unsuccessful then just give summury of error."""

    # add_labor_response = await agent.run(
    #     add_labor_prompt,
    #     execution=AgentExecutionConfig(
    #        max_retries_per_step=1,
    #         total_max_retries=1,
    #         max_iterations=2,
    #     )
    # ).observe(observer)

    


    summary = description_summary + craft_list_summary + craft_summary + labor_summary + add_labor_summary
    
    summary_prompt = f"""
    You are a helpful assistant summarizing the result of a Maximo work order decision.

    The following is the system-generated summary of description, craft planning, and labor scheduling:
    **{summary}**

    If there were any errors encountered during labor assignment, they are included in the summary above — ensure they are conveyed clearly and naturally in your response.

    Respond to the user's original query:
    **{input_text}**

    Instructions:
    - Use the above summary to guide your response, but **do not repeat it verbatim** — rephrase it naturally.
    - Mention any labor assignment errors **gracefully**, without sounding overly technical.
    - Keep the tone clear, helpful, and conversational.
    """


    summary_response = await agent.run(
    summary_prompt,
    execution=AgentExecutionConfig(
        max_retries_per_step=1,
        total_max_retries=1,
        max_iterations=2,
        # tools=update_workorder_tool
        )
    ).observe(observer)

    final_summary = '\n'.join([m.text for m in summary_response.result.content])

    print("final summary after all agents = ",final_summary)


    return summary
