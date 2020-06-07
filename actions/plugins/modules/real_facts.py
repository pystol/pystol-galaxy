#!/usr/bin/python

"""
Copyright 2019 Pystol (pystol.org).

Licensed under the Apache License, Version 2.0 (the "License"); you may
not use this file except in compliance with the License. You may obtain
a copy of the License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations
under the License.
"""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: real_facts

short_description: A module that dishes out the true facts.

version_added: "2.8"

description:
    - "A module that dishes out the true facts."

options:
    name:
        default: Jane Doe

author:
    - "Carlos Camacho (@ccamacho)"
'''

EXAMPLES = '''
# Pass in a message
- name: Test with a message
  real_facts:
    name: David Newswanger
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


import random
from ansible.module_utils.basic import AnsibleModule


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='str', default='Jane Doe'),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    result = dict(
        changed=False,
        fact=''
    )

    result['fact'] = random.choice(FACTS).format(
        name=module.params['name']
    )

    if module.check_mode:
        return result

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
