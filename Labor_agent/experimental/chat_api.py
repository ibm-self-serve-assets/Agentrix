import uuid
import time
from fastapi import FastAPI, Header, Depends
from fastapi.responses import StreamingResponse, JSONResponse
from experimental.models import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    Choice,
    MessageResponse,
)
from typing import Optional, Dict, Any
from experimental.security import get_current_user
from servers.bee_mcp_github import get_agent_response

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

    prompt = request.messages[-1].content

    if request.stream:
        return StreamingResponse(
            content="data: [Agent Streaming not yet implemented]\n\n",
            media_type="text/event-stream",
        )
    else:
        agent_response = await get_agent_response(prompt)
        return JSONResponse(
            content=ChatCompletionResponse(
                id=str(uuid.uuid4()),
                object="chat.completion",
                created=int(time.time()),
                model=request.model,
                choices=[
                    Choice(
                        index=0,
                        message=MessageResponse(
                            role="assistant", content=agent_response.result.text
                        ),
                        finish_reason="stop",
                    )
                ],
            ).model_dump()
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)