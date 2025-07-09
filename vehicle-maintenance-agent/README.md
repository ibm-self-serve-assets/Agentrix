# 🚗 Vehicle Maintenance Agent (Watsonx Orchestrate Edition)

## 🚀 Introduction

The Vehicle Maintenance Assistant is an AI Agent designed to help car owners identify and understand vehicle issues by interpreting natural language inputs like “My car is shaking” or “Check engine light is on.” It combines real-time telematics data, diagnostic trouble codes (DTCs), and vehicle documentation to offer personalized, accurate diagnostics and actionable guidance such as finding nearby service centers, etc. The system can be deployed with a FastAPI backend and React-based frontend.

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

- Customer Experience: Reduces stress for drivers by providing instant, understandable insights.
- Service Optimization: Reduces unnecessary service visits and helps service centers prioritize real issues.
- Brand Loyalty: Builds trust by offering proactive, intelligent support post-purchase.
- Data Utilization: Leverages telematics data and DTC documentation to deliver accurate, data-driven support.
- Scalability: Easily extendable across vehicle models, regions, and support channels (mobile app, web, IVR).

---

## 🔁 Workflow

![image](https://github.ibm.com/skol/agentrix-catalogue/assets/244854/3ec8a4b1-bccd-4c16-b1f5-d5bd49f3cc20)


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
VITE_CHATBOT_NAME="Vehicle Maintenance Agent"
VITE_WELCOME_MESSAGE="Hi, I am Vehicle Maintenance Agent. How can I assist you today?"
VITE_ENABLE_CHAT=true # set to false to disable chat
VITE_APP_NAME="Vehicle Maintenance Agent"
```

---

## 🛠️ Installation

### Prerequisites
- Python 3.11+
- Node.js v18+

### Local Execution

1. **Clone the repository**
```bash
git clone https://github.com/your-org/vehicle-maintenance-agent.git
cd vehicle-maintenance-agent
```
Setup the watsonx orchestrate environment using below guide
https://ibm.github.io/EEL-agentic-ai-bootcamp/labs/environment-setup-lab/wxo-client-setup/


2. **Backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
./start.sh #initialises the orchesrate environment
./import-all.sh # run this to import the agents to the environment.
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
docker build -t vehicle-maintenance-agent-backend .
docker run -d -p 8000:8000 --env-file .env vehicle-maintenance-agent
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
    "What does the engine temperature warning light mean?"
    "My car is shaking and I have the engine temperature warning light on can you diagnose it?"
    "Where is the nearest service center?"
```

---

## 📫 Contact

For deployment support, contact [manoj.jahgirdar@in.ibm.com](mailto:manoj.jahgirdar@in.ibm.com)
