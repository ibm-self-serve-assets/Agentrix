import os
from enum import Enum

class ModelEnum(str, Enum):
    # Models that are good at reasoning
    LLAMA_3_70_B_INSTRUCT = 'meta-llama/llama-3-3-70b-instruct'
    GRANITE_3_8_B_INSTRUCT = 'ibm/granite-3-8b-instruct'
    MISTRAL_LARGE = 'mistralai/mistral-large'
    LLAMA_3_90_B_VISION = 'meta-llama/llama-3-2-90b-vision-instruct'

class PromptEnum(str, Enum):
    AGENT_PLANNING_PROMPT = "config/planning_prompt.txt"

    


class AppConfig:
    FASTAPI_KEY = os.getenv("FASTAPI_KEY")
    WX_ENDPOINT = os.getenv("WX_ENDPOINT")
    IBM_CLOUD_API_KEY = os.getenv("IBM_CLOUD_API_KEY")
    WX_PROJECT_ID = os.getenv("WX_PROJECT_ID")
    MODEL = ModelEnum
    PROMPT = PromptEnum
    PARAMETERS = {
        "decoding_method": "greedy",
        "min_new_tokens": 1,
        "max_new_tokens": 3000,
        "repetition_penalty": 1
    }
    AGENT_VERBOSE = True # Set to True to see the agent's thought, action and observation process in the console
    