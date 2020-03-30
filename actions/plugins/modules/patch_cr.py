from ansible.module_utils.basic import AnsibleModule
import sys
from kubernetes import client
from kubernetes.client.rest import ApiException

from ansible_collections.pystol.actions.plugins.module_utils.k8s_common import load_kubernetes_config

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: patch_cr

short_description: A module that patch a cr to update its values.

version_added: "2.8"

description:
    - "A module that patch a cr to update its values."

options:
    name:
        default: ''
    key:
        default: ''
    value:
        default: ''

author:
    - Carlos Camacho
'''

EXAMPLES = '''
# Pass in a message
- name: Test with a message
  patch_cr:
    name: pystol-action-jhgyt
    key: workflow_state
    value: PystolActionEnded
'''

RETURN = '''
fact:
    description: Actual facts
    type: str
    sample: Jane Doe is a smart cookie.
'''


def patch_cr(name, key, value):
    custom_api = client.CustomObjectsApi()

    # First we fetch the custom object.
    group = "pystol.org"
    version = "v1alpha1"
    namespace = "pystol"
    plural = "pystolactions"
    try:
        obj = custom_api.get_namespaced_custom_object(
            group=group,
            version=version,
            namespace=namespace,
            plural=plural,
            name=name)
    except ApiException as e:
        print("Object do not exist: %s\n" % e)

    obj["spec"][key] = value

    # Then we replace it in the cluster.
    try:
        custom_api.replace_namespaced_custom_object(
            group=group,
            version=version,
            namespace=namespace,
            plural=plural,
            name=name,
            body=obj)
    except ApiException as e:
        print("Problem patching object: %s\n" % e)


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='str', required=True),
        key=dict(type='str', required=True),
        value=dict(type='str', required=True),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    out = ""
    err = ""
    rc = 0

    load_kubernetes_config()
    configuration = client.Configuration()
    configuration.assert_hostname = False
    client.api_client.ApiClient(configuration=configuration)

    module.log(msg='test!!!!!!!!!!!!!!!!!')

    name = module.params['name']
    key = module.params['key']
    value = module.params['value']

    result = dict(
        changed=True,
        stdout=out,
        stderr=err,
        rc=rc,
    )

    patch_cr(name, key, value)

    if module.check_mode:
        return result

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
