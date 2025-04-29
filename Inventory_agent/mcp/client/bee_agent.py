import asyncio
import json
import sys
import traceback

from beeai_framework.agents.experimental.remote import RemoteAgent
from beeai_framework.errors import FrameworkError


async def main() -> None:
    prompt = "How is the weather in Bengaluru?"

    remote_mcp_server = "https://manojs-mcp-server.1u9sfcpo6wod.us-east.codeengine.appdomain.cloud/sse"
    local_mcp_server = "http://127.0.0.1:8000/sse"
    
    agent = RemoteAgent(agent_name="chat", url=remote_mcp_server)
    
        # Run the agent and observe events
    response = (
        await agent.run(
            {
                "messages": [{"role": "user", "content": prompt}],
                "config": {"tools": ["weather_tool", "search_tool"]},
            }
        )
        .on(
            "update",
            lambda data, event: (
                print("Agent 🤖 (debug) : ", data.value["logs"][0]["message"])
                if "logs" in data.value
                else None
            ),
        )
        .on(
            "error",  # Log errors
            lambda data, event: print("Agent 🤖 : ", data.error.explain()),
        )
    )

    print("Agent 🤖 : ", json.loads(response.result.text)["messages"][0]["content"])


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except FrameworkError as e:
        traceback.print_exc()
        sys.exit(e.explain())
