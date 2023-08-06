#!/usr/bin/python
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

DOCUMENTATION = '''
---
module: zuul_deps
version_added: "2.0"
short_description: Transforms the dependent changes variable from Zuul format into a dictionary
description:
    - Transforms the dependent changes variable from Zuul format into a dictionary
options:
  host:
    description:
      - The content of the ZUUL_URL variable
    required: True
  changes:
    description:
      - The content of the ZUUL_CHANGES variable
    required: True
  branch:
    description:
      - Which branch to transform dependent changes on.
    default: None
'''

EXAMPLES = '''
- zuul_deps:
    host: https://review.openstack.org
    changes: "openstack/tripleo-heat-templates:master:refs/changes/88/296488/1^openstack/instack-undercloud:master:refs/changes/84/315184/5"
'''


def process(host, changes, branch):
    """Process the changes from Zuul format"""
    output = []

    for item in reversed(changes.split("^")):
        params = item.split(":")
        if branch and branch != params[1]:
            continue
        if params[0] in [i['project'] for i in output]:
            continue
        # https://bugs.launchpad.net/tripleo/+bug/1676853
        if '.openstack.org' in host:
            host = 'https://git.openstack.org'
        # add URL prefix if only the bare hostname is given
        if host.find('://') == -1:
            host = ''.join(['https://', host])
        output.append({"host": host,
                       "project": params[0],
                       "branch": params[1],
                       "refspec": params[2]})
    return {'changed': True,
            'ansible_facts': {'zuul_change_list': output}}


def main():
    module = AnsibleModule(
        argument_spec=dict(
            host=dict(required=True, type='str'),
            changes=dict(required=True, type='str'),
            branch=dict(default=None, type='str')
        )
    )
    result = process(module.params['host'],
                     module.params['changes'],
                     module.params['branch'])
    module.exit_json(**result)


# see http://docs.ansible.com/developing_modules.html#common-module-boilerplate
from ansible.module_utils.basic import *

if __name__ == "__main__":
    main()
