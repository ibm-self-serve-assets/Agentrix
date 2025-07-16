# 💰 Wealth Management Agent

## 🚀 Introduction

The Wealth management agent is an AI-powered assistant that enhances the productivity of investment professionals by consolidating key financial insights and actions into a single interface. It streamlines tasks such as retrieving and displaying investment reports, summarizing client meetings, and analyzing market performance, eliminating the need to switch between multiple tools. By providing quick access to critical information and automating routine tasks, the agent enables wealth managers to make informed decisions more efficiently, improving client engagement and overall workflow.

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

- Pre-meeting report generation: The financial research and analysis agent can efficiently generate a detailed report for client's portfolio by gathering data from multiple sources.
- Post-meeting MoM summarization: The financial research and analysis agent can summarize meeting transcripts and draft an email with minutes of meeting.
- Market & Financial Insights: The financial research and analysis agent can also provide PoV from Goldman reports (RAG) or get financial insights (Web Search).

---

## 🔁 Workflow


---


## ⚙️ Environment Variables

### 🔒 Backend (`.env`)
```
IBM_CLOUD_API_KEY=
WX_PROJECT_ID=
WX_ENDPOINT=https://us-south.ml.cloud.ibm.com
FASTAPI_KEY=wm
USE_TOOL_CACHE=true # set to false to use the live tool results
TAVILY_API_KEY= # Skip this to use cached responses
```

> Steps to create Tavily API key:
>
> - [Tavily documentation](https://app.tavily.com/home)

### 🌐 Frontend (`.env`)
```
VITE_BACKEND_URL=http://127.0.0.1:8000 # your backend URL
VITE_API_KEY=wm # api key to access the backend URL. (FASTAPI_KEY)
VITE_CHATBOT_NAME="Wealth Manager Agent"
VITE_WELCOME_MESSAGE="Hi, I am a wealth manager agent. How can I assist you today?"
VITE_ENABLE_CHAT=false # set to false to disable chat
```

---

## 🛠️ Installation

### Prerequisites
- Python 3.11+
- Node.js v18+

### Local Execution

1. **Clone the repository**
```bash
git clone https://github.com/your-org/wealth-management-agent.git
cd wealth-management-agent
```
Setup the watsonx orchestrate environment using below guide
https://ibm.github.io/EEL-agentic-ai-bootcamp/labs/environment-setup-lab/wxo-client-setup/


2. **Backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app
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
docker build -t wealth-management-agent-backend .
docker run -d -p 8000:8000 --env-file .env wealth-management-agent-backend
```

2. **Start Frontend**
```bash
cd ../frontend
docker build -t wealth-management-agent-frontend .
docker run -d -p 3000:3000 --env-file .env wealth-management-agent-frontend
```

---

## 📦 Example

```text
    "Give me a report on John Doe's stock investment portfolio"
    "Get the transcript from my previous meeting with John Doe and create an email"
    "How does the US equity market compare to the rest of world?"
```

---

## 📫 Contact

For deployment support, contact [manoj.jahgirdar@in.ibm.com](mailto:manoj.jahgirdar@in.ibm.com)
