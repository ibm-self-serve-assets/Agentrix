
import uuid
import time
from fastapi import FastAPI, Header, Depends
from fastapi.responses import StreamingResponse

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Optional, Dict, Any

import httpx
import asyncio

from dotenv import load_dotenv
import os
load_dotenv()


app = FastAPI()

class ModelName(str, Enum):
    mistral_large = "mistralai/mistral-large"
    llama_3_1_405b = "meta-llama/llama-3-405b-instruct"
    llama_3_1_70b = "meta-llama/llama-3-1-70b-instruct"
    gpt_4_o_mini = "gpt-4o-mini"

DEFAULT_MODEL = ModelName.mistral_large

class Message(BaseModel):
    role: str = Field(
        ...,
        description="The role of the message sender",
        pattern="^(user|assistant|system|tool)$",
    )
    content: str = Field(..., description="The content of the message")

class ExtraBody(BaseModel):
    thread_id: Optional[str] = Field(
        None, description="The thread ID for tracking the request"
    )

class MessageResponse(BaseModel):
    role: str = Field(
        ..., description="The role of the message sender", pattern="^(user|assistant)$"
    )
    content: str = Field(..., description="The content of the message")


class Choice(BaseModel):
    index: int = Field(..., description="The index of the choice")
    message: MessageResponse = Field(..., description="The message")
    finish_reason: Optional[str] = Field(
        None, description="The reason the message generation finished"
    )

class ChatCompletionRequest(BaseModel):
    model: str = Field(
        default_factory=lambda: DEFAULT_MODEL, description="ID of the model to use"
    )
    context: Dict[str, Any] = Field(
        {}, description="Contextual information for the request"
    )
    messages: List[Message] = Field(
        ..., description="List of messages in the conversation"
    )
    stream: Optional[bool] = Field(
        False, description="Whether to stream responses as server-sent events"
    )
    extra_body: Optional[ExtraBody] = Field(
        None, description="Additional data or parameters"
    )

class ChatCompletionResponse(BaseModel):
    id: str = Field(..., description="Unique identifier for the completion")
    object: str = Field(
        "chat.completion",
        description="The type of object returned, should be 'chat.completion'",
    )
    created: int = Field(
        ..., description="Timestamp of when the completion was created"
    )
    model: str = Field(..., description="The model used for generating the completion")
    choices: List[Choice] = Field(..., description="List of completion choices")


async def call_model_api(user_input):
    url = os.getenv("APP_URL","")
    print("url = ",url)
    # url = "https://maximo-supervisory-agent.1v42372h1yjp.us-east.codeengine.appdomain.cloud/runs"  

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_API_KEY"  # If needed
    }

    # payload = {
    #     "model": "string",
    #     "context": {},
    #     "messages": [
    #         {
    #             "role": "tool",
    #             "content": "string"
    #         }
    #     ],
    #     "stream": False,
    #     "extra_body": {
    #         "thread_id": "string"
    #     }
    # }

    payload = {
        "agent_name": "router",
        "input": [{"role": "user", "parts": [{"content": user_input}]}],
        "mode": "sync"
      }

    timeout = httpx.Timeout(120.0, connect=10.0)  # 120s total timeout

    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()



@app.post("/chat/completions")
async def chat_completions(
    request: ChatCompletionRequest,
    X_IBM_THREAD_ID: Optional[str] = Header(
        None,
        alias="X-IBM-THREAD-ID",
        description="Optional header to specify the thread ID",
    ),
    # current_user: Dict[str, Any] = Depends(get_current_user),
):
    thread_id = ""
    if X_IBM_THREAD_ID:
        thread_id = X_IBM_THREAD_ID
    if request.extra_body and request.extra_body.thread_id:
        thread_id = request.extra_body.thread_id
    if request.stream:
        # return StreamingResponse(
        #     generate_stream(request.messages[-1].content, thread_id, request.model),
        #     media_type="text/event-stream",
        # )
        return None
    else:
        id = str(uuid.uuid4())
        # marketing_response = await generate(request.messages[-1].content)
        # Run the async function
        marketing_response = await call_model_api(user_input=request.messages[-1].content)
        print("response from application = ",marketing_response)
        assistant_content = (
            marketing_response.get("output", [{}])[0]
            .get("parts", [{}])[0]
            .get("content", "")
        )
        return ChatCompletionResponse(
            id=id,
            object="chat.completion",
            created=int(time.time()),
            model=request.model,
            choices=[
                Choice(
                    index=0,
                    message=MessageResponse(
                        role="assistant", content=assistant_content
                    ),
                    finish_reason="stop",
                )
            ],
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)