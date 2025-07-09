#!/bin/bash
set -e

# Step 1: Register Watsonx Orchestrate environment
orchestrate env add --name bootcamp --url "$WXO_INSTANCE_URL" -t ibm_iam || true
orchestrate env activate bootcamp --apikey "$IAM_API_KEY"

# Step 2: Start the backend
uvicorn main:app --host 0.0.0.0 --port 8000


