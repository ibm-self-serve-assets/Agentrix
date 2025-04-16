# from flask import Flask, jsonify, request
# from flask_restx import Api
# from flask_cors import CORS
# import logging
# from ApiMaximo import maximo_ns

# # Flask app setup
# app = Flask(__name__)
# CORS(app)
# api = Api(app, version='1.0', title='Maximo Work Order API', 
#           description='API for processing Maximo Work Orders', 
#           doc='/swagger/', openapi_version='3.0.2')

# # Add namespaces (from ApiMaximo)
# api.add_namespace(maximo_ns)

# # Logging Configuration
# logging.basicConfig(
#     format='%(asctime)s - %(levelname)s:%(message)s',
#     handlers=[
#         logging.StreamHandler(),  # Print to console
#     ],
#     level=logging.INFO
# )

# # Define a simple homepage route
# @app.route('/')
# def index():
#     return "Welcome to the Maximo Work Order API!"

# # Main method (entry point)
# def main():
#     logging.info("Main started...")

# # Main entry point
# if __name__ == '__main__':
#     logging.info("Starting Maximo Work Order API...")
#     app.run(host='0.0.0.0', port=8080, debug=True)


# from beeai_framework.backend.chat import ChatModel
# from beeai_framework.workflows.agent import AgentWorkflow, AgentWorkflowInput
# from beeai_framework.tools.weather import OpenMeteoTool
# from flask import Flask, jsonify

# from flask import request
# from Agentmaximo import *

# # Flask app setup
# app = Flask(__name__)

# @app.route('/process_workorder', methods=['POST'])
# async def process_workorder():
#     data = request.get_json()
#     wonum = data.get("wonum")

#     if not wonum:
#         return jsonify({"error": "Work order number ('wonum') is required."}), 400

#     # Fetch work order details from Maximo
#     agent_maximo = AgentMaximo()
#     coords = agent_maximo.fetch_maximo_wo_details(wonum)

#     if coords["LONGITUDEX"] == "N/A" or coords["LATITUDEY"] == "N/A":
#         return jsonify({"error": "Latitude/Longitude not found for this work order."}), 404

#     # Initialize LLM and workflow for decision-making
#     llm = ChatModel.from_name("ollama:granite3.1-dense:8b")
#     workflow = AgentWorkflow(name="WO Smart Weather Scheduler")

#     # Adding agents directly in the function
#     workflow.add_agent(
#         name="WeatherAgent",
#         role="Weather Data Fetcher",
#         instructions=(
#             "Use the provided latitude and longitude to fetch a 3-day weather forecast. "
#             "Extract and summarize temperature, precipitation, and wind conditions in a concise format."
#         ),
#         tools=[OpenMeteoTool()],
#         llm=llm
#     )

#     workflow.add_agent(
#         name="SummaryAgent",
#         role="Decision Engine",
#         instructions=(
#             "You are a decision engine that determines whether to schedule or delay field work based on weather data. "
#             "Only respond with one of the following: 'Schedule the work' or 'Delay the work due to [reason]'. "
#             "Consider temperature, rain, snow, storm, and wind. Be concise and decisive."
#             "After summary, only respond with one of these exact statements:\n\n"
#             "- 'Yes, schedule the workorder.'\n"
#             "- 'No, delay the workorder due to [brief reason].'\n\n"
#         ),
#         llm=llm
#     )

#     # Running the workflow
#     response = await workflow.run([
#         AgentWorkflowInput(prompt=f"Use OpenMeteoTool to get a 3-day weather forecast for latitude {coords['LONGITUDEX']} and longitude {coords['LATITUDEY']}."),
#         AgentWorkflowInput(prompt="Based on the above weather, should work be scheduled or delayed?"),
#     ]).on(
#         "success",
#         lambda data, event: print(
#             f"\n-> Step '{data.step}' has been completed with the following outcome.\n\n{data.state.final_answer}"
#         ),
#     )

#     # Fetching the decision from LLM
#     summary = response.result.final_answer
#     print("\nLLM Decision:", summary)

#     # Make update or decision based on LLM output
#     if "schedule the workorder" in summary.lower():
#         update_result = agent_maximo.update_schedule(wonum)
#         return jsonify({"final_decision": "Yes, schedule the workorder.", "update_response": update_result}), 200
#     else:
#         return jsonify({"final_decision": summary, "update_response": "No update made to the work order."}), 200


# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=3000)




from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
from flask_restx import Api

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Swagger API configuration
api = Api(
    app,
    version='1.0',
    title='Maximo Work Order API',
    description='API for processing Maximo Work Orders',
    doc='/swagger/',
    openapi_version='3.0.2'
)

# Import and register namespaces
from ApiMaximo import maximo_ns

api.add_namespace(maximo_ns)

# Logging Configuration
logging.basicConfig(
    format='%(asctime)s - %(levelname)s:%(message)s',
    handlers=[
        logging.StreamHandler()
    ],
    level=logging.INFO
)

# Homepage route (optional)
@app.route('/')
def index():
    return app.send_static_file('index.html')

# Main entry point
if __name__ == '__main__':
    logging.info("Starting Maximo Work Order API...")
    app.run(host='0.0.0.0', port=3000, debug=True)

