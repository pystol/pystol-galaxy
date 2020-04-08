#!/usr/bin/python


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: drain_nodes

short_description: A module that drain nodes

version_added: "2.8"

description:
    - "A module that drain nodes"

options:
    nodes:
        default: default
    amount:
        default: 10
    duration:
        default: 60

author:
    - "Carlos Camacho (@ccamacho)"
'''

EXAMPLES = '''
# Pass in a message
- name: Test with a message
  drain_nodes:
    nodes: ["minikube", "worker1"]
    amount: 3
    duration: 60
'''

RETURN = '''
fact:
    description: Actual facts
    type: str
    sample: Jane Doe is a smart cookie.
'''

FACTS = [
    "{name} is looking great today!",
    "{name} is a smart cookie.",
    "I’d choose {name}'s company over pizza anytime."
]


from ansible.module_utils.basic import AnsibleModule
from kubernetes import client
from kubernetes.client.rest import ApiException

import time
import json
from random import sample

from ansible_collections.pystol.actions.plugins.module_utils.k8s_common import load_kubernetes_config
from ansible_collections.pystol.actions.plugins.module_utils.logger import get_logger


def evict_pod(name, namespace):
    """
    Evict a pod from a node.

    This method evicts a single pod from a node
    """
    logger = get_logger("evict_pod")
    api_instance = client.CoreV1Api()

    ev = client.V1beta1Eviction()
    ev.metadata = client.V1ObjectMeta()
    ev.metadata.name = name
    ev.metadata.namespace = namespace
    ev.delete_options = client.V1DeleteOptions()

    try:
        api_instance.create_namespaced_pod_eviction(
            name=name, namespace=namespace, body=ev)
    except Exception as e:
        logger.debug(e)
        raise Exception("Failed to evict pod " +
                        name + ": " + e)


def cordon_node(name):
    """
    Cordon a node from the cluster.

    This method set a node as unschedulable
    """
    logger = get_logger("cordon_node")
    core_v1 = client.CoreV1Api()
    body = {"spec": {"unschedulable": True}}
    try:
        core_v1.patch_node(name=name, body=body)
        return True
    except Exception as e:
        logger.debug("Error: " + e)
        return False


def uncordon_node(name):
    """
    Uncordon a node from the cluster.

    This method set a node as schedulable
    """
    logger = get_logger("uncordon_node")
    core_v1 = client.CoreV1Api()
    body = {"spec": {"unschedulable": False}}
    try:
        core_v1.patch_node(name=name, body=body)
        return True
    except Exception as e:
        logger.debug("Error: " + e)
        return False


def get_pods(node_name):
    """
    Get the pods of a specific node.

    This method get the pods of a node
    """
    logger = get_logger("get_pods")
    api_instance = client.CoreV1Api()
    try:
        api_response = api_instance.list_pod_for_all_namespaces(
            field_selector="spec.nodeName={}".format(node_name))
        return api_response
    except ApiException as e:
        logger.debug("Error: " + e)
        print("CoreV1Api->list_pod_for_all_namespaces: %s\n" % e)


def get_worker_nodes():
    """
    Get all the workers from the cluster.

    This method get the worker nodes
    """
    logger = get_logger("get_worker_nodes")
    api_instance = client.CoreV1Api()
    try:
        names = []
        resp = api_instance.list_node(pretty='true',
                                      label_selector='node-role.kubernetes.io/worker')
        for node in resp.items:
            names.append(node.metadata.name)
        return names
    except ApiException as e:
        logger.debug("Error: " + e)
        print("CoreV1Api->list_node: %s\n" % e)


def calc_evict_list(pod_list):
    """
    Calculate eviction list.

    This method calculates the pods to remove
    """
    logger = get_logger("calc_evict_list")
    delete_pods_with_local_storage = False
    to_evict = []
    for pod in pod_list:
        name = pod.metadata.name
        phase = pod.status.phase
        volumes = pod.spec.volumes
        annotations = pod.metadata.annotations

        logger.debug("Checking POD: " + name)

        if annotations and "kubernetes.io/config.mirror" in annotations:
            logger.debug("Not deleting, mirror pod: " + name)
            continue

        if any(filter(lambda v: v.empty_dir is not None, volumes)):
            logger.debug("Pod " + name +
                         " has a volume made of a local storage")
            if not delete_pods_with_local_storage:
                logger.debug("Not evicting a pod with local storage")
                continue
            to_evict.append(pod)
            continue

        if phase in ["Succeeded", "Failed"]:
            to_evict.append(pod)
            continue

        for owner in pod.metadata.owner_references:
            if owner.controller and owner.kind != "DaemonSet":
                to_evict.append(pod)
                break
            elif owner.kind == "DaemonSet":
                logger.debug("Pod " + name + "is owned by a DaemonSet")
                break
        else:
            raise Exception(
                "Pod " + name + " is unmanaged, "
                "can not drain. Delete it manually")
    return to_evict


def drain_node(node_name):
    """
    Drain a node from all the possible pods.

    This method will drain a node
    """
    logger = get_logger("drain_node")
    logger.debug("Starting to drain: " + node_name)
    # We get all the pods from the node
    ret = get_pods(node_name)
    # Now we will try to remove as much pods as we can
    to_evict = calc_evict_list(ret.items)
    if not to_evict:
        logger.debug("No pods to remove from node.")
        return True
    logger.debug("Found " + str(len(to_evict)) + "pods to evict")
    for pod in to_evict:
        evict_pod(name=pod.metadata.name,
                  namespace=pod.metadata.namespace)
    pods = to_evict[:]
    started = time.time()
    timeout = 180
    api_instance = client.CoreV1Api()
    while True:
        logger.debug("Waiting for " + str(len(pods)) + "pods to go")
        if time.time() - started > timeout:
            remaining_pods = "\n".join([p.metadata.name for p in pods])
            raise Exception(
                "Draining nodes did not completed within " + timeout + "s."
                "Remaining pods are: " + remaining_pods)
        pending_pods = pods[:]
        for pod in pods:
            try:
                p = api_instance.read_namespaced_pod(
                    pod.metadata.name, pod.metadata.namespace)
                if p.metadata.uid != pod.metadata.uid:
                    pending_pods.remove(pod)
                    continue
                logger.debug("Pod " + p.metadata.name + " still around "
                             "in phase: " + p.status.phase)
            except ApiException as x:
                if x.status == 404:
                    pending_pods.remove(pod)
        pods = pending_pods[:]
        if not pods:
            logger.debug("Evicted all pods")
            break
        time.sleep(10)
    return True


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        nodes=dict(type='json', required=True),
        amount=dict(type='int', required=True),
        duration=dict(type='int', required=True),
    )

    global module
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    rc = 0
    stderr = "err"
    stderr_lines = ["errl1", "errl2"]
    stdout = "out"
    stdout_lines = ["outl1", "outl1"]

    nodes = module.params['nodes']
    amount = module.params['amount']
    duration = module.params['duration']

    result = dict(
        changed=True,
        stdout=stdout,
        stdout_lines=stdout_lines,
        stderr=stderr,
        stderr_lines=stderr_lines,
        rc=rc,
    )

    # Load the Kubernetes configuration
    load_kubernetes_config()
    configuration = client.Configuration()
    configuration.assert_hostname = False
    client.api_client.ApiClient(configuration=configuration)

    nodes_list = json.loads(nodes)
    module.log(msg='Nodes list size:' + str(len(nodes_list)))

    # We get the final list of nodes to drain
    all_workers = get_worker_nodes()
    if len(nodes_list) == 0:
        # This means that there are no specific nodes, get get random nodes
        module.log(msg='Nodes list is empty, we get random nodes')
        if amount >= len(all_workers):
            amount = len(all_workers)
        nodes_list = sample(all_workers, amount)
    else:
        aux_nodes = []
        for node in nodes_list:
            if node in all_workers:
                aux_nodes.append(node)
        nodes_list = aux_nodes

    module.log(msg='Nodes to drain: ' + str(nodes_list))

    # We cordon the nodes and drain them
    for node_name in nodes_list:
        module.log(msg='Node to cordon:' + node_name)
        if cordon_node(node_name):
            module.log(msg='Cordon OK - Node to drain:' + node_name)
            drain_node(node_name)
        else:
            module.log(msg='Cordon NOT OK')

    # We wait until the duration pass
    module.log(msg='Waiting for: ' + str(duration))
    time.sleep(duration)

    # We restore the nodes
    for node_name in nodes_list:
        module.log(msg='Node to uncordon:' + node_name)
        if uncordon_node(node_name):
            module.log(msg='Uncordon OK')
        else:
            module.log(msg='Uncordon NOT OK')

    if module.check_mode:
        return result

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
