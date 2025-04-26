import asyncio
from typing import AsyncGenerator
import uuid
import time
import logging
import json
from dotenv import load_dotenv
import requests
import os

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
    # NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account (https://dataplatform.cloud.ibm.com/docs/content/wsj/analyze-data/ml-authentication.html?context=wx)
    API_KEY = os.getenv("WATSONX_API_KEY")
    token_response = requests.post(
        "https://iam.cloud.ibm.com/identity/token",
        data={
            "apikey": API_KEY,
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        },
    )
    mltoken = token_response.json()["access_token"]

    # NOTE:  manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"history": input_text}

    deployment_id = os.getenv("WATSONX_DEPLOYMENT_ID")
    response_scoring = requests.post(
        f"https://us-south.ml.cloud.ibm.com/ml/v4/deployments/{deployment_id}/ai_service?version=2021-05-01",
        json=payload_scoring,
        headers={"Authorization": "Bearer " + mltoken},
    )
    return response_scoring.json()["result"][0]