# 🌎 Explore Industry specific agents

## 🚀 Introduction

A set of Industry-specific agents are preconfigured using a specific Agent Framework and watsonx.ai LLMs to demonstrate how an Agentic system can be built to answer user questions more accurately and comprehensively compared to simply prompt engineering a standalone LLM. The example domain specific Agents help the user with travel planning, financial analysis and literature research. Each Agent uses the LangGraph framework and a watsonx.ai LLM along with external tools. It combines reasoning and tool calling capabilities of the underlying LLM to create an iterative flow that performs better compared to the LLM's answer based on a single prompt.

---

## 📚 Table of Contents
- [Key Features](#key-features)
- [Workflow](#workflow)
- [Environment Variables](#environment-variables)
- [Installation](#installation)
- [Docker Deployment](#docker-deployment)
- [Example](#example)
- [Contact](#contact)

---

## ✨ Key Features

- A playground with various industry-ready use cases that can be solved with AI Agents.
- Personalized Travel Planner agent: An agent that helps users plan trips by gathering information about destinations, predicting weather conditions, and recommending activities based on real-time data.
- Research Assistant for Academia and Industry: An AI-driven research assistant that can autonomously gather and synthesize information from multiple sources, including Wikipedia, arXiv and web, to generate comprehensive literature reviews or research summaries.
- Financial Market Analysis and Forecasting: Create an agent that autonomously tracks financial news, analyzes historical data, and forecasts future trends. The agent could also compare weather conditions with market trends for agriculture stocks or commodities.

---

## 🔁 Workflow

![image](https://dsce-production-public.s3.us.cloud-object-storage.appdomain.cloud/arch/AI-agentss-accelerator.png)


---


## ⚙️ Environment Variables

### 🔒 Backend (`.env`)
```
WX_ENDPOINT=https://us-south.ml.cloud.ibm.com
WX_PROJECT_ID=
IBM_CLOUD_API_KEY=
FASTAPI_KEY=test
SERPER_API_KEY= # (Optional) If using Google Search
TAVILY_SEARCH_API= # (Optional) If using Tavily Search
USE_CACHE_TOOL_RESPONSES=false # set this to true to use cached tool responses
UPDATE_TOOL_CACHE=false # set this to true to update the tool cache
UPDATE_AGENT_CACHE=false # set this to true to update the agent response cache
LLM_TIMEOUT=30
```

### 🌐 Frontend (`.env`)
```
REACT_APP_LANGGRAPH_BACKEND=http://127.0.0.1:8000/api/v1
```

---

## 🛠️ Installation

### Prerequisites
- Python 3.11+
- Node.js v18+

### Local Execution

1. **Clone the repository**
```bash
git clone https://github.com/your-org/explore-industry-specific-agents.git
cd explore-industry-specific-agents
```

Setup the watsonx orchestrate environment using below guide
https://ibm.github.io/EEL-agentic-ai-bootcamp/labs/environment-setup-lab/wxo-client-setup/


2. **Backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

3. **Frontend**
```bash
cd ../frontend
npm install
npm run dev
```

---

## 🐳 Docker Deployment

1. **Build & Run Backend**
```bash
cd backend
docker build -t explore-industry-specific-agents-backend .
docker run -d -p 8000:8000 --env-file .env explore-industry-specific-agents-backend
```

2. **Start Frontend**
```bash
cd ../frontend
docker build -t explore-industry-specific-agents-frontend .
docker run -d -p 8000:8000 --env-file .env explore-industry-specific-agents-frontend
```

---

## 📦 Example

```text
    "I am planning a trip to New York city next week. Can you get me information about the tourist attractions, weather forecast and social events?"
    "What are some advancements in machine learning applications in healthcare?"
    "Summarize the recent trends in tech stocks?"
```

---

## 📫 Contact

For deployment support, contact [Aishwarya.Pradeep1@ibm.com](mailto:Aishwarya.Pradeep1@ibm.com), [manoj.jahgirdar@in.ibm.com](mailto:manoj.jahgirdar@in.ibm.com)
