# Maximo Supervisory Agent

This application simulates AI-powered decision-making for Maximo by integrating Maximo REST APIs with a multi-agent workflow powered by the **bee-ai framework**.

The **Supervisory Agent**, built using **bee-ai + ACP server**, interprets user prompts and executes a sequential multi-agent pipeline:

### Agentic Workflow:
**Weather Agent → Inventory Agent → Labor Agent**

Each agent is responsible for a specialized task:
- **Weather Agent**: Checks forecast to determine work feasibility.
- **Inventory Agent**: Verifies material availability for work.
- **Labor Agent**: Assigns available labor resources.

---

# Tech Stack

**Backend:**  
Python 3.11, FastAPI

**Agents Framework:**  
BEE-AI

**Routing + Control:**  
bee-ai + ACP Server

**External APIs:**  
- Maximo REST API  
- Open-Meteo  

**Deployment:**  
- IBM Cloud Code Engine  
- IBM Cloud Container Registry

---

## Folder Structure

```
.
├── main.py                      # Entry point for supervisory agent
├── wrapper/                     # Contains FastAPI wrapper
│   └── app.py                   # Run this for wrapper server
├── src/
│   └── agent/                   # All BEE-AI agents (weather, labor, inventory)
│   └── tools/                   # Supporting tools used by the agents
├── apis/
│   └── generation_weather.py           
|   └── generation_inventory.py 
|   └── generation_labor.py            
├── requirements.txt             # Python dependencies
├── metadata.yaml                
├── demo_explainer.md            # Step-by-step walkthrough of the demo
├── README.md                    
└── ...

```

---


## Local Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Supervisory Agent
```bash
python main.py
```

---

## Running the Wrapper API

To start the REST API of /chat/completions wrapper around the agent logic:

```bash
cd wrapper
python app.py
```

---

## Example Prompts

You can interact with the agent using the following types of prompts:

- Plan the unplanned workorder  
- Plan workorder 1307  
- Plan workorder 1307 based on weather conditions  
- Plan workorder 1307 based on inventory availability  
- Assign labor to workorder 1307 based on their availability  
- Schedule workorder 1307 considering weather forecast  
- Check inventory before planning workorder 1307  
- Assign available technician to workorder 1307  
- Is it feasible to plan workorder 1307 today?  
- What’s the availability of parts for workorder 1307?  
- Who can be assigned to workorder 1307?  
- Plan workorder 1307 using weather, inventory, and labor data  
- Review prerequisites before scheduling workorder 1307  
- Can I proceed with workorder 1307 now?  
- Evaluate readiness for workorder 1307  
- Plan field work for workorder 1307  

---

## Powered By

- [bee-ai Framework](https://github.com/IBM/bee-ai)
- IBM Maximo REST APIs