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
import requests
import os
from dotenv import load_dotenv

load_dotenv()

async def run_agent(agent: str, input: str) -> list[Message]:
    async with Client(base_url="http://localhost:8000") as client:
        run = await client.run_sync(
            agent=agent, input=[Message(parts=[MessagePart(content=input, content_type="text/plain")])]
        )
    return run.output


class UnplannedWorkOrderToolInput(BaseModel):
    dummy: str = Field(default="", description="No input required")


class UnplannedWorkOrderToolResult(BaseModel):
    workorders: list[str] = Field(description="List of up to 5 unplanned work order numbers")


class UnplannedWorkOrderToolOutput(ToolOutput):
    result: UnplannedWorkOrderToolResult = Field(description="Unplanned Work Order tool result")

    def get_text_content(self) -> str:
        return to_json(self.result)

    def is_empty(self) -> bool:
        return not self.result.workorders

    def __init__(self, result: UnplannedWorkOrderToolResult) -> None:
        super().__init__()
        self.result = result


class FetchUnplannedWorkorderTool(Tool[UnplannedWorkOrderToolInput, ToolRunOptions, UnplannedWorkOrderToolOutput]):
    name = "FetchUnplannedWorkorderTool"
    description = "Fetch unplanned Maximo work orders (status=WAPPR and FLOWCONTROLLED=true)"
    input_schema = UnplannedWorkOrderToolInput

    def _create_emitter(self) -> Emitter:
        return Emitter.root().child(
            namespace=["tool", "FetchUnplannedWorkorder"],
            creator=self,
        )
    
    # async def _run(
    #     self, input: UnplannedWorkOrderToolInput, options: ToolRunOptions | None, context: RunContext
    # ) -> UnplannedWorkOrderToolOutput:
    #     response = await run_agent("get_workorder_agent")
    #     return UnplannedWorkOrderToolOutput(result=UnplannedWorkOrderToolResult(text=str(response[0])))


    async def _run(
        self, input: UnplannedWorkOrderToolInput, options: ToolRunOptions | None, context: RunContext
    ) -> UnplannedWorkOrderToolOutput:
        try:
            api_key = os.getenv("MAXIMO_APIKEY", "")
            base_url = os.getenv("MAXIMO_BASE_URL", "")
            endpoint = f"{base_url}/maximo/api/os/AGAPIWODETAILS"

            query_params = {
                "apikey": api_key,
                "lean": "1",
                "ignorecollectionref": "1",
                "oslc.select": "wonum,description,siteid",
                "oslc.where": 'status="WAPPR" and schedstart!="*" and schedfinish!="*" and FLOWCONTROLLED=true'
            }

            response = requests.get(endpoint, params=query_params, verify=False)

            if response.status_code == 200:
                data = response.json()
                results = []

                if "member" in data:
                    for item in data["member"]:
                        wonum = item.get("wonum", "N/A")
                        results.append(wonum)
                        if len(results) == 5:
                            break

                return UnplannedWorkOrderToolOutput(
                    result=UnplannedWorkOrderToolResult(workorders=results)
                )

            else:
                return UnplannedWorkOrderToolOutput(
                    result=UnplannedWorkOrderToolResult(workorders=[])
                )

        except Exception as e:
            return UnplannedWorkOrderToolOutput(
                result=UnplannedWorkOrderToolResult(workorders=[f"Error: {str(e)}"])
            )
