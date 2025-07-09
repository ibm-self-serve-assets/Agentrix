#!/bin/bash
set -e

# Step 1: Register Watsonx Orchestrate environment
orchestrate env add --name agentrix --url "$WXO_INSTANCE_URL" -t ibm_iam || true
orchestrate env activate agentrix --apikey "$IAM_API_KEY"

cd ../frontend || true
npm install
npm run build

cd ../backend || true

# Step 2: Start the backend
uvicorn main:app --host 0.0.0.0 --port 8010


