# IBM Closet Companion

## Introduction
This is an AI Companion that assists you with fashion choices (wardrobe recommendations) based on your calendar events using watsonx.ai and Agentic AI.

---

## Table of Contents
- [Key Features](#key-features)
- [Architecture & Tech Stack](#architecture--tech-stack)
- [Environment Variables](#environment-variables)
- [Installation](#installation)
- [Docker Deployment](#docker-deployment)

---

## Key Features
- User Personalization: Enables login through predefined personas or temporary users, ensuring flexibility and fast onboarding.

- Event Management: Users can view and create custom events, promoting ongoing interaction and repeat usage.

- Integrated AI Services: AI-generated styling and travel suggestions offer value-added, premium features with potential for monetization through partnerships or subscription models.

- User Context & Data Utilization: Access to profile details and wardrobe items allows the app to deliver contextual, data-driven recommendations, increasing user satisfaction and stickiness.

- Scalable Design: Persona-based login with logout and switch capabilities supports diverse user testing, team collaboration, or customer journey simulations in various business scenarios.


---

## Architecture & Tech Stack

The application is designed with a modular and data-driven architecture to deliver personalized event-based recommendations

- User Profile Input: Captures personal attributes such as name, age, weight, height, and body shape, enabling tailored content delivery.

- Event Management Module: Displays synthetic event data and allows creation of custom events with fields like name, date, location, and description.

- Recommendation Engine: Dynamically generates suggestions per event, using user profile data and event-specific details.

- Agentic Framework Integration: Utilizes personal data, event context (purpose, location, weather), and wardrobe inventory to perform gap analysis and generate AI-powered styling & travel recommendations.

Tech Stack:
- Frontend : ReactJS, Carbon Design System
- Backend: Fast APIs, IBM Cloudant
- AI: IBM watsonx.ai, LangGraph
- Deployment: IBM Code Engine, IBM Container Registry (ICR)

---

## Environment Variables

### Backend (`.env`)
```
WX_URL= # watsonx.ai URL
WX_APIKEY= # IBM Cloud APIKey
PROJECT_ID= # watsonx.ai Project ID
```

### Frontend (`.env`)
```
REACT_APP_BASE_URL= # replace this with backend url once this is deployed on CE
REACT_APP_BASE_URL_SECONDARY= # replace this with backend url once this is deployed on CE
```

---

## Installation

### Prerequisites
- Python 3.11+
- Node.js v18+

### Local Execution

1. **Clone the repository**
```bash
git clone https://github.ibm.com/skol/agentrix-catalogue.git
cd fashionapp
```

2. **Backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

3. **Frontend**
```bash
cd ../frontend
npm install
npm start
```

---

## Docker Deployment

1. **Build & Run Backend**
```bash
cd backend
docker build -t closetcompanion-backend .
docker run -d -p 8000:8000 --env-file .env closetcompanion-backend
```

2. **Start Frontend**
```bash
cd ../frontend
npm install
npm start
```

---

## Contact

For deployment support, contact [aishwarya.pradeep1@ibm.com]