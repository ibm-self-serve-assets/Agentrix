# 🚛 Supply Chain Automation Agent (Watsonx Orchestrate Edition)

## 🚀 Introduction

This project is a modular, AI-powered system that simulates end-to-end supply chain operations using IBM Watsonx Orchestrate. It uses autonomous agents for forecasting, inventory checks, procurement, logistics, and compliance, orchestrated by a central controller. The system can be deployed with a FastAPI backend and React-based frontend.

---

## 📚 Table of Contents
- [Key Features](#key-features)
- [Architecture & Tech Stack](#architecture--tech-stack)
- [Environment Variables](#environment-variables)
- [Installation](#installation)
- [Docker Deployment](#docker-deployment)
- [Example](#example)
- [Notes](#notes)
- [Contact](#contact)

---

## ✨ Key Features

- **📈 Forecast Agent** – Predicts demand using Prophet.
- **📦 Inventory Agent** – Evaluates stock levels and flags restock needs.
- **📥 Procurement Agent** – Selects vendors and generates procurement plans.
- **🚚 Logistics Agent** – Plans delivery based on lead times and urgency.
- **📋 Compliance Agent** – Checks vendor eligibility against policies.
- **🧠 Controller Agent** – Orchestrates workflows across all agents.

---

## 🧩 Architecture & Tech Stack

```
User ⟶ Frontend UI (ReactJS(vite))
     ⬇️
FastAPI Backend (Python)
     ⬇️
Watsonx Orchestrate Agent Framework
     ⬇️
+--------------------------+
| Controller Agent         |
|  ↳ Forecast Agent        |
|  ↳ Inventory Agent       |
|  ↳ Procurement Agent     |
|  ↳ Compliance Agent      |
|  ↳ Logistics Agent       |
+--------------------------+

Tech Stack:
- Frontend: ReactJS(Vite), Carbon Design System
- Backend: FastAPI
- AI: IBM watsonx orchestrate
- Deployment: IBM Code Engine, IBM Container Registry
```

---

## ⚙️ Environment Variables

### 🔒 Backend (`.env`)
```
IAM_API_KEY=
INSTANCE_ID=
AGENT_ID=
WXO_INSTANCE_URL=  # watsonx orchestrate deployed url
```

### 🌐 Frontend (`.env`)
```
VITE_BACKEND_URL= # replace this with backend url once this is deployed on CE.
VITE_CHATBOT_NAME="Supply Chain Agent"
VITE_WELCOME_MESSAGE="Hi, I am Supply Chain Agent. How can I assist you today?"
VITE_ENABLE_CHAT=true # set to false to disable chat
VITE_APP_NAME="Supply Chain Agent"
```

---

## 🛠️ Installation

### Prerequisites
- Python 3.11+
- Node.js v18+

### Local Execution

1. **Clone the repository**
```bash
git clone https://github.ibm.com/skol/agentrix-catalogue/tree/main/supply-chain-agent.git
cd supply-chain-agent
```
Setup the watsonx orchestrate environment using below guide:
https://ibm.github.io/EEL-agentic-ai-bootcamp/labs/environment-setup-lab/wxo-client-setup/

2. **Backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
./start.sh        # initializes orchestrate environment
./import-all.sh   # imports agents
uvicorn main:app --reload
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
docker build -t supplychain-backend .
docker run -d -p 8000:8000 --env-file .env supplychain-backend
```

2. **Start Frontend**
```bash
cd ../frontend
npm run build
serve -s dist
```

---

## 📦 Example

```text
"Can you do an end to end planning fro the upcoming 4 weeks"
"Forecast sales for SKU001 for the next month"
"We need to restock SKU001 and choose the best vendor."
"Verify compliance of Supplier A with ESG norms."
```

---

## 📒 Notes
- This system is event-driven but not chat-based by default.
- It is extensible via YAML agents and Python tools in Orchestrate.

---

## 📫 Contact

For deployment support, contact [brunda.reddy@ibm.com](mailto:brunda.reddy@ibm.com)
