#!/usr/bin/env bash
set -x

# Resolve absolute path of current script
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Import tools
for tool_path in forecast_tool.py inventory_tool.py procurement_tool.py logistics_tool.py compliance_tool.py; do
  orchestrate tools import -k python -f "${SCRIPT_DIR}/tools/${tool_path}" -r "${SCRIPT_DIR}/requirements.txt"
done

# Import agents
for agent_yaml in forecast_agent.yaml inventory_agent.yaml procurement_agent.yaml logistics_agent.yaml compliance_agent.yaml controller_agent.yaml; do
  orchestrate agents import -f "${SCRIPT_DIR}/agents/${agent_yaml}"
done

# (Optional) List everything
orchestrate tools list
orchestrate agents list
orchestrate knowledge-bases list
