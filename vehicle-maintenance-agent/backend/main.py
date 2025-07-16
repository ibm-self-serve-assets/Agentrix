from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import json
from pydantic import BaseModel
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi import status
from fastapi import Request
import os
from dotenv import load_dotenv
from typing import Dict, Any, Optional
load_dotenv()

app = FastAPI()

# Replace with your actual values
INSTANCE_ID = os.getenv("INSTANCE_ID")
AGENT_ID = os.getenv("AGENT_ID")
IAM_API_KEY = os.getenv("IAM_API_KEY")
WXO_INSTANCE_URL=os.getenv("WXO_INSTANCE_URL")

# Allow frontend on localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = IAM_API_KEY

@app.post("/get-saas-token")
def get_saas_token():
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {
        "accept": "application/json",
        "content-type": "application/x-www-form-urlencoded"
    }
    payload = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": API_KEY
    }

    try:
        response = requests.post(url, data=payload, headers=headers)  # ✅ use data=
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    
# Define the expected structure of the payload
class Message(BaseModel):
    role: str
    content: str

class PayloadModel(BaseModel):
    model: str
    messages: list[Message]
    stream: bool

class PayloadModelNew(BaseModel):
  message: Dict[str, Any]
  additional_properties: Dict[str, Any] = {}
  context: Dict[str, Any] = {}

@app.post("/get_wx_orch_chat")
# approach1 when we stream=false and want to render json
def get_wx_orch_chat(payload: PayloadModel, request: Request):
    response_token = get_saas_token()
    token = response_token['access_token']
    thread_id = request.headers.get("x-ibm-thread-id")
    print('response_token', response_token)

    url = f"{WXO_INSTANCE_URL}/instances/{INSTANCE_ID}/v1/orchestrate/{AGENT_ID}/chat/completions"

    headers = {
        "Authorization": f"Bearer {token}",
        "IAM-API_KEY": IAM_API_KEY,
        "Content-Type": "application/json",
        "X-IBM-THREAD-ID": thread_id,
        "Accept": "application/json",  # Requesting full JSON response
    }

    print('payload', payload)

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload.dict(),
            timeout=30  # Optional: Add timeout
        )

        if response.status_code != 200:
            print("Watsonx responded with error.")
            return JSONResponse(
                status_code=response.status_code,
                content={
                    "message": "Watsonx returned error",
                    "status": response.status_code,
                    "error": response.text
                }
            )

        try:
            result = response.json()
        except json.JSONDecodeError:
            print("Invalid JSON returned.")
            return JSONResponse(
                status_code=500,
                content={"message": "Invalid JSON response from Watsonx"}
            )

        return JSONResponse(
            status_code=200,
            content=result
        )

    except requests.exceptions.RequestException as e:
        print("RequestException:", str(e))
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Failed to connect to orchestration service", "type": "error"}
        )

    except Exception as e:
        print("Unhandled exception:", str(e))
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Internal server error", "type": "error"}
        )

@app.post("/get_wx_orch_chat_stream")
# approach 2 when we nee to stream the response
def get_wx_orch_chat_stream(payload: PayloadModel, request: Request):

    response_token = get_saas_token()  # Make sure getToken() returns a dict, not a coroutine

    token = response_token['access_token']  # Use dictionary access, not dot
    thread_id = request.headers.get("x-ibm-thread-id")
    

    url = f"{WXO_INSTANCE_URL}/instances/{INSTANCE_ID}/v1/orchestrate/{AGENT_ID}/chat/completions"

    headers = {
        "Authorization": f"Bearer {token}",
        "IAM-API_KEY": IAM_API_KEY,
        "Content-Type": "application/json",
        "X-IBM-THREAD-ID": thread_id,
        "Accept": "*",
    }

    print('payload', payload)
        # Send streaming request to watsonx or other model endpoint
    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload.dict(),
            stream=True  # Stream from upstream
        )


        # Define event stream generator
        def event_stream():
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode("utf-8").strip()
                    if not decoded_line:
                        continue

                    if decoded_line.startswith("data:"):
                        decoded_line = decoded_line[len("data:"):].strip()

                    try:
                        data = json.loads(decoded_line)
                        yield f"data: {json.dumps(data)}\n\n"
                    except json.JSONDecodeError:
                        print("Stream parse error (skipped line):", decoded_line)
                        continue
            yield "data: [DONE]\n\n"


        if response.status_code != 200 or 'text/event-stream' not in response.headers.get("Content-Type", ""):
            print("Watsonx responded with error or non-streaming content.")
            return JSONResponse(
                status_code=response.status_code,
                content={"message": "Failed to connect or invalid response from Watsonx", "type": "error", "status": response.status_code}
            )

        # 🟢 This should be outside the generator
        return StreamingResponse(event_stream(), media_type="text/event-stream")
    

    except requests.exceptions.RequestException as e:
        print("RequestException:", str(e))
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Failed to connect to orchestration service", "type": "error"}
        )

    except Exception as e:
        print("Unhandled exception:", str(e))
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Internal server error", "type": "error"}
        )

@app.get("/get_thread_messages/{thread_id}")
def get_thread_messages(thread_id: str, request: Request):

    response_token = get_saas_token()
    token = response_token['access_token']

    url = f"{WXO_INSTANCE_URL}/instances/{INSTANCE_ID}/v1/orchestrate/threads/{thread_id}/messages"

    headers = {
        "Authorization": f"Bearer {token}",
        "IAM-API_KEY": IAM_API_KEY,
        "Content-Type": "application/json",
        "Accept": "*/*",  # Fix accept value
    }

    try:
        response = requests.get(
            url,
            headers=headers
        )
        return response.json()

    except requests.exceptions.RequestException as e:
        print("RequestException:", str(e))
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Failed to connect to orchestration service", "type": "error"}
        )
    
@app.post("/get_wx_orch_stream")
def get_wx_orch_stream(payload: PayloadModelNew, request: Request):

    thread_id = request.headers.get("x-ibm-thread-id")

       # Build the payload to forward or process
    request_payload = {
        "message": payload.message,
        "additional_properties": payload.additional_properties,
        "context": payload.context,
        "agent_id": AGENT_ID,
    }

    # Only add thread_id if it's not empty
    if thread_id:
        request_payload["thread_id"] = thread_id
    print('payload in stream latest', payload)

    response_token = get_saas_token()  # Make sure getToken() returns a dict, not a coroutine

    token = response_token['access_token']  # Use dictionary access, not dot
   
    stream= True
    stream_timeout=120000
    multiple_content= True
    url = f"{WXO_INSTANCE_URL}/instances/{INSTANCE_ID}/v1/orchestrate/runs?stream={stream}&stream_timeout={stream_timeout}&multiple_content={multiple_content}"

    print('url', url)
    headers = {
        "Authorization": f"Bearer {token}",
        "IAM-API_KEY": IAM_API_KEY,
        "Content-Type": "application/json",
        "Accept": "*",  "accept-language": "en-GB,en-US;q=0.9,en;q=0.8" ,
        'access-control-allow-origin': '*' ,
                }

    print('payload', payload)
        # Send streaming request to watsonx or other model endpoint
    try:
        response = requests.post(
            url,
            headers=headers,
            json=request_payload,
            stream=True  # Stream from upstream
        )


        # Define event stream generator
        def event_stream():
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode("utf-8").strip()
                    if not decoded_line:
                        continue

                    if decoded_line.startswith("data:"):
                        decoded_line = decoded_line[len("data:"):].strip()

                    try:
                        data = json.loads(decoded_line)
                        yield f"data: {json.dumps(data)}\n\n"
                    except json.JSONDecodeError:
                        print("Stream parse error (skipped line):", decoded_line)
                        continue
            yield "data: [DONE]\n\n"


        if response.status_code != 200 or 'text/event-stream' not in response.headers.get("Content-Type", ""):
            print("Watsonx responded with error or non-streaming content.")
            return JSONResponse(
                status_code=response.status_code,
                content={"message": "Failed to connect or invalid response from Watsonx", "type": "error", "status": response.status_code}
            )

        # 🟢 This should be outside the generator
        return StreamingResponse(event_stream(), media_type="text/event-stream")
    

    except requests.exceptions.RequestException as e:
        print("RequestException:", str(e))
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Failed to connect to orchestration service", "type": "error"}
        )

    except Exception as e:
        print("Unhandled exception:", str(e))
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Internal server error", "type": "error"}
        )


@app.post("/chat")
async def chat(payload: PayloadModelNew):
    return {"status": "received", "agent_id": payload.agent_id}