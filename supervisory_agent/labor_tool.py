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


class LaborToolInput(BaseModel):
    text: str = Field(description="Input message for the labor agent")


class LaborToolResult(BaseModel):
    text: str = Field(description="Response returned from the labor agent")


class LaborToolOutput(ToolOutput):
    result: LaborToolResult = Field(description="Labor tool result")

    def get_text_content(self) -> str:
        return to_json(self.result)

    def is_empty(self) -> bool:
        return self.result.text == ""

    def __init__(self, result: LaborToolResult) -> None:
        super().__init__()
        self.result = result


class LaborTool(Tool[LaborToolInput, ToolRunOptions, LaborToolOutput]):
    name = "LaborTool"
    description = "Call the labor_agent with the provided input text, Just do one iteration for assignment and if it is unsuccessful then just give summary of error."
    input_schema = LaborToolInput

    def _create_emitter(self) -> Emitter:
        return Emitter.root().child(
            namespace=["tool", "labor"],
            creator=self,
        )

    async def _run(
        self, input: LaborToolInput, options: ToolRunOptions | None, context: RunContext
    ) -> LaborToolOutput:
        response = await run_agent("labor_agent", input.text)
        return LaborToolOutput(result=LaborToolResult(text=str(response[0])))
