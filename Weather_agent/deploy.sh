
ibmcloud target -g itz-wxo-31000122W8_67e2b -r us-east
ibmcloud ce project select --id 72b6b68f-e138-4890-aad8-f65f02f40a97

# ibmcloud ce app create --name bee-external-travel-planner \
# --image us.icr.io/cr-itz-10cifu/bee_external_agent:1.1 \                  
# --min-scale 1 \
# --env-from-secret bee-withoutwx-secrets \
# --registry-secret manoj-creds \    
# --memory 4G \
# --cpu 1 