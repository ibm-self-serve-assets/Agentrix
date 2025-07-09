import yaml
from kubernetes import client, config


class K8sCluster:
    def __init__(self, configfile):
        config.load_kube_config(config_file=configfile)
        self.cluster = client.CoreV1Api()
        self.cluster_apps = client.AppsV1Api()

    def list_namespaces(self) -> list:
        list_of_ns = []
        v1_namespaces = self.cluster.list_namespace().items
        for ns in v1_namespaces:
            list_of_ns.append(ns.metadata.name)
        return list_of_ns

    def list_pods(self, ns):
        list_of_pods = []
        v1_pods = self.cluster.list_namespaced_pod(namespace=ns).items
        # print(v1_pods)
        for pod in v1_pods:
            list_of_pods.append(pod.metadata.name)
        return list_of_pods

    def list_deploys(self, ns):
        list_of_deploys = []
        v1_deploys = self.cluster_apps.list_namespaced_deployment(namespace=ns).items
        for deploy in v1_deploys:
            list_of_deploys.append(deploy.metadata.name)
        return list_of_deploys

    def list_sts(self, ns):
        list_of_sts = []
        v1_sts = self.cluster_apps.list_namespaced_stateful_set(namespace=ns).items
        for sts in v1_sts:
            list_of_sts.append(sts.metadata.name)
        return list_of_sts

    def unhealthy_pods(self, ns):
        list_unhealthy_pods = []
        pods = self.cluster.list_namespaced_pod(namespace=ns).items
        for pod in pods:
            if not self.is_pod_ready(pod):
                list_unhealthy_pods.append(pod.metadata.name)
        return list_unhealthy_pods

    def is_pod_ready(self, pod):
        # Check if all conditions indicate the pod is ready
        if pod.status.phase == "Pending":
            return False
        for condition in pod.status.conditions:
            if condition.type == 'Ready' and condition.status != 'True' and condition.reason != 'PodCompleted':
                return False

        return True

    def pod_status_details(self, ns, podname) -> dict:
        pod = self.cluster.read_namespaced_pod(namespace=ns, name=podname)
        containerstatus = []
        try:
            for container_status in pod.status.container_statuses:
                try:
                    last_state = container_status.last_state
                except AttributeError:
                    last_state = container_status.state

                last_state = {
                    "name": container_status.name,
                    "ready": container_status.ready,
                    "last_state": last_state,
                }
                containerstatus.append(last_state)
            pod_status = {
                "name": pod.metadata.name,
                "namespace": pod.metadata.namespace,
                "phase": pod.status.phase,
                "conditions": pod.status.conditions,
                "container statuses": containerstatus
            }
        except TypeError:
            pod_status = {
                "name": pod.metadata.name,
                "namespace": pod.metadata.namespace,
                "phase": pod.status.phase,
                "conditions": pod.status.conditions,
                "container statuses": ""
            }

        return pod_status

    def read_pod_logs(self, ns, podname, tail_lines=20):
        try:
            pod = self.cluster.read_namespaced_pod(namespace=ns, name=podname)
            logs = {}
            for container in pod.spec.containers:
                container_name = container.name
                try:
                    log_data = self.cluster.read_namespaced_pod_log(
                        name=podname,
                        namespace=ns,
                        container=container_name,
                        tail_lines=tail_lines
                    )
                    logs[container_name] = log_data
                except Exception as e:
                    print(f"Error reading logs: {e}")
                    # logs[container_name] = ""
            return logs
        except Exception as e:
            return ""

    def read_pod_events(self, ns, podname):
        eventlist = ""
        try:
            pod_events = self.cluster.list_namespaced_event(namespace=ns,
                                                            field_selector=f'involvedObject.name={podname}')
            for event in pod_events.items:
                eventlist = eventlist + " " + f"Event: {event.message} ({event.reason})"
        except Exception as e:
            print(f"Error reading events: {e}")
        return eventlist

    def get_pod_yaml(self, ns, podname):
        try:
            pod = self.cluster.read_namespaced_pod(name=podname, namespace=ns)
        except Exception as e:
            print(f"Error: {e}")
            return None
        pod_yaml = client.ApiClient().sanitize_for_serialization(pod)
        pod_yaml_str = yaml.dump(pod_yaml)
        return pod_yaml_str

    def get_deploy_yaml(self, ns, deploy_name):
        try:
            deployment = self.cluster_apps.read_namespaced_deployment(name=deploy_name, namespace=ns)
        except Exception as e:
            print(f"Error: {e}")
            return None
        # Convert deployment to dictionary
        deployment_dict = client.ApiClient().sanitize_for_serialization(deployment)

        # Remove metadata.managedFields and status sections
        metadata = deployment_dict.get('metadata', {})
        metadata.pop('managedFields', None)
        metadata.pop('annotations', None)
        metadata.pop('creationTimestamp', None)
        metadata.pop('generation', None)
        metadata.pop('ownerReferences', None)
        metadata.pop('resourceVersion', None)
        metadata.pop('uid', None)
        deployment_dict.pop('status', None)

        # Dump dictionary to YAML string
        deployment_yaml_str = yaml.dump(deployment_dict)
        return deployment_yaml_str

    def get_sts_yaml(self, ns, sts_name):
        try:
            sts = self.cluster_apps.read_namespaced_stateful_set(name=sts_name, namespace=ns)
        except Exception as e:
            print(f"Error: {e}")
            return None

        sts_dict = client.ApiClient().sanitize_for_serialization(sts)

        # Remove metadata.managedFields and status sections
        metadata = sts_dict.get('metadata', {})
        metadata.pop('managedFields', None)
        metadata.pop('annotations', None)
        metadata.pop('creationTimestamp', None)
        metadata.pop('generation', None)
        metadata.pop('ownerReferences', None)
        metadata.pop('resourceVersion', None)
        metadata.pop('uid', None)
        sts_dict.pop('status', None)

        # Dump dictionary to YAML string
        sts_yaml_str = yaml.dump(sts_dict)
        return sts_yaml_str

    def get_pod_owner(self, ns, pod_name):
        """
        Get the type and name of the Deployment or StatefulSet associated with a pod, if applicable.

        Returns:
            tuple: (owner_type, owner_name) where owner_type is 'Deployment' or 'StatefulSet',
                   and owner_name is the name of the associated object. Returns (None, None) if not found.
        """
        try:
            # Fetch pod details
            pod = self.cluster.read_namespaced_pod(name=pod_name, namespace=ns)
            owner_references = pod.metadata.owner_references

            if not owner_references:
                return None, None  # Pod has no owner

            # Check the owner references
            for owner in owner_references:
                if owner.kind == "ReplicaSet":
                    # Find the Deployment associated with the ReplicaSet
                    rs = self.cluster_apps.read_namespaced_replica_set(name=owner.name, namespace=ns)
                    for rs_owner in rs.metadata.owner_references:
                        if rs_owner.kind == "Deployment":
                            return "Deployment", rs_owner.name
                elif owner.kind == "StatefulSet":
                    # Directly return StatefulSet type and name
                    return "StatefulSet", owner.name

            return None, None  # No associated Deployment or StatefulSet found
        except Exception as e:
            print(f"Error fetching pod owner: {e}")
            return None, None