#!/bin/bash
# Hardcoded API Key (Strongly discouraged for real-world use)
IBM_CLOUD_API_KEY=""
# Optional: Set the IBM Cloud region and resource group
IBM_CLOUD_REGION=""
IBM_CLOUD_RESOURCE_GROUP=""
# Login command
 ibmcloud login --apikey $IBM_CLOUD_API_KEY -r $IBM_CLOUD_REGION -g $IBM_CLOUD_RESOURCE_GROUP