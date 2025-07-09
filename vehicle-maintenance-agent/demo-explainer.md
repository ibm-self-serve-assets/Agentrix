# Agent Use Case Walkthrough

Follow these four simple steps to understand, try, and build upon this AI agent use case:

---

## Step 1: Review the Use Case Summary

This asset will simulate a vehicle troubleshooting scenario. Here the scenario is that a vehicle that has Internet of Things (IoT) has broken down and the user is seeking for help. The car has some weird noise and the user asks the chatbot why is there a noise what does it mean? and the AI Agent goes through reasoning to find out what went wrong and provide an analysis report and find nearest service center.

---

## Step 2: Try the Interactive Demo Application

Launch the demo to test the agent’s capabilities in real-time.

- Navigate to the deployed agent URL or run it locally
- Use the sample input provided.
- Observe outputs, logs, or UI responses

### Demo Explainer

1. Once the wealth manager agent application is opened, you will be presented with a welcome message and 3 sample prompts.
    - What does the engine temperature warning light mean?
    - My car is shaking and I have the engine temperature warning light on can you diagnose it?
    - Where is the nearest service center?

    Note: The text field is disabled on DSCE to prevent abusing the foundation model and only the three main prompts are given to try out. You can download the code to use the chat functionality.

2. Click on the first prompt `What does the engine temperature warning light mean?`. The agent will use the Knowledge base (RAG) and answer this query.

3. Click on the second prompt `My car is shaking and I have the engine temperature warning light on can you diagnose it?`. The agent will transfer the control to Telematics data analyzer agent which will ask follow-up questions if required and give a car health report. The car report is read, and a suggestion is provided by the Troubleshoot agent.

4. Click on the third prompt `Where is the nearest service center?` The agent will invoke the Get nearest service center tool and pass the lat & long received from the Telematics data analyzer agent (assumption is that car will send the current lat & long data as part of telematics data.) and get the nearest service centers from the list of service centers.

---

## Step 3: Get an Application Code Sample

Download or clone the sample application code that powers the demo.

```bash
git clone https://github.com/your-org/agent-template
cd agent-template/agent-your-agent
```

> The sample assumes you have **Python 3+** installed. If not, [download it here](https://www.python.org/downloads/).

- Modify the logic in `backend/app/`
- Add/change the UI (if applicable) in `frontend/src/`
- Refer to `README.md` in the root folder to set up and run locally

---

## Step 4: Explore the Technology Powering This Use Case

Learn about the AI models, frameworks, and infrastructure behind the agent:

- watsonx Orchestrate
- React / Vite for frontend (optional)
- Open-source models like Llama, BERT, or LangChain for logic
- Containerized deployment using Docker

---
