
from flask_restx import Namespace, Resource, fields
from Agentmaximo import AgentMaximo
from flask import request, jsonify
import asyncio
from beeai_framework.backend.chat import ChatModel
from beeai_framework.workflows.agent import AgentWorkflow, AgentWorkflowInput
from beeai_framework.tools.weather import OpenMeteoTool
import re

maximo_ns = Namespace('maximo', description='Maximo Operations')

work_order_input_model = maximo_ns.model('WorkOrderInput', {
    'query': fields.String(required=True, description='Query related to workorder')
})

work_order_output_model = maximo_ns.model('WorkOrderOutput', {
    'weather_response':  fields.String(description='Response of weather API'),
    'final_decision': fields.String(description='Summary of weather decision'),
    'update_response': fields.String(description='Response from Maximo scheduler')
})

@maximo_ns.route('/')
class MaximoWorkflow(Resource):
    @maximo_ns.expect(work_order_input_model)
    @maximo_ns.marshal_with(work_order_output_model)
    def post(self):
        data = request.json
        query = data.get("query")

        # Extract number after "wonum"
        match = re.search(r'\bwonum\s+(\d+)', query, re.IGNORECASE)
        if match:
            wonum = match.group(1)
        else:
            wonum = None

        if not wonum:
            return {"final_decision": "Missing wonum", "update_response": "Work order number is required."}, 400

        async def run_workflow():
            agent_maximo = AgentMaximo()
            coords = agent_maximo.fetch_maximo_wo_details(wonum)

            if coords["LONGITUDEX"] == "N/A" or coords["LATITUDEY"] == "N/A":
                return {"final_decision": "Invalid Coordinates", "update_response": "Latitude/Longitude not found."}

            llm = ChatModel.from_name("ollama:granite3.1-dense:8b")
            workflow = AgentWorkflow(name="WO Smart Weather Scheduler")

            workflow.add_agent(
                name="WeatherAgent",
                role="Weather Data Fetcher",
                instructions=(
                    "Use the provided latitude and longitude to fetch a 3-day weather forecast using OpenMeteoTool.\n"
                    "Generate a detailed and human-readable weather summary with this format:\n\n"
                    "The 3-day weather forecast for the given coordinates is as follows:\n\n"
                    "**Day 1:**\n"
                    "- Temperature: High of ...°F (...°C), low of ...°F (...°C)\n"
                    "- Precipitation: ...% chance of rain\n"
                    "- Wind: ...\n\n"
                    "**Day 2:**\n"
                    "- Temperature: High of ...\n"
                    "- Precipitation: ...\n"
                    "- Wind: ...\n\n"
                    "**Day 3:**\n"
                    "- Temperature: High of ...\n"
                    "- Precipitation: ...\n"
                    "- Wind: ...\n\n"
                    "Make the summary clear and well-formatted for decision-making."
                ),
                tools=[OpenMeteoTool()],
                llm=llm
            )

            workflow.add_agent(
                name="SummaryAgent",
                role="Decision Engine",
                instructions=(
                    "You are a decision engine that determines whether to schedule or delay field work based on the provided weather summary.\n\n"
                    "Consider temperature extremes, high precipitation, storms, and wind when making your decision.\n"
                    "After reading the forecast, respond with one of the following exact sentences:\n\n"
                    "- 'Yes, schedule the workorder.'\n"
                    "- 'No, delay the workorder due to [reason].'\n\n"
                    "Do not repeat the weather summary, only respond with your decision."
                ),
                llm=llm
            )

            response = await workflow.run([
                AgentWorkflowInput(prompt=f"Use OpenMeteoTool to get a 3-day weather forecast for latitude {coords['LONGITUDEX']} and longitude {coords['LATITUDEY']}."),
                AgentWorkflowInput(prompt="Based on the above weather, should work be scheduled or delayed?")
            ])

            
            weather_forecast = response.steps[0].state.final_answer
            summary = response.result.final_answer

            if "schedule the workorder" in summary.lower():
                update_result = agent_maximo.update_schedule(wonum)
                return {
                    "weather_response":weather_forecast,
                    "final_decision": summary,
                    "update_response": update_result.get("message", str(update_result))
                }
            else:
                return {
                    "weather_response":weather_forecast,
                    "final_decision": summary,
                    "update_response": "No update made to the work order."
                }

        return asyncio.run(run_workflow())
