#!/bin/bash
set -e
# ibmcloud target -g Default -r us-east
# ibmcloud ce project select --id ac68787f-3624-49bb-97af-323d51f81def
ibmcloud ce project select --id 72b6b68f-e138-4890-aad8-f65f02f40a97
ibmcloud ce app logs --application bee-external --follow