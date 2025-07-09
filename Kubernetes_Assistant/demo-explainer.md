## Demo Explainer
1- User can provide the kubeconfig file to connect to his/her Kubernetes/Openshift cluster. Only read permissions are 
required for the cluster.

2- After connecting to cluster, user can select a namespace to list the unhealthy pods in that namespace if troublshooting 
the issue or can select a deployment/statefulset if scanning for security vulnerabilities.

3- After this user can select an unhealthy pod and 'diagnose with watsonx' to get the summary and possible resolutions 
for the unhealthy pod. If scanning the deployment/statefulset for security vulnerabilities, user can select specific 
deployment/statefulset and ask watsonx to scan and recommend.

4- User can use 'Ask a Kubernetes Question' if he/she needs to understand what a given resolution step means or how to perform it.

5- If the issue summary/resolution indicated any problem with the pod definition, user can use 'Peer Review Kubernetes Code'
for the Pod or it's owning resource, like Deployment/StatefulSet etc.

6- If user is having any difficulty in understanding the related Kubernetes code, he/she can use 'Explain Kubernetes Code'.

7- 'Kubernetes Code Generation' can be used by SREs to generate code for Kubernetes objects like, configMaps, Secrets, 
Deployments if required.