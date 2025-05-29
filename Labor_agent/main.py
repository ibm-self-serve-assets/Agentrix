import uuid
import time
from fastapi import FastAPI, Header, Depends
from fastapi.responses import StreamingResponse
from apis.models import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    Choice,
    MessageResponse,
)
from apis.generation import generate, generate_stream
from typing import Optional, Dict, Any
from apis.security import get_current_user

app = FastAPI()

@app.post("/chat/completions")
async def chat_completions(
    request: ChatCompletionRequest,
    X_IBM_THREAD_ID: Optional[str] = Header(
        None,
        alias="X-IBM-THREAD-ID",
        description="Optional header to specify the thread ID",
    ),
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    thread_id = ""
    if X_IBM_THREAD_ID:
        thread_id = X_IBM_THREAD_ID
    if request.extra_body and request.extra_body.thread_id:
        thread_id = request.extra_body.thread_id
    if request.stream:
        return StreamingResponse(
            generate_stream(request.messages[-1].content, thread_id, request.model),
            media_type="text/event-stream",
        )
    else:
        id = str(uuid.uuid4())
        marketing_response = await generate(request.messages[-1].content)
        return ChatCompletionResponse(
            id=id,
            object="chat.completion",
            created=int(time.time()),
            model=request.model,
            choices=[
                Choice(
                    index=0,
                    message=MessageResponse(
                        role="assistant", content=marketing_response
                    ),
                    finish_reason="stop",
                )
            ],
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)