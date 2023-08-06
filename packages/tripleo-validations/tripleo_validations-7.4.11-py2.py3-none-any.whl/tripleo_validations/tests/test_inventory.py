# -*- coding: utf-8 -*-

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from heatclient.exc import HTTPNotFound
from mock import MagicMock

from tripleo_validations.inventory import StackOutputs
from tripleo_validations.inventory import TripleoInventory
from tripleo_validations.tests import base


MOCK_ENABLED_SERVICES = {
    "ObjectStorage": [
        "kernel",
        "swift_storage",
        "tripleo_packages"
    ],
    "Controller": [
        "kernel",
        "keystone",
        "tripleo_packages"
    ],
    "Compute": [
        "nova_compute",
        "kernel",
        "tripleo_packages"
    ],
    "CephStorage": [
        "kernel",
        "tripleo_packages"
    ],
    "BlockStorage": [
        "cinder_volume",
        "kernel",
        "tripleo_packages"
    ]
}


class TestInventory(base.TestCase):
    def setUp(self):
        super(TestInventory, self).setUp()
        self.outputs_data = {'outputs': [
            {'output_key': 'EnabledServices',
             'output_value': {
                 'Controller': ['a', 'b', 'c'],
                 'Compute': ['d', 'e', 'f'],
                 'CustomRole': ['g', 'h', 'i']}},
            {'output_key': 'KeystoneURL',
             'output_value': 'xyz://keystone'},
            {'output_key': 'ServerIdData',
             'output_value': {
                 'server_ids': {
                     'Controller': ['a', 'b', 'c'],
                     'Compute': ['d'],
                     'CustomRole': ['e']},
                 'bootstrap_server_id': 'a'}},
            {'output_key': 'RoleNetHostnameMap',
             'output_value': {
                 'Controller': {
                     'ctlplane': ['c-0.ctlplane.localdomain',
                                  'c-1.ctlplane.localdomain',
                                  'c-2.ctlplane.localdomain']},
                 'Compute': {
                     'ctlplane': ['cp-0.ctlplane.localdomain']},
                 'CustomRole': {
                     'ctlplane': ['cs-0.ctlplane.localdomain']}}},
            {'output_key': 'RoleNetIpMap',
             'output_value': {
                 'Controller': {
                     'ctlplane': ['x.x.x.1',
                                  'x.x.x.2',
                                  'x.x.x.3']},
                 'Compute': {
                     'ctlplane': ['y.y.y.1']},
                 'CustomRole': {
                     'ctlplane': ['z.z.z.1']}}}]}
        self.plan_name = 'overcloud'

        self.hclient = MagicMock()
        self.hclient.stacks.environment.return_value = {
            'parameter_defaults': {'AdminPassword': 'theadminpw'}}
        self.mock_stack = MagicMock()
        self.mock_stack.outputs = self.outputs_data['outputs']
        self.hclient.stacks.get.return_value = self.mock_stack

        self.configs = MagicMock()
        self.configs.plan = self.plan_name
        self.configs.auth_url = 'xyz://keystone.local'
        self.configs.cacert = 'acacert'
        self.configs.project_name = 'admin'
        self.configs.username = 'admin'
        self.configs.ansible_ssh_user = 'heat-admin'

        self.session = MagicMock()
        self.session.get_token.return_value = 'atoken'
        self.session.get_endpoint.return_value = 'anendpoint'

        self.outputs = StackOutputs('overcloud', self.hclient)
        self.inventory = TripleoInventory(
            self.configs, self.session, self.hclient)
        self.inventory.stack_outputs = self.outputs

    def test_get_roles_by_service(self):
        services = TripleoInventory.get_roles_by_service(
            MOCK_ENABLED_SERVICES)
        expected = {
            'kernel': ['BlockStorage', 'CephStorage', 'Compute', 'Controller',
                       'ObjectStorage'],
            'swift_storage': ['ObjectStorage'],
            'tripleo_packages': ['BlockStorage', 'CephStorage', 'Compute',
                                 'Controller', 'ObjectStorage'],
            'keystone': ['Controller'],
            'nova_compute': ['Compute'],
            'cinder_volume': ['BlockStorage'],
        }
        self.assertDictEqual(services, expected)

    def test_outputs_are_empty_if_stack_doesnt_exist(self):
        self.hclient.stacks.get.side_effect = HTTPNotFound('not found')
        stack_outputs = StackOutputs('no-plan', self.hclient)
        self.assertEqual(list(stack_outputs), [])

    def test_outputs_valid_key_calls_api(self):
        expected = 'xyz://keystone'
        self.hclient.stacks.output_show.return_value = dict(output=dict(
            output_value=expected))
        self.assertEqual(expected, self.outputs['KeystoneURL'])
        # This should also support the get method
        self.assertEqual(expected, self.outputs.get('KeystoneURL'))
        self.assertTrue(self.hclient.called_once_with('overcloud',
                                                      'KeystoneURL'))

    def test_outputs_invalid_key_raises_keyerror(self):
        self.assertRaises(KeyError, lambda: self.outputs['Invalid'])

    def test_outputs_get_method_returns_default(self):
        default = 'default value'
        self.assertEqual(default, self.outputs.get('Invalid', default))

    def test_outputs_iterating_returns_list_of_output_keys(self):
        self.assertEqual(
            {'EnabledServices', 'KeystoneURL', 'ServerIdData',
             'RoleNetHostnameMap', 'RoleNetIpMap'},
            set([o for o in self.outputs]))

    def test_inventory_list(self):
        expected = {'c-0': {'hosts': ['x.x.x.1'],
                            'vars': {'deploy_server_id': 'a'}},
                    'c-1': {'hosts': ['x.x.x.2'],
                            'vars': {'deploy_server_id': 'b'}},
                    'c-2': {'hosts': ['x.x.x.3'],
                            'vars': {'deploy_server_id': 'c'}},
                    'Compute': {
                        'children': ['cp-0'],
                        'vars': {'ansible_ssh_user': 'heat-admin',
                                 'bootstrap_server_id': 'a',
                                 'role_name': 'Compute'}},
                    'Controller': {
                        'children': ['c-0', 'c-1', 'c-2'],
                        'vars': {'ansible_ssh_user': 'heat-admin',
                                 'bootstrap_server_id': 'a',
                                 'role_name': 'Controller'}},
                    'cp-0': {'hosts': ['y.y.y.1'],
                             'vars': {'deploy_server_id': 'd'}},
                    'cs-0': {'hosts': ['z.z.z.1'],
                             'vars': {'deploy_server_id': 'e'}},
                    'CustomRole': {
                        'children': ['cs-0'],
                        'vars': {'ansible_ssh_user': 'heat-admin',
                                 'bootstrap_server_id': 'a',
                                 'role_name': 'CustomRole'}},
                    'overcloud': {
                        'children': ['Compute', 'Controller', 'CustomRole']},
                    'undercloud': {
                        'hosts': ['localhost'],
                        'vars': {'ansible_connection': 'local',
                                 'auth_url': 'xyz://keystone.local',
                                 'cacert': 'acacert',
                                 'os_auth_token': 'atoken',
                                 'overcloud_keystone_url': 'xyz://keystone',
                                 'overcloud_admin_password': 'theadminpw',
                                 'plan': 'overcloud',
                                 'project_name': 'admin',
                                 'undercloud_service_list': [
                                     'openstack-nova-compute',
                                     'openstack-heat-engine',
                                     'openstack-ironic-conductor',
                                     'openstack-swift-container',
                                     'openstack-swift-object',
                                     'openstack-mistral-engine'],
                                 'undercloud_swift_url': 'anendpoint',
                                 'username': 'admin'}}}
        inv_list = self.inventory.list()
        for k in expected:
            self.assertEqual(expected[k], inv_list[k])

    def test_ansible_ssh_user(self):
        self.configs.ansible_ssh_user = 'my-custom-admin'
        self.inventory = TripleoInventory(
            self.configs, self.session, self.hclient)
        self.inventory.stack_outputs = self.outputs

        expected = {'c-0': {'hosts': ['x.x.x.1'],
                            'vars': {'deploy_server_id': 'a'}},
                    'c-1': {'hosts': ['x.x.x.2'],
                            'vars': {'deploy_server_id': 'b'}},
                    'c-2': {'hosts': ['x.x.x.3'],
                            'vars': {'deploy_server_id': 'c'}},
                    'Compute': {
                        'children': ['cp-0'],
                        'vars': {'ansible_ssh_user': 'my-custom-admin',
                                 'bootstrap_server_id': 'a',
                                 'role_name': 'Compute'}},
                    'Controller': {
                        'children': ['c-0', 'c-1', 'c-2'],
                        'vars': {'ansible_ssh_user': 'my-custom-admin',
                                 'bootstrap_server_id': 'a',
                                 'role_name': 'Controller'}},
                    'cp-0': {'hosts': ['y.y.y.1'],
                             'vars': {'deploy_server_id': 'd'}},
                    'cs-0': {'hosts': ['z.z.z.1'],
                             'vars': {'deploy_server_id': 'e'}},
                    'CustomRole': {
                        'children': ['cs-0'],
                        'vars': {'ansible_ssh_user': 'my-custom-admin',
                                 'bootstrap_server_id': 'a',
                                 'role_name': 'CustomRole'}},
                    'overcloud': {
                        'children': ['Compute', 'Controller', 'CustomRole']},
                    'undercloud': {
                        'hosts': ['localhost'],
                        'vars': {'ansible_connection': 'local',
                                 'auth_url': 'xyz://keystone.local',
                                 'cacert': 'acacert',
                                 'os_auth_token': 'atoken',
                                 'overcloud_keystone_url': 'xyz://keystone',
                                 'overcloud_admin_password': 'theadminpw',
                                 'plan': 'overcloud',
                                 'project_name': 'admin',
                                 'undercloud_service_list': [
                                     'openstack-nova-compute',
                                     'openstack-heat-engine',
                                     'openstack-ironic-conductor',
                                     'openstack-swift-container',
                                     'openstack-swift-object',
                                     'openstack-mistral-engine'],
                                 'undercloud_swift_url': 'anendpoint',
                                 'username': 'admin'}}}

        inv_list = self.inventory.list()
        for k in expected:
            self.assertEqual(expected[k], inv_list[k])
