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


class InventoryToolInput(BaseModel):
    text: str = Field(description="Input message for the Inventory agent")


class InventoryToolResult(BaseModel):
    text: str = Field(description="Response returned from the Inventory agent")


class InventoryToolOutput(ToolOutput):
    result: InventoryToolResult = Field(description="Inventory tool result")

    def get_text_content(self) -> str:
        return to_json(self.result)

    def is_empty(self) -> bool:
        return self.result.text == ""

    def __init__(self, result: InventoryToolResult) -> None:
        super().__init__()
        self.result = result


class InventoryTool(Tool[InventoryToolInput, ToolRunOptions, InventoryToolOutput]):
    name = "InventoryTool"
    description = "Call the inventory_agent with the provided input text"
    input_schema = InventoryToolInput

    def _create_emitter(self) -> Emitter:
        return Emitter.root().child(
            namespace=["tool", "Inventory"],
            creator=self,
        )

    async def _run(
        self, input: InventoryToolInput, options: ToolRunOptions | None, context: RunContext
    ) -> InventoryToolOutput:
        response = await run_agent("inventory_agent", input.text)
        return InventoryToolOutput(result=InventoryToolResult(text=str(response[0])))
