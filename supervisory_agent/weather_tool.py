# Copyright 2025 © BeeAI a Series of LF Projects, LLC
# SPDX-License-Identifier: Apache-2.0

from acp_sdk import Message
from acp_sdk.client import Client
from acp_sdk.models import MessagePart
from beeai_framework.context import RunContext
from beeai_framework.emitter import Emitter
from beeai_framework.tools import ToolOutput
from beeai_framework.tools.tool import Tool
from beeai_framework.tools.types import ToolRunOptions
from beeai_framework.utils.strings import to_json
from pydantic import BaseModel, Field


async def run_agent(agent: str, input: str) -> list[Message]:
    async with Client(base_url="http://localhost:8000") as client:
        run = await client.run_sync(
            agent=agent, input=[Message(parts=[MessagePart(content=input, content_type="text/plain")])]
        )
    return run.output


class WeatherToolInput(BaseModel):
    text: str = Field(description="Input message for the Weather agent")


class WeatherToolResult(BaseModel):
    text: str = Field(description="Response returned from the Weather agent")


class WeatherToolOutput(ToolOutput):
    result: WeatherToolResult = Field(description="Weather tool result")

    def get_text_content(self) -> str:
        return to_json(self.result)

    def is_empty(self) -> bool:
        return self.result.text == ""

    def __init__(self, result: WeatherToolResult) -> None:
        super().__init__()
        self.result = result


class WeatherTool(Tool[WeatherToolInput, ToolRunOptions, WeatherToolOutput]):
    name = "WeatherTool"
    description = "Call the weather_agent with the provided input text"
    input_schema = WeatherToolInput

    def _create_emitter(self) -> Emitter:
        return Emitter.root().child(
            namespace=["tool", "Weather"],
            creator=self,
        )

    async def _run(
        self, input: WeatherToolInput, options: ToolRunOptions | None, context: RunContext
    ) -> WeatherToolOutput:
        response = await run_agent("weather_agent", input.text)
        return WeatherToolOutput(result=WeatherToolResult(text=str(response[0])))
