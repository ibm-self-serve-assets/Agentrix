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
    from src.agents.get_agent import get_beeai_framework_agent, observer

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
            max_retries_per_step=3,
            total_max_retries=10,
            max_iterations=20,
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
            max_retries_per_step=3,
            total_max_retries=10,
            max_iterations=20,
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
            max_retries_per_step=3, 
            total_max_retries=10, 
            max_iterations=20
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
            max_retries_per_step=3, 
            total_max_retries=10, 
            max_iterations=20
        )
    ).observe(observer)

    print("selected labor for selected craft= ",labor_response)
    labor_summary = '\n'.join([m.text for m in labor_response.result.content])

    add_labor_prompt = f"""You have a valid labor code and the details of a work order {description_summary}. Your task is to assign this labor {labor_summary} to the given work order in Maximo.

    Use the work order number, site ID, and labor code to perform the assignment. Confirm the assignment has been made successfully."""

    add_labor_response = await agent.run(
        add_labor_prompt,
        execution=AgentExecutionConfig(
            max_retries_per_step=3, 
            total_max_retries=10, 
            max_iterations=20
        )
    ).observe(observer)

    print("add labor= ",add_labor_response)
    add_labor_summary = '\n'.join([m.text for m in add_labor_response.result.content])

    # # Step 5: Get and assign labor
    # labor_data = agent_maximo.get_labor(selected_craft)
    # if not labor_data or "laborcode" not in labor_data:
    #     assignment_status = False
    #     labor_code = "N/A"
    # else:
    #     labor_code = labor_data["laborcode"]
    #     assignment_status = agent_maximo.addLabor(labor_code, wonum, siteid="BEDFORD")

    # Step 6: Ask LLM to summarize dynamically using full context
#     summary_prompt = f"""
# You are a field automation assistant helping with Maximo work order assignments.

# Here is the user's original request:
# \"\"\"{input_text}\"\"\"

# Below are the extracted and processed details:
# - Work Order Number: {wonum}
# - Issue Description: {description}
# - Assigned Craft: {selected_craft}
# - Assigned Labor: {labor_code}
# - Assignment Status: {"Successful" if assignment_status else "Failed"}

# Using the original request and these details, generate a clear, helpful response.

# 👉 Respond in a professional tone suitable for a technician or supervisor.
# 👉 If assignment is successful, confirm the update and next steps.
# 👉 If assignment failed, explain clearly and suggest retry or escalation.
# Do not include extra explanations or system logs—just the final message.
# """

    summary = description_summary + craft_list_summary + craft_summary + labor_summary + add_labor_summary

    summary_prompt = f""" You are a helpful assistant to add labor based on crafts. The variable  {summary} contains the raw decision output (e.g., description, crafts, and labor scheduling info).

        Respond to the user's **{input_text}** naturally and conversationally:

        Use `summary` to guide your answer but **don’t repeat it verbatim** — rephrase it based on input text.
        """

    summary_response = await agent.run(
    summary_prompt,
    execution=AgentExecutionConfig(
        max_retries_per_step=3,
        total_max_retries=10,
        max_iterations=5,
        # tools=update_workorder_tool
        )
    ).observe(observer)

    final_summary = '\n'.join([m.text for m in summary_response.result.content])

    print("final summary after all agents = ",final_summary)

    # summary_response = await agent.run(
    #     summary_prompt,
    #     execution=AgentExecutionConfig(max_retries_per_step=2, total_max_retries=5, max_iterations=10)
    # ).observe(observer)

    # return ''.join([m.text for m in summary_response.result.content])

    return final_summary
