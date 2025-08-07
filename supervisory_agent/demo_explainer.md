🛠️ Maximo Planner Agent: Intelligent Work Order Planning & Execution

Welcome to the **Maximo Planner Agent**, an AI-powered agentic system designed to simulate real-world asset management operations. It automates key decision-making steps such as weather validation, inventory verification, and labor assignment for Maximo work orders—all triggered by a single natural language prompt.

This demo showcases how autonomous agents collaborate to intelligently manage maintenance workflows in Maximo using decentralized reasoning and sequential planning.

---

## 🚀 How It Works

### 1. Ask a Maintenance Question

Start by asking a high-level question about your maintenance workflow. For example:

- "Plan the unplanned workorder."
- "Plan workorder 1301.”
- "Assign labor to workorder 1301 based on availability."
- "Can you check the weather and schedule workorder 1307?"

Your question initiates a chain of agents, each handling a specialized task.

---

### 2. Behind the Scenes: Agents at Work

Once your query is submitted, the following agent workflow is triggered in sequence:

- 🌦️ **Weather Agent** – Checks environmental readiness using Open-Meteo and wttr.in.
- 📦 **Inventory Agent** – Verifies if the required parts are available in Maximo.
- 🧑‍🔧 **Labor Agent** – Assigns a technician based on availability and workload.
- 🧠 **Supervisory Agent** – Coordinates the above agents and compiles a final decision plan.

Each agent uses the **BEE-AI framework** for decision logic, while the **Supervisory Agent**, powered by **bee-ai + ACP server**, routes and orchestrates the overall process.

---

### 3. Review Your Intelligent Maintenance Plan

Once all steps are complete, you’ll receive a breakdown including:

✅ Weather status for the work order location  
✅ Inventory availability with material codes and stock levels  
✅ Assigned labor details including name, availability, and skill match  
✅ A combined, ready-to-execute work order plan

---

## 🧠 What Makes This Demo Unique?

- **Agentic Orchestration:** Simulates how real field planners and supervisors operate.
- **End-to-End Decision Chain:** Weather ➝ Inventory ➝ Labor, coordinated via a supervisory layer.
- **Conversational Control:** No forms or dashboards—just type your request.
- **Transparent Execution Plan:** See exactly how and why each decision was made.

---

## 🧪 Get Started

1. Open the application in your browser.
2. Enter a Maximo-related query like:  
   “Plan workorder 1307 based on weather, inventory, and labor.”
3. Watch the agents collaborate and deliver a maintenance-ready plan.

Experience how AI can act as your next Maximo field planner!

---

## 💡 Tips for Demo Success

- Use queries like:
  - “Plan workorder 1307 based on weather conditions.”
  - “Plan inventory for workorder 1307”
  - “Assign labor to workorder 1307.”
- Try chaining queries to simulate a full maintenance lifecycle.

---
