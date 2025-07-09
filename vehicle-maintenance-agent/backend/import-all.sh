#!/usr/bin/env bash
set -x

# Resolve absolute path of current script
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Import tools
for tool_path in get_nearest_service_center.py get_vehicle_telematics.py; do
  orchestrate tools import -k python -f "${SCRIPT_DIR}/tools/${tool_path}" -r "${SCRIPT_DIR}/tools/requirements.txt"
done

# Deploy the Knowledge
orchestrate knowledge-bases import -f knowledge_bases/knowledge.yaml

# Import agents
for agent_yaml in vehicle_telematics.yaml agent.yaml; do
  orchestrate agents import -f "${SCRIPT_DIR}/agents/${agent_yaml}"
done

# (Optional) List everything
orchestrate tools list
orchestrate agents list
orchestrate knowledge-bases list
