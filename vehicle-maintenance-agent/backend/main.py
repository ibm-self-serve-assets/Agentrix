from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import requests
import json
from pydantic import BaseModel
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# Load from .env
INSTANCE_ID = os.getenv("INSTANCE_ID")
AGENT_ID = os.getenv("AGENT_ID")
IAM_API_KEY = os.getenv("IAM_API_KEY")

if not (INSTANCE_ID and AGENT_ID and IAM_API_KEY):
    print("⚠️ Missing environment variables. Check .env or Docker ENV setup.")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Accept from all, or restrict as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve React frontend build files
app.mount("/static", StaticFiles(directory="../frontend/build/static"), name="static")

@app.get("/")
def homepage():
    return FileResponse("../frontend/build/index.html")

@app.post("/get-saas-token")
def get_saas_token():
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {
        "accept": "application/json",
        "content-type": "application/x-www-form-urlencoded"
    }
    payload = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": IAM_API_KEY
    }

    try:
        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

class Message(BaseModel):
    role: str
    content: str

class PayloadModel(BaseModel):
    model: str
    messages: list[Message]
    stream: bool

@app.post("/get_wx_orch_chat")
def get_wx_orch_chat(payload: PayloadModel):
    response_token = get_saas_token()
    token = response_token['access_token']

    url = f"https://api.us-south.watson-orchestrate.cloud.ibm.com/instances/{INSTANCE_ID}/v1/orchestrate/{AGENT_ID}/chat/completions"
    headers = {
        "Authorization": f"Bearer {token}",
        "IAM-API_KEY": IAM_API_KEY,
        "Content-Type": "application/json",
        "Accept": "*"
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload.dict(),
            stream=True
        )

        def event_stream():
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode("utf-8").strip()
                    print("RAW STREAM:", decoded_line)
                    if decoded_line.startswith("data:"):
                        decoded_line = decoded_line[len("data:"):].strip()

                    try:
                        data = json.loads(decoded_line)
                        yield f"data: {json.dumps(data)}\n\n"
                    except json.JSONDecodeError:
                        continue
            yield "data: [DONE]\n\n"

        return StreamingResponse(event_stream(), media_type="text/event-stream")

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
