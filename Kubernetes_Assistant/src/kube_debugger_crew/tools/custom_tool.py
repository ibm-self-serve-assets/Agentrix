import io
from io import BytesIO
from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from k8scluster import K8sCluster
from flask import session


class KubeInput(BaseModel):
    namespace: str = Field(..., description="Kubernetes pod's namespace")
    pod: str = Field(..., description="Kuberenetes pod")
    issue: str = Field(..., description="Status of the failing Pod")


class KubeTool(BaseTool):
    name: str = "Kubernetes Logs collector"
    description: str = (
        "Use this tool to collect the Pod logs, Pod status and Kubernetes events for issue debugging purpose."
    )
    args_schema: Type[BaseModel] = KubeInput

    def _run(self, namespace: str, pod: str, issue: str) -> str:
        # Implementation goes here
        file_path = session.get('kubeconfig')
        with open(file_path, 'r') as file:
            file_content = file.read()
        kubeconfig_file_object = io.BytesIO(file_content.encode('utf-8'))
        k8scluster = K8sCluster(configfile=kubeconfig_file_object)
        pod_status = k8scluster.pod_status_details(ns=namespace,
                                                   podname=pod)  # k8s_cluster.pod_status_details(namespace,pod)
        pod_logs = k8scluster.read_pod_logs(ns=namespace, podname=namespace)
        pod_events = k8scluster.read_pod_events(ns=namespace, podname=pod)
        pod_details = pod_status.__str__() + "\n" + pod_logs.__str__() + "\n" + pod_events
        return (pod_details)


class KubeInputForOwner(BaseModel):
    namespace: str = Field(..., description="Kubernetes pod's namespace")
    pod: str = Field(..., description="Kuberenetes pod")

class PodOrMgrYaml(BaseTool):
    # Return the Yaml of POD or Pod owner (if deployment or statefulset owns this pod
    name: str = "Kubernetes Pod or Deployment or StatefulSet YAML"
    description: str = (
        "Use this tool to retrieve the Pod owner yaml or Pod yaml if there is no owner of the pod"
    )
    args_schema: Type[BaseModel] = KubeInputForOwner

    def _run(self, namespace: str, pod: str) -> str:
        file_path = session.get('kubeconfig')
        with open(file_path, 'r') as file:
            file_content = file.read()
        kubeconfig_file_object = io.BytesIO(file_content.encode('utf-8'))
        k8scluster = K8sCluster(configfile=kubeconfig_file_object)
        owner, name = k8scluster.get_pod_owner(ns=namespace, pod_name=pod)
        #print(f"Pod Owner: {owner}, OwnerName: {name}")
        if owner is None:
            return (k8scluster.get_pod_yaml(ns=namespace, podname=pod))
        elif owner == "Deployment":
            return (k8scluster.get_deploy_yaml(ns=namespace, deploy_name=name))
        elif owner == "StatefulSet":
            return (k8scluster.get_sts_yaml(ns=namespace, sts_name=name))
        else:
            return ""
