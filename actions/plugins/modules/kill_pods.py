import matplotlib
matplotlib.use('Agg')
import random
from ansible.module_utils.basic import AnsibleModule
from scipy.stats import poisson
import matplotlib.pyplot as plt
from kubernetes import client, config
from kubernetes.client.rest import ApiException
import datetime

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: kill_pods

short_description: A module that kill pods

version_added: "2.8"

description:
    - "A module that kill pods."

options:
    namespace:
        default: default
    distribution:
        default: poisson
    amount:
        default: 10

author:
    - Carlos Camacho
'''

EXAMPLES = '''
# Pass in a message
- name: Test with a message
  kill_pods:
    namespace: default
    distribution: poisson
    amount: 10
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


global_available = []
global_unavailable = []
global_kill = []


def delete_pod(name, namespace):
    core_v1 = client.CoreV1Api()
    delete_options = client.V1DeleteOptions()
    try:
        core_v1.delete_namespaced_pod(
            name=name,
            namespace=namespace,
            body=delete_options)
    except ApiException as e:
        print("CoreV1Api->delete_namespaced_pod: %s\n" % e)


def get_pods(namespace=''):
    api_instance = client.CoreV1Api()
    try:
        if namespace == '':
            api_response = api_instance.list_pod_for_all_namespaces()
        else:
            api_response = api_instance.list_namespaced_pod(
                namespace,
                field_selector='status.phase=Running')
        return api_response
    except ApiException as e:
        print("CoreV1Api->list_pod_for_all_namespaces: %s\n" % e)


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        namespace=dict(type='str', default='default'),
        distribution=dict(type='str', default='poisson'),
        amount=dict(type='int', default=10),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    out = ""
    err = ""

    namespace = module.params['namespace']
    amount = module.params['amount']

    result = dict(
        changed=True,
        stdout=out,
        stderr=err,
    )

    result['fact'] = random.choice(FACTS).format(
        name=module.params['namespace']
    )

    # random numbers from poisson distribution
    n = amount
    a = 0
    data_poisson = poisson.rvs(mu=10, size=n, loc=a)
    counts, bins, bars = plt.hist(data_poisson)
    plt.close()
    config.load_kube_config()
    configuration = client.Configuration()
    configuration.assert_hostname = False
    client.api_client.ApiClient(configuration=configuration)
    for experiment in counts:
        pod_list = get_pods(namespace=namespace)
        aux_li = []
        for fil in pod_list.items:
            if fil.status.phase == "Running":
                aux_li.append(fil)
        pod_list = aux_li

        # From the Running pods I randomly choose those to die
        # based on the histogram length
        print("-------")
        print("Pod list length: " + str(len(pod_list)))
        print("Number of pods to get: " + str(int(experiment)))
        print("-------")
        # In the case of the experiment being longer than the pod list,
        # then the maximum will be the lenght of the pod list
        if (int(experiment) > len(pod_list)):
            to_be_killed = random.sample(pod_list, len(pod_list))
        else:
            to_be_killed = random.sample(pod_list, int(experiment))

        for pod in to_be_killed:
            delete_pod(pod.metadata.name,
                       pod.metadata.namespace)
        print("To be killed: " + str(experiment))
        global_kill.append((datetime.datetime.now(), int(experiment)))
        print(datetime.datetime.now())
    print("Ending histogram execution")

    if module.check_mode:
        return result

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
