from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_ibm import ChatWatsonx
from langgraph.graph import MessagesState, StateGraph, START, END
from langgraph.prebuilt import create_react_agent
from langgraph.types import Command
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.runnables.config import RunnableConfig
from ibm_watsonx_ai.foundation_models import ModelInference
from fastapi.middleware.cors import CORSMiddleware
from langgraph.errors import GraphRecursionError
import operator
import os
from typing import Literal
from typing import Annotated
from typing_extensions import TypedDict
import requests
import json
from urllib.parse import quote
from dotenv import load_dotenv
load_dotenv()
import re
import ast

app = FastAPI()
app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"], 
)


# Set credentials
credentials= {
    "url": os.getenv("WX_URL",None),
    "apikey": os.getenv("WX_APIKEY", None)
}
project_id= os.getenv("PROJECT_ID",None)



# Utilities

def extract_list(input_str):
    input_str = re.sub(r'```(?:python)?', '', input_str).strip()

    match = re.search(r'\[.*?\]', input_str)
    if match:
        return ast.literal_eval(match.group(0))
    return []


def get_access_token(apikey):
	
    iam_url = 'https://iam.cloud.ibm.com/identity/token'

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {
        'grant_type': 'urn:ibm:params:oauth:grant-type:apikey',
        'apikey': apikey
    }

    response = requests.post(iam_url, headers=headers, data=data)

    if response.status_code == 200:
        access_token = response.json().get('access_token')
        # print(f"Access Token: {access_token}")
    else:
        print(f"Failed to get access token: {response.status_code}")
        # print(response.text)
	
    return access_token


def call_llm(catalog:list, user_details:dict, recc_type:str):

    access_token = get_access_token(apikey=credentials["apikey"])

    url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"

    prompt_input= ""
    max_tokens = 100

    if recc_type == "style":
        max_tokens = 100
        prompt_input= f"""You are a personal fashion assistant. Given catalog data and query as input, recommend a list of apparel item IDs from ONLY the catalog that are suitable for the given event. Your response should be a list of IDs of the apparel from the catalog only and should not be present in wardrobe.

Do not add any information other than what is provided to you. Do not provide justification or advices.

Tasks:
- Based on the catalog, only suggest apparel items from the catalog appropriate for a {user_details["event_type"]} event in {user_details["event_location"]} on {user_details["event_date"]}.
- Return the IDs of the suggested items from the catalog that fit the criteria (suitable for Event)

Constraints:
- Only include items from the provided catalog.
- Suggestions should only be apparel items not in my wardrobe

Catalog data:
{catalog}

query:
- User Profile: I am a {user_details["gender"]}.
- Wardrobe Items I Own: {user_details["wardrobe_items_ids"]} (IDs from the catalog)
- Event: {user_details["event_type"]}
- Location: {user_details["event_location"]}
- Date: {user_details["event_date"]}

output:
"""

    else:
        max_tokens = 300
        prompt_input= f"""You are a helpful travel assistant. Given the following details, provide concise information about the local tourist attractions and places to visit for the given location:

query:
- User Profile: I am a {user_details["gender"]}.
- Event: {user_details["event_type"]}
- Location: {user_details["event_location"]}
- Date: {user_details["event_date"]}

output:
"""
        


    body = {
        "input": prompt_input,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": max_tokens,
            "min_new_tokens": 0,
            "repetition_penalty": 1
        },
        "model_id": "mistralai/mistral-large",
        "project_id": project_id,
        "moderations": {
            "hap": {
                "input": {
                    "enabled": True,
                    "threshold": 0.5,
                    "mask": {
                        "remove_entity_value": True
                    }
                },
                "output": {
                    "enabled": True,
                    "threshold": 0.5,
                    "mask": {
                        "remove_entity_value": True
                    }
                }
            },
            "pii": {
                "input": {
                    "enabled": True,
                    "threshold": 0.5,
                    "mask": {
                        "remove_entity_value": True
                    }
                },
                "output": {
                    "enabled": True,
                    "threshold": 0.5,
                    "mask": {
                        "remove_entity_value": True
                    }
                }
            }
        }
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    
    response = requests.post(
        url,
        headers=headers,
        json=body
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()
    data = data["results"][0]["generated_text"]

    return(data)


def output_consolidator(tool_logs, query, wardrobe_ids, gender):
    model_id = "mistralai/mistral-large"
    parameters = {
    "decoding_method": "greedy",
    "max_new_tokens": 2000,
    "min_new_tokens": 0,
    "repetition_penalty": 1
    }

    model = ModelInference(
        model_id = model_id,
        params = parameters,
        credentials = credentials,
        project_id = project_id,
        )
    
    formattedprompt=''
    
    with open('./imgmap.json') as file:
        json_data = json.load(file)

    catalog_data = [
        item for item in json_data 
        if item['gender'].lower() == gender.lower()
    ]

    prompt_input = """You are a response auditor and corrector. Given catalogue data, tool logs and query as input, analyse the tool logs as per the Guidelines and catalogue data provided and return your response as a json string format with the following fields:
    'images': list of only the IDs taken from styling recommendations
    
    Do not add any information other than what is provided to you.
    
    Guidelines:
    - The final output should be in json format
    - The "styling_recc" should not contains any IDs. Extract the IDs as a list and add to the "images" field
    - All recommended items should be from the catalogue data only

    catalogue data:
    {catalog_data}


    tool logs:
    {tool_logs}

    query:
    {query}

    output:
    """

    formattedprompt = prompt_input.format(catalog_data=catalog_data, tool_logs=tool_logs, query=query)

    generated_response = model.generate_text(prompt=formattedprompt, guardrails=False)
    return generated_response



# Phase 1 tools - style_recommender_tool, travel_recommender_tool
@tool
def style_recommender_tool(
    wardrobe_items_ids: str, gender: str, event_date: str, event_location: str, event_type: str) -> list:
    """Use this function to provide event, gender, wardrobe_items_ids, event location and event date to get recommended style"""
    wardrobe_items_ids = json.loads(wardrobe_items_ids)
    with open('./imgmap.json') as file:
        json_data = json.load(file)
    
    filtered_data = [
        item for item in json_data 
        if item['id'] not in wardrobe_items_ids and item['gender'].lower() == gender.lower()
    ]

    user_details = {"event_type": event_type, "event_location": event_location, "event_date":event_date, "gender": gender, "wardrobe_items_ids": wardrobe_items_ids}


    # print('style recommender called')
    response = call_llm(filtered_data, user_details, "style")

    return response

@tool
def travel_recommender_tool( gender: str, event_date: str, event_location: str, event_type: str) -> list:
    """Use this function to provide event, gender, event location and event date to get travel recommendation"""

    user_details = {"event_type": event_type, "event_location": event_location, "event_date":event_date, "gender": gender}

    # print('travel recommender called')
    response = call_llm([], user_details, "travel")

    return response



# Phase 2 tools- catalogue_data_retriever, complete_catalogue_data_retriever
@tool
def catalogue_data_retriever(
    wardrobe_ids: str, gender: str) -> list:
    """Use this function to get catalogue of apparel products data excluding the wardrobe_ids and getting relevant catalogue data"""
    wardrobe_ids = json.loads(wardrobe_ids)
    with open('./imgmap.json') as file:
        json_data = json.load(file)
    
    filtered_data = [
        item for item in json_data 
        if item['id'] not in wardrobe_ids and item['gender'].lower() == gender.lower()
    ]    
    return filtered_data
    

@tool
def complete_catalogue_data_retriever(gender: str) -> list:
    """Use this function to get complete catalogue data of apparel items relevant to given gender"""
    # wardrobe_ids = json.loads(wardrobe_ids)
    with open('./imgmap.json') as file:
        json_data = json.load(file)
    
    filtered_data = [
        item for item in json_data 
        if item['gender'].lower() == gender.lower()
    ]    
    return filtered_data



llm = ChatWatsonx(
    model_id="meta-llama/llama-3-3-70b-instruct",
    url=credentials.get("url"),
    apikey=credentials.get("apikey"),
    project_id=project_id,
    params={
           "frequency_penalty": 0,
            "max_tokens": 200,
            "presence_penalty": 0,
            "temperature": 0.1,
            "top_p": 1
    },
)


class State(TypedDict):
    query: str
    final_output: str
    recc: Annotated[list, operator.add] = []

web_search_agent = create_react_agent(
    llm, tools=[travel_recommender_tool], prompt="Get travel recommendation with the given user details"
)

def search_node(state):
    result = web_search_agent.invoke(state['query'])
    return {"recc": [result]} 

data_agent = create_react_agent(llm, tools=[style_recommender_tool], prompt="""Provide styling recommendation. Respond in the format {"image_ids": [list of suitable item IDs from catalog]}""")

def dataretriever_node(state):
    result = data_agent.invoke(state['query'])
    return {"recc": [result]}


builder = StateGraph(State)
builder.add_node("travel_recommender", search_node)
builder.add_node("style_recommender", dataretriever_node)

builder.add_edge(START, "travel_recommender")
builder.add_edge(START, "style_recommender")
builder.add_edge("travel_recommender", END)
builder.add_edge("style_recommender", END)
graph = builder.compile()


# llm_mb = ChatWatsonx(
#     model_id="ibm/granite-3-8b-instruct",
#     url=credentials.get("url"),
#     apikey=credentials.get("apikey"),
#     project_id=project_id,
#     params={
#            "frequency_penalty": 0,
#             "max_tokens": 300,
#             "presence_penalty": 0,
#             "temperature": 0.1,
#             "top_p": 1
#     },
# )



wardrobe_gap_analyser = create_react_agent(
    llm, tools=[catalogue_data_retriever], prompt="Given wardrobe items that user already has, provide the wardrobe gap analysis as per the catalogue data"
)

def wardrobe_gap_analyser_node(state):
    result = wardrobe_gap_analyser.invoke(state['query'])
    return {"recc": [result]} 

style_recommender_agent = create_react_agent(llm, tools=[complete_catalogue_data_retriever], prompt="""You are a personal fashion assistant tasked with suggesting complimentary apparel items to the user selections based on provided gender""")

def style_recommender_node(state):
    result = style_recommender_agent.invoke(state['query'])
    return {"recc": [result]}



# builder_mb = StateGraph(State)
# builder_mb.add_node("wardrobe_gap_analyser", wardrobe_gap_analyser_node)
# builder_mb.add_node("mb_style_recommender", style_recommender_node)

# builder_mb.add_edge(START, "wardrobe_gap_analyser")
# builder_mb.add_edge(START, "mb_style_recommender")
# builder_mb.add_edge("wardrobe_gap_analyser", END)
# builder_mb.add_edge("mb_style_recommender", END)
# graph_mb = builder_mb.compile()



#---------------------------------------------------------------------

class UserQuery(BaseModel):
    query: dict

#Phase 1 API
@app.post("/getrecommendations")
async def get_recommendations(user_input: UserQuery):

    user_id= user_input.query["user_id"]
    evt_id= user_input.query["event_id"]
    evt_name = user_input.query["event_name"]
    evt_loc = user_input.query["event_location"]
    evt_date = user_input.query["event_date"]
    gender = user_input.query["gender"]
    wardrobe_ids = user_input.query["wardrobe_items"]

    prompt_p1=f"""- User Profile: I am a {gender}.
- Wardrobe Items I Own: {wardrobe_ids} (IDs from the catalog)
- Event: {evt_name}
- Location: {evt_loc}
- Date: {evt_date}"""


    config = RunnableConfig(recursion_limit=22)
    
    try:
        resp = []
        for s in graph.stream({"query": {"messages": prompt_p1}}, config):
            resp.append(s)

        formatted_travel_recc = resp[1]['travel_recommender']['recc'][0]['messages'][2].content
        formatted_style_recc = extract_list(resp[0]['style_recommender']['recc'][0]['messages'][2].content)

        # travel_recc = json.loads(str(resp[1]['travel_recommender']['recc'][0]['messages'][2].content))
        # formatted_travel_recc = next(iter(travel_recc.values()))

        # style_recc = json.loads(str(resp[0]['style_recommender']['recc'][0]['messages'][2].content))
        # formatted_style_recc = next(iter(style_recc.values()))


        formatted_output = {'travel_recc': formatted_travel_recc, 'image_ids': formatted_style_recc, "user_id": user_id, "event_id": evt_id}

        return {"response": formatted_output}

    except GraphRecursionError:
        print("Recursion limit reached")
        return {"response": "Server Error"}


#Phase 2 API
# @app.post("/getmbrecommendations")
# async def get_mb_recommendations(user_input: UserQuery):

#     user_id= user_input.query["user_id"]
#     evt_id= user_input.query["event_id"]
#     evt_name = user_input.query["event_name"]
#     evt_loc = user_input.query["event_location"]
#     evt_date = user_input.query["event_date"]
#     gender = user_input.query["gender"]
#     wardrobe_ids = user_input.query["wardrobe_items"]
#     mb_ids = user_input.query["moodboard_items"]


#     prompt_p2 =f"""
# - User Profile: I am a {gender}.
# - Wardrobe Items I Own: {wardrobe_ids} (IDs from the catalog).
# - Items I Like and Selected: {mb_ids} (IDs from the catalog).

# Task:
# - Perform a wardrobe gap analysis: Identify which styling items from the catalog I do not currently own.
# - Based on the catalog, only suggest apparel items I do not own that complement the items I selected ({mb_ids}).
# - The suggested items must be appropriate for a {evt_name} event in {evt_loc} on {evt_date}.
# - Return the IDs and descriptions of the suggested items from the catalog that fit the criteria.

# Constraints:
# - Only include items from the provided catalog.
# - Suggestions should only be apparel items not already in my wardrobe or the ones I selected.
# """

#     config_mb = RunnableConfig(recursion_limit=50)
#     valid_json={}
#     agent_response_mb = []
#     for smb in graph.stream({"query": {"messages": prompt_p2}}, config_mb):
#         agent_response_mb.append(smb)
    
#     final_response = output_consolidator(agent_response_mb, prompt_p2, wardrobe_ids, gender)
#     final_response_processed = final_response.strip().replace("```json", "").replace("```", "").strip()

#     try:
#         valid_json = json.loads(final_response_processed)
#         valid_json.update({"user_id": user_id, "event_id": evt_id})

#     except json.JSONDecodeError as e:
#         print(f"Error parsing JSON: {e}")

#     return {"response": valid_json}
