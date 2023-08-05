# Copyright 2016 Futurewei. All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import time

from tempest.common import waiters
from tempest import config
from tempest.lib.common.utils import test_utils
from tempest.lib import decorators
from tempest import test
import testscenarios

from networking_sfc.tests.tempest_plugin.tests.scenario import base

CONF = config.CONF
load_tests = testscenarios.load_tests_apply_scenarios


class TestSfc(base.SfcScenarioTest):
    @classmethod
    def skip_checks(cls):
        super(TestSfc, cls).skip_checks()
        if not (CONF.network.project_networks_reachable
                or CONF.network.public_network_id):
            msg = ('Either project_networks_reachable must be "true", or '
                   'public_network_id must be defined.')
            raise cls.skipException(msg)
        required_exts = ['sfc', 'flow_classifier']
        for ext in required_exts:
            if not test.is_extension_enabled(ext, 'network'):
                msg = "%s Extension not enabled." % ext
                raise cls.skipException(msg)

    @classmethod
    def setup_credentials(cls):
        # Create no network resources for these tests.
        cls.set_network_resources()
        super(TestSfc, cls).setup_credentials()

    def _setup_security_group(self):
        self.security_group = self._create_security_group()
        self._create_security_group_rule(
            self.security_group, protocol=None,
            direction='ingress'
        )

    def setUp(self):
        super(TestSfc, self).setUp()
        self.ssh_user = CONF.validation.image_ssh_user
        self.keypair = self.create_keypair()
        self._setup_security_group()
        self.net1, self.subnet1, self.router1 = self.create_networks()
        self.router2 = self._create_router()
        self.router3 = self._create_router()
        self.router2_net1 = self._create_port(self.net1['id'])
        self._add_router_interface(
            self.router2['id'], self.router2_net1['id'])
        self.router3_net1 = self._create_port(self.net1['id'])
        self._add_router_interface(
            self.router3['id'], self.router3_net1['id'])
        self.router2_net1_fixed_ip = self.router2_net1[
            'fixed_ips'][0]['ip_address']
        self.router3_net1_fixed_ip = self.router3_net1[
            'fixed_ips'][0]['ip_address']

    def _setup_server(self, network):
        server = self._create_server(network=self.net1)
        floating_ip = self._create_floating_ip(
            server)
        port_id, fixed_ip = (
            self._get_server_port_id_and_ip4(server))
        return floating_ip, port_id, fixed_ip

    def _create_floating_ip(self, server):
        floating_ip = self.create_floating_ip(
            server)
        self.check_floating_ip_status(floating_ip, 'ACTIVE')
        floating_ip_addr = floating_ip['floating_ip_address']
        self.check_public_network_connectivity(
            floating_ip_addr, self.ssh_user,
            self.keypair['private_key'], True,
            servers=[server])
        return floating_ip_addr

    def _wait_for_port_chain_status(self, port_chain, status):
        time.sleep(10)

    def _create_port_chain_helper(self, symmetric):
        (
            server1_floating_ip, server1_port_id, server1_fixed_ip
        ) = self._setup_server(self.net1)
        (
            server2_floating_ip, server2_port_id, server2_fixed_ip
        ) = self._setup_server(self.net1)
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        if symmetric:
            fc = self._create_flowclassifier(
                logical_source_port=server1_port_id,
                source_ip_prefix='%s/32' % server1_fixed_ip,
                logical_destination_port=server2_port_id,
                destination_ip_prefix='%s/32' % server2_fixed_ip
            )
        else:
            fc = self._create_flowclassifier(
                logical_source_port=server1_port_id,
                source_ip_prefix='%s/32' % server1_fixed_ip,
                destination_ip_prefix='%s/32' % server2_fixed_ip
            )
        port_pair = self._create_port_pair(
            ingress=self.router2_net1['id'],
            egress=self.router2_net1['id']
        )
        port_pair_group = self._create_port_pair_group(
            port_pairs=[port_pair['id']]
        )
        port_chain = self._create_port_chain(
            port_pair_groups=[port_pair_group['id']],
            flow_classifiers=[fc['id']],
            chain_parameters={'symmetric': symmetric}
        )
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [[self.router2_net1_fixed_ip]],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        self.portchain_client.delete_port_chain(port_chain['id'])
        self._wait_for_port_chain_status(port_chain, 'DELETED')
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])

    @decorators.idempotent_id('f970f6b3-6541-47ac-a9ea-f769be1e21a8')
    @test.services('compute', 'network')
    def test_create_port_chain(self):
        self._create_port_chain_helper(False)

    @decorators.idempotent_id('35927961-1904-4a6b-9d08-ad819f1cf812')
    @test.services('compute', 'network')
    def test_create_port_chain_symmetric(self):
        self._create_port_chain_helper(True)

    def _create_port_chain_multi_fc_helper(self, symmetric):
        (
            server1_floating_ip, server1_port_id, server1_fixed_ip
        ) = self._setup_server(self.net1)
        (
            server2_floating_ip, server2_port_id, server2_fixed_ip
        ) = self._setup_server(self.net1)
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        self._check_connectivity(
            server2_floating_ip, server1_fixed_ip,
            [],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        if symmetric:
            fc1 = self._create_flowclassifier(
                logical_source_port=server1_port_id,
                source_ip_prefix='%s/32' % server1_fixed_ip,
                logical_destination_port=server2_port_id,
                destination_ip_prefix='%s/32' % server2_fixed_ip
            )
            fc2 = self._create_flowclassifier(
                logical_source_port=server2_port_id,
                source_ip_prefix='%s/32' % server2_fixed_ip,
                logical_destination_port=server1_port_id,
                destination_ip_prefix='%s/32' % server1_fixed_ip
            )
        else:
            fc1 = self._create_flowclassifier(
                logical_source_port=server1_port_id,
                source_ip_prefix='%s/32' % server1_fixed_ip,
                destination_ip_prefix='%s/32' % server2_fixed_ip
            )
            fc2 = self._create_flowclassifier(
                logical_source_port=server2_port_id,
                source_ip_prefix='%s/32' % server2_fixed_ip,
                destination_ip_prefix='%s/32' % server1_fixed_ip
            )
        port_pair = self._create_port_pair(
            ingress=self.router2_net1['id'],
            egress=self.router2_net1['id']
        )
        port_pair_group = self._create_port_pair_group(
            port_pairs=[port_pair['id']]
        )
        port_chain = self._create_port_chain(
            port_pair_groups=[port_pair_group['id']],
            flow_classifiers=[fc1['id'], fc2['id']],
            chain_parameters={'symmetric': symmetric}
        )
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [[self.router2_net1_fixed_ip]],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        self._check_connectivity(
            server2_floating_ip, server1_fixed_ip,
            [[self.router2_net1_fixed_ip]],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        self.portchain_client.delete_port_chain(port_chain['id'])
        self._wait_for_port_chain_status(port_chain, 'DELETED')
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        self._check_connectivity(
            server2_floating_ip, server1_fixed_ip,
            [],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])

    @decorators.idempotent_id('f970f6b3-6541-47ac-a9ea-f769be1e21a9')
    @test.services('compute', 'network')
    def test_create_port_chain_multi_flow_classifiers(self):
        self._create_port_chain_multi_fc_helper(False)

    @decorators.idempotent_id('f970f6b3-6541-47ac-a9ea-f769be1e21b1')
    @test.services('compute', 'network')
    def test_create_port_chain_multi_flow_classifiers_symmetric(self):
        self._create_port_chain_multi_fc_helper(True)

    def _create_port_chain_multi_port_pairs_helper(self, symmetric):
        (
            server1_floating_ip, server1_port_id, server1_fixed_ip
        ) = self._setup_server(self.net1)
        (
            server2_floating_ip, server2_port_id, server2_fixed_ip
        ) = self._setup_server(self.net1)
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        if symmetric:
            fc = self._create_flowclassifier(
                logical_source_port=server1_port_id,
                source_ip_prefix='%s/32' % server1_fixed_ip,
                logical_destination_port=server2_port_id,
                destination_ip_prefix='%s/32' % server2_fixed_ip
            )
        else:
            fc = self._create_flowclassifier(
                logical_source_port=server1_port_id,
                source_ip_prefix='%s/32' % server1_fixed_ip,
                destination_ip_prefix='%s/32' % server2_fixed_ip
            )
        port_pair1 = self._create_port_pair(
            ingress=self.router2_net1['id'],
            egress=self.router2_net1['id']
        )
        port_pair2 = self._create_port_pair(
            ingress=self.router3_net1['id'],
            egress=self.router3_net1['id']
        )
        port_pair_group = self._create_port_pair_group(
            port_pairs=[port_pair1['id'], port_pair2['id']]
        )
        port_chain = self._create_port_chain(
            port_pair_groups=[port_pair_group['id']],
            flow_classifiers=[fc['id']],
            chain_parameters={'symmetric': symmetric}
        )
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [[self.router2_net1_fixed_ip, self.router3_net1_fixed_ip]],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        self.portchain_client.delete_port_chain(port_chain['id'])
        self._wait_for_port_chain_status(port_chain, 'DELETED')
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])

    @decorators.idempotent_id('f970f6b3-6541-47ac-a9ea-f769be1e21aa')
    @test.services('compute', 'network')
    def test_create_port_chain_multi_port_pairs(self):
        self._create_port_chain_multi_port_pairs_helper(False)

    @decorators.idempotent_id('f970f6b3-6541-47ac-a9ea-f869be1e21ad')
    @test.services('compute', 'network')
    def test_create_port_chain_multi_port_pairs_symmetric(self):
        self._create_port_chain_multi_port_pairs_helper(True)

    def _create_port_chain_multi_ppg_helper(self, symmetric):
        (
            server1_floating_ip, server1_port_id, server1_fixed_ip
        ) = self._setup_server(self.net1)
        (
            server2_floating_ip, server2_port_id, server2_fixed_ip
        ) = self._setup_server(self.net1)
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        if symmetric:
            fc = self._create_flowclassifier(
                logical_source_port=server1_port_id,
                source_ip_prefix="%s/32" % server1_fixed_ip,
                logical_destination_port=server2_port_id,
                destination_ip_prefix="%s/32" % server2_fixed_ip
            )
        else:
            fc = self._create_flowclassifier(
                logical_source_port=server1_port_id,
                source_ip_prefix="%s/32" % server1_fixed_ip,
                destination_ip_prefix="%s/32" % server2_fixed_ip
            )
        port_pair1 = self._create_port_pair(
            ingress=self.router2_net1['id'],
            egress=self.router2_net1['id']
        )
        port_pair2 = self._create_port_pair(
            ingress=self.router3_net1['id'],
            egress=self.router3_net1['id']
        )
        port_pair_group1 = self._create_port_pair_group(
            port_pairs=[port_pair1['id']]
        )
        port_pair_group2 = self._create_port_pair_group(
            port_pairs=[port_pair2['id']]
        )
        port_chain = self._create_port_chain(
            port_pair_groups=[port_pair_group1['id'], port_pair_group2['id']],
            flow_classifiers=[fc['id']],
            chain_parameters={'symmetric': symmetric}
        )
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [[self.router2_net1_fixed_ip], [self.router3_net1_fixed_ip]],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        self.portchain_client.delete_port_chain(port_chain['id'])
        self._wait_for_port_chain_status(port_chain, 'DELETED')
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])

    @decorators.idempotent_id('f970f6b3-6541-47ac-a9ea-f769be1e21ab')
    @test.services('compute', 'network')
    def test_create_port_chain_multi_port_pair_groups(self):
        self._create_port_chain_multi_ppg_helper(False)

    @decorators.idempotent_id('f970f6b3-6541-47ac-a9ea-f769be1e21b0')
    @test.services('compute', 'network')
    def test_create_port_chain_multi_port_pair_groups_symmetric(self):
        self._create_port_chain_multi_ppg_helper(True)

    @decorators.idempotent_id('f970f6b3-6541-47ac-a9ea-f769be1e22ab')
    @test.services('compute', 'network')
    def test_create_multi_port_chain(self):
        (
            server1_floating_ip, server1_port_id, server1_fixed_ip
        ) = self._setup_server(self.net1)
        (
            server2_floating_ip, server2_port_id, server2_fixed_ip
        ) = self._setup_server(self.net1)
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        fc1 = self._create_flowclassifier(
            logical_source_port=server1_port_id,
            source_ip_prefix='%s/32' % server1_fixed_ip,
            destination_ip_prefix='%s/32' % server2_fixed_ip
        )
        fc2 = self._create_flowclassifier(
            logical_source_port=server2_port_id,
            source_ip_prefix='%s/32' % server2_fixed_ip,
            destination_ip_prefix='%s/32' % server1_fixed_ip
        )
        port_pair1 = self._create_port_pair(
            ingress=self.router2_net1['id'],
            egress=self.router2_net1['id']
        )
        port_pair2 = self._create_port_pair(
            ingress=self.router3_net1['id'],
            egress=self.router3_net1['id']
        )
        port_pair_group1 = self._create_port_pair_group(
            port_pairs=[port_pair1['id']]
        )
        port_pair_group2 = self._create_port_pair_group(
            port_pairs=[port_pair2['id']]
        )
        port_chain1 = self._create_port_chain(
            port_pair_groups=[port_pair_group1['id'], port_pair_group2['id']],
            flow_classifiers=[fc1['id']]
        )
        port_chain2 = self._create_port_chain(
            port_pair_groups=[port_pair_group2['id'], port_pair_group1['id']],
            flow_classifiers=[fc2['id']]
        )
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [[self.router2_net1_fixed_ip], [self.router3_net1_fixed_ip]],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        self._check_connectivity(
            server2_floating_ip, server1_fixed_ip,
            [[self.router3_net1_fixed_ip], [self.router2_net1_fixed_ip]],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        self.portchain_client.delete_port_chain(port_chain1['id'])
        self.portchain_client.delete_port_chain(port_chain2['id'])
        self._wait_for_port_chain_status(port_chain1, 'DELETED')
        self._wait_for_port_chain_status(port_chain2, 'DELETED')
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        self._check_connectivity(
            server2_floating_ip, server1_fixed_ip,
            [],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])

    @decorators.idempotent_id('f970f6b3-6541-47ac-a9ea-f769be1e21ac')
    @test.services('compute', 'network')
    def test_update_port_chain_add_flow_classifiers(self):
        (
            server1_floating_ip, server1_port_id, server1_fixed_ip
        ) = self._setup_server(self.net1)
        (
            server2_floating_ip, server2_port_id, server2_fixed_ip
        ) = self._setup_server(self.net1)
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        self._check_connectivity(
            server2_floating_ip, server1_fixed_ip,
            [],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        fc1 = self._create_flowclassifier(
            logical_source_port=server1_port_id,
            source_ip_prefix='%s/32' % server1_fixed_ip,
            destination_ip_prefix='%s/32' % server2_fixed_ip
        )
        fc2 = self._create_flowclassifier(
            logical_source_port=server2_port_id,
            source_ip_prefix='%s/32' % server2_fixed_ip,
            destination_ip_prefix='%s/32' % server1_fixed_ip
        )
        port_pair = self._create_port_pair(
            ingress=self.router2_net1['id'],
            egress=self.router2_net1['id']
        )
        port_pair_group = self._create_port_pair_group(
            port_pairs=[port_pair['id']]
        )
        port_chain = self._create_port_chain(
            port_pair_groups=[port_pair_group['id']],
            flow_classifiers=[fc1['id']]
        )
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [[self.router2_net1_fixed_ip]],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        self._check_connectivity(
            server2_floating_ip, server1_fixed_ip,
            [],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        self.portchain_client.update_port_chain(
            port_chain['id'], flow_classifiers=[fc1['id'], fc2['id']])
        self._wait_for_port_chain_status(port_chain, 'ACTIVE')
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [[self.router2_net1_fixed_ip]],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        self._check_connectivity(
            server2_floating_ip, server1_fixed_ip,
            [[self.router2_net1_fixed_ip]],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])

    @decorators.idempotent_id('f970f6b3-6541-47ac-a9ea-f769be1e21ad')
    @test.services('compute', 'network')
    def test_update_port_chain_remove_flow_classifiers(self):
        (
            server1_floating_ip, server1_port_id, server1_fixed_ip
        ) = self._setup_server(self.net1)
        (
            server2_floating_ip, server2_port_id, server2_fixed_ip
        ) = self._setup_server(self.net1)
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        self._check_connectivity(
            server2_floating_ip, server1_fixed_ip,
            [],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        fc1 = self._create_flowclassifier(
            logical_source_port=server1_port_id,
            source_ip_prefix='%s/32' % server1_fixed_ip,
            destination_ip_prefix='%s/32' % server2_fixed_ip
        )
        fc2 = self._create_flowclassifier(
            logical_source_port=server2_port_id,
            source_ip_prefix='%s/32' % server2_fixed_ip,
            destination_ip_prefix='%s/32' % server1_fixed_ip
        )
        port_pair = self._create_port_pair(
            ingress=self.router2_net1['id'],
            egress=self.router2_net1['id']
        )
        port_pair_group = self._create_port_pair_group(
            port_pairs=[port_pair['id']]
        )
        port_chain = self._create_port_chain(
            port_pair_groups=[port_pair_group['id']],
            flow_classifiers=[fc1['id'], fc2['id']]
        )
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [[self.router2_net1_fixed_ip]],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        self._check_connectivity(
            server2_floating_ip, server1_fixed_ip,
            [[self.router2_net1_fixed_ip]],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        self.portchain_client.update_port_chain(
            port_chain['id'], flow_classifiers=[fc1['id']])
        self._wait_for_port_chain_status(port_chain, 'ACTIVE')
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [[self.router2_net1_fixed_ip]],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        self._check_connectivity(
            server2_floating_ip, server1_fixed_ip,
            [],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])

    @decorators.idempotent_id('f970f6b3-6541-47ac-a9ea-f769be1e21ae')
    @test.services('compute', 'network')
    def test_update_port_chain_replace_flow_classifiers(self):
        (
            server1_floating_ip, server1_port_id, server1_fixed_ip
        ) = self._setup_server(self.net1)
        (
            server2_floating_ip, server2_port_id, server2_fixed_ip
        ) = self._setup_server(self.net1)
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        self._check_connectivity(
            server2_floating_ip, server1_fixed_ip,
            [],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        fc1 = self._create_flowclassifier(
            logical_source_port=server1_port_id,
            source_ip_prefix='%s/32' % server1_fixed_ip,
            destination_ip_prefix='%s/32' % server2_fixed_ip
        )
        fc2 = self._create_flowclassifier(
            logical_source_port=server2_port_id,
            source_ip_prefix='%s/32' % server2_fixed_ip,
            destination_ip_prefix='%s/32' % server1_fixed_ip
        )
        port_pair = self._create_port_pair(
            ingress=self.router2_net1['id'],
            egress=self.router2_net1['id']
        )
        port_pair_group = self._create_port_pair_group(
            port_pairs=[port_pair['id']]
        )
        port_chain = self._create_port_chain(
            port_pair_groups=[port_pair_group['id']],
            flow_classifiers=[fc1['id']]
        )
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [[self.router2_net1_fixed_ip]],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        self._check_connectivity(
            server2_floating_ip, server1_fixed_ip,
            [],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        self.portchain_client.update_port_chain(
            port_chain['id'], flow_classifiers=[fc2['id']])
        self._wait_for_port_chain_status(port_chain, 'DELETED')
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        self._check_connectivity(
            server2_floating_ip, server1_fixed_ip,
            [[self.router2_net1_fixed_ip]],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])

    @decorators.idempotent_id('f970f6b3-6541-47ac-a9ea-f769be1e21af')
    @test.services('compute', 'network')
    def test_update_port_chain_add_port_pair_groups(self):
        (
            server1_floating_ip, server1_port_id, server1_fixed_ip
        ) = self._setup_server(self.net1)
        (
            server2_floating_ip, server2_port_id, server2_fixed_ip
        ) = self._setup_server(self.net1)
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        self._check_connectivity(
            server2_floating_ip, server1_fixed_ip,
            [],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        fc = self._create_flowclassifier(
            logical_source_port=server1_port_id,
            source_ip_prefix='%s/32' % server1_fixed_ip,
            destination_ip_prefix='%s/32' % server2_fixed_ip
        )
        port_pair1 = self._create_port_pair(
            ingress=self.router2_net1['id'],
            egress=self.router2_net1['id']
        )
        port_pair2 = self._create_port_pair(
            ingress=self.router3_net1['id'],
            egress=self.router3_net1['id']
        )
        port_pair_group1 = self._create_port_pair_group(
            port_pairs=[port_pair1['id']]
        )
        port_pair_group2 = self._create_port_pair_group(
            port_pairs=[port_pair2['id']]
        )
        port_chain = self._create_port_chain(
            port_pair_groups=[port_pair_group1['id']],
            flow_classifiers=[fc['id']]
        )
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [[self.router2_net1_fixed_ip]],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        self.portchain_client.update_port_chain(
            port_chain['id'],
            port_pair_groups=[
                port_pair_group1['id'], port_pair_group2['id']
            ]
        )
        self._wait_for_port_chain_status(port_chain, 'ACTIVE')
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [[self.router2_net1_fixed_ip], [self.router3_net1_fixed_ip]],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])

    @decorators.idempotent_id('f970f6b3-6541-47ac-a9ea-f769be1e21bf')
    @test.services('compute', 'network')
    def test_update_port_chain_remove_port_pair_groups(self):
        (
            server1_floating_ip, server1_port_id, server1_fixed_ip
        ) = self._setup_server(self.net1)
        (
            server2_floating_ip, server2_port_id, server2_fixed_ip
        ) = self._setup_server(self.net1)
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        self._check_connectivity(
            server2_floating_ip, server1_fixed_ip,
            [],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        fc = self._create_flowclassifier(
            logical_source_port=server1_port_id,
            source_ip_prefix='%s/32' % server1_fixed_ip,
            destination_ip_prefix='%s/32' % server2_fixed_ip
        )
        port_pair1 = self._create_port_pair(
            ingress=self.router2_net1['id'],
            egress=self.router2_net1['id']
        )
        port_pair2 = self._create_port_pair(
            ingress=self.router3_net1['id'],
            egress=self.router3_net1['id']
        )
        port_pair_group1 = self._create_port_pair_group(
            port_pairs=[port_pair1['id']]
        )
        port_pair_group2 = self._create_port_pair_group(
            port_pairs=[port_pair2['id']]
        )
        port_chain = self._create_port_chain(
            port_pair_groups=[
                port_pair_group1['id'], port_pair_group2['id']
            ],
            flow_classifiers=[fc['id']]
        )
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [[self.router2_net1_fixed_ip], [self.router3_net1_fixed_ip]],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        self.portchain_client.update_port_chain(
            port_chain['id'],
            port_pair_groups=[
                port_pair_group1['id']
            ]
        )
        self._wait_for_port_chain_status(port_chain, 'ACTIVE')
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [[self.router2_net1_fixed_ip]],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])

    @decorators.idempotent_id('f970f6b3-6541-47ac-a9ea-f769be1e21be')
    @test.services('compute', 'network')
    def test_update_port_chain_replace_port_pair_groups(self):
        (
            server1_floating_ip, server1_port_id, server1_fixed_ip
        ) = self._setup_server(self.net1)
        (
            server2_floating_ip, server2_port_id, server2_fixed_ip
        ) = self._setup_server(self.net1)
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        self._check_connectivity(
            server2_floating_ip, server1_fixed_ip,
            [],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        fc = self._create_flowclassifier(
            logical_source_port=server1_port_id,
            source_ip_prefix='%s/32' % server1_fixed_ip,
            destination_ip_prefix='%s/32' % server2_fixed_ip
        )
        port_pair1 = self._create_port_pair(
            ingress=self.router2_net1['id'],
            egress=self.router2_net1['id']
        )
        port_pair2 = self._create_port_pair(
            ingress=self.router3_net1['id'],
            egress=self.router3_net1['id']
        )
        port_pair_group1 = self._create_port_pair_group(
            port_pairs=[port_pair1['id']]
        )
        port_pair_group2 = self._create_port_pair_group(
            port_pairs=[port_pair2['id']]
        )
        port_chain = self._create_port_chain(
            port_pair_groups=[
                port_pair_group1['id']
            ],
            flow_classifiers=[fc['id']]
        )
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [[self.router2_net1_fixed_ip]],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        self.portchain_client.update_port_chain(
            port_chain['id'],
            port_pair_groups=[
                port_pair_group2['id']
            ]
        )
        self._wait_for_port_chain_status(port_chain, 'ACTIVE')
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [[self.router3_net1_fixed_ip]],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])

    @decorators.idempotent_id('f970f6b3-6541-47ac-a9ea-f769be1e21bc')
    @test.services('compute', 'network')
    def test_update_port_chain_replace_port_pair_groups_flow_classifiers(self):
        (
            server1_floating_ip, server1_port_id, server1_fixed_ip
        ) = self._setup_server(self.net1)
        (
            server2_floating_ip, server2_port_id, server2_fixed_ip
        ) = self._setup_server(self.net1)
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        self._check_connectivity(
            server2_floating_ip, server1_fixed_ip,
            [],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        fc1 = self._create_flowclassifier(
            logical_source_port=server1_port_id,
            source_ip_prefix='%s/32' % server1_fixed_ip,
            destination_ip_prefix='%s/32' % server2_fixed_ip
        )
        fc2 = self._create_flowclassifier(
            logical_source_port=server2_port_id,
            source_ip_prefix='%s/32' % server2_fixed_ip,
            destination_ip_prefix='%s/32' % server1_fixed_ip
        )
        port_pair1 = self._create_port_pair(
            ingress=self.router2_net1['id'],
            egress=self.router2_net1['id']
        )
        port_pair2 = self._create_port_pair(
            ingress=self.router3_net1['id'],
            egress=self.router3_net1['id']
        )
        port_pair_group1 = self._create_port_pair_group(
            port_pairs=[port_pair1['id']]
        )
        port_pair_group2 = self._create_port_pair_group(
            port_pairs=[port_pair2['id']]
        )
        port_chain = self._create_port_chain(
            port_pair_groups=[
                port_pair_group1['id']
            ],
            flow_classifiers=[fc1['id']]
        )
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [[self.router2_net1_fixed_ip]],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        self._check_connectivity(
            server2_floating_ip, server1_fixed_ip,
            [],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        self.portchain_client.update_port_chain(
            port_chain['id'],
            port_pair_groups=[port_pair_group2['id']],
            flow_classifiers=[fc2['id']])
        self._wait_for_port_chain_status(port_chain, 'ACTIVE')
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        self._check_connectivity(
            server2_floating_ip, server1_fixed_ip,
            [[self.router3_net1_fixed_ip]],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])

    def _wait_for_port_pair_group_status(self, port_pair_group, status):
        time.sleep(10)

    @decorators.idempotent_id('f970f6b3-6541-47ac-a9ea-f769be1e21bb')
    @test.services('compute', 'network')
    def test_update_port_pair_group_add_port_pairs(self):
        (
            server1_floating_ip, server1_port_id, server1_fixed_ip
        ) = self._setup_server(self.net1)
        (
            server2_floating_ip, server2_port_id, server2_fixed_ip
        ) = self._setup_server(self.net1)
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        fc = self._create_flowclassifier(
            logical_source_port=server1_port_id,
            source_ip_prefix='%s/32' % server1_fixed_ip,
            destination_ip_prefix='%s/32' % server2_fixed_ip
        )
        port_pair1 = self._create_port_pair(
            ingress=self.router2_net1['id'],
            egress=self.router2_net1['id']
        )
        port_pair2 = self._create_port_pair(
            ingress=self.router3_net1['id'],
            egress=self.router3_net1['id']
        )
        port_pair_group = self._create_port_pair_group(
            port_pairs=[port_pair1['id']]
        )
        self._create_port_chain(
            port_pair_groups=[
                port_pair_group['id']
            ],
            flow_classifiers=[fc['id']]
        )
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [[self.router2_net1_fixed_ip]],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        self.portpairgroup_client.update_port_pair_group(
            port_pair_group['id'],
            port_pairs=[
                port_pair1['id'], port_pair2['id']
            ]
        )
        self._wait_for_port_pair_group_status(port_pair_group, 'ACTIVE')
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [[self.router2_net1_fixed_ip, self.router3_net1_fixed_ip]],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])

    @decorators.idempotent_id('f970f6b3-6541-47ac-a9ea-f769be1e21ba')
    @test.services('compute', 'network')
    def test_update_port_pair_group_remove_port_pairs(self):
        (
            server1_floating_ip, server1_port_id, server1_fixed_ip
        ) = self._setup_server(self.net1)
        (
            server2_floating_ip, server2_port_id, server2_fixed_ip
        ) = self._setup_server(self.net1)
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        fc = self._create_flowclassifier(
            logical_source_port=server1_port_id,
            source_ip_prefix='%s/32' % server1_fixed_ip,
            destination_ip_prefix='%s/32' % server2_fixed_ip
        )
        port_pair1 = self._create_port_pair(
            ingress=self.router2_net1['id'],
            egress=self.router2_net1['id']
        )
        port_pair2 = self._create_port_pair(
            ingress=self.router3_net1['id'],
            egress=self.router3_net1['id']
        )
        port_pair_group = self._create_port_pair_group(
            port_pairs=[port_pair1['id'], port_pair2['id']]
        )
        self._create_port_chain(
            port_pair_groups=[
                port_pair_group['id']
            ],
            flow_classifiers=[fc['id']]
        )
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [[self.router2_net1_fixed_ip, self.router3_net1_fixed_ip]],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        self.portpairgroup_client.update_port_pair_group(
            port_pair_group['id'],
            port_pairs=[port_pair1['id']])
        self._wait_for_port_pair_group_status(port_pair_group, 'ACTIVE')
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [[self.router2_net1_fixed_ip]],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])

    @decorators.idempotent_id('f970f6b3-6541-47ac-a9ea-f769be1e21b9')
    @test.services('compute', 'network')
    def test_update_port_pair_group_replace_port_pairs(self):
        (
            server1_floating_ip, server1_port_id, server1_fixed_ip
        ) = self._setup_server(self.net1)
        (
            server2_floating_ip, server2_port_id, server2_fixed_ip
        ) = self._setup_server(self.net1)
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        fc = self._create_flowclassifier(
            logical_source_port=server1_port_id,
            source_ip_prefix='%s/32' % server1_fixed_ip,
            destination_ip_prefix='%s/32' % server2_fixed_ip
        )
        port_pair1 = self._create_port_pair(
            ingress=self.router2_net1['id'],
            egress=self.router2_net1['id']
        )
        port_pair2 = self._create_port_pair(
            ingress=self.router3_net1['id'],
            egress=self.router3_net1['id']
        )
        port_pair_group = self._create_port_pair_group(
            port_pairs=[port_pair1['id']]
        )
        self._create_port_chain(
            port_pair_groups=[
                port_pair_group['id']
            ],
            flow_classifiers=[fc['id']]
        )
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [[self.router2_net1_fixed_ip]],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        self.portpairgroup_client.update_port_pair_group(
            port_pair_group['id'],
            port_pairs=[port_pair2['id']])
        self._wait_for_port_pair_group_status(port_pair_group, 'ACTIVE')
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [[self.router3_net1_fixed_ip]],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])

    @decorators.idempotent_id('f970f6b3-6541-47ac-a9ea-f769be1e21b9')
    @test.services('compute', 'network')
    def test_multi_port_chains_update_port_pair_group_replace_port_pairs(
        self
    ):
        self.router4 = self._create_router()
        self.router4_net1 = self._create_port(self.net1['id'])
        self._add_router_interface(
            self.router4['id'], self.router4_net1['id'])
        self.router4_net1_fixed_ip = self.router4_net1[
            'fixed_ips'][0]['ip_address']
        self.router5 = self._create_router()
        self.router5_net1 = self._create_port(self.net1['id'])
        self._add_router_interface(
            self.router5['id'], self.router5_net1['id'])
        self.router5_net1_fixed_ip = self.router5_net1[
            'fixed_ips'][0]['ip_address']
        (
            server1_floating_ip, server1_port_id, server1_fixed_ip
        ) = self._setup_server(self.net1)
        (
            server2_floating_ip, server2_port_id, server2_fixed_ip
        ) = self._setup_server(self.net1)
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        fc1 = self._create_flowclassifier(
            logical_source_port=server1_port_id,
            source_ip_prefix='%s/32' % server1_fixed_ip,
            destination_ip_prefix='%s/32' % server2_fixed_ip
        )
        fc2 = self._create_flowclassifier(
            logical_source_port=server2_port_id,
            source_ip_prefix='%s/32' % server2_fixed_ip,
            destination_ip_prefix='%s/32' % server1_fixed_ip
        )
        port_pair1 = self._create_port_pair(
            ingress=self.router2_net1['id'],
            egress=self.router2_net1['id']
        )
        port_pair2 = self._create_port_pair(
            ingress=self.router3_net1['id'],
            egress=self.router3_net1['id']
        )
        port_pair3 = self._create_port_pair(
            ingress=self.router4_net1['id'],
            egress=self.router4_net1['id']
        )
        port_pair4 = self._create_port_pair(
            ingress=self.router5_net1['id'],
            egress=self.router5_net1['id']
        )
        port_pair_group1 = self._create_port_pair_group(
            port_pairs=[port_pair1['id']]
        )
        port_pair_group2 = self._create_port_pair_group(
            port_pairs=[port_pair2['id']]
        )
        self._create_port_chain(
            port_pair_groups=[
                port_pair_group1['id'], port_pair_group2['id']
            ],
            flow_classifiers=[fc1['id']]
        )
        self._create_port_chain(
            port_pair_groups=[
                port_pair_group2['id'], port_pair_group1['id']
            ],
            flow_classifiers=[fc2['id']]
        )
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [[self.router2_net1_fixed_ip], [self.router3_net1_fixed_ip]],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        self._check_connectivity(
            server2_floating_ip, server1_fixed_ip,
            [[self.router3_net1_fixed_ip], [self.router2_net1_fixed_ip]],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        self.portpairgroup_client.update_port_pair_group(
            port_pair_group1['id'],
            port_pairs=[port_pair3['id']])
        self._wait_for_port_pair_group_status(port_pair_group1, 'ACTIVE')
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [[self.router4_net1_fixed_ip], [self.router3_net1_fixed_ip]],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        self._check_connectivity(
            server2_floating_ip, server1_fixed_ip,
            [[self.router3_net1_fixed_ip], [self.router4_net1_fixed_ip]],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        self.portpairgroup_client.update_port_pair_group(
            port_pair_group2['id'],
            port_pairs=[port_pair4['id']])
        self._wait_for_port_pair_group_status(port_pair_group1, 'ACTIVE')
        self._check_connectivity(
            server1_floating_ip, server2_fixed_ip,
            [[self.router4_net1_fixed_ip], [self.router5_net1_fixed_ip]],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])
        self._check_connectivity(
            server2_floating_ip, server1_fixed_ip,
            [[self.router5_net1_fixed_ip], [self.router4_net1_fixed_ip]],
            username=self.ssh_user,
            private_key=self.keypair['private_key'])

    def _create_server(self, network):
        kwargs = {}
        if self.keypair is not None:
            kwargs['key_name'] = self.keypair['name']
        if self.security_group is not None:
            kwargs['security_groups'] = [{'name': self.security_group['name']}]
        server = self.create_server(
            networks=[{'uuid': network['id']}],
            wait_until='ACTIVE',
            **kwargs)
        waiters.wait_for_server_status(self.servers_client,
                                       server['id'], 'ACTIVE')
        self._check_tenant_network_connectivity(
            server, self.ssh_user, self.keypair['private_key'])
        return server

    def _add_router_interface(self, router_id, port_id):
        interface = self.routers_client.add_router_interface(
            router_id, port_id=port_id)
        self.addCleanup(self._remove_router_interface, router_id, port_id)
        return interface

    def _remove_router_interface(self, router_id, port_id):
        self.routers_client.remove_router_interface(
            router_id, port_id=port_id)

    def _create_flowclassifier(
        self, flowclassifier_client=None,
        **kwargs
    ):
        if not flowclassifier_client:
            flowclassifier_client = self.flowclassifier_client
        result = flowclassifier_client.create_flowclassifier(**kwargs)
        fc = result['flow_classifier']
        self.addCleanup(
            test_utils.call_and_ignore_notfound_exc,
            flowclassifier_client.delete_flowclassifier, fc['id'])
        return fc

    def _create_port_pair(self, portpair_client=None, **kwargs):
        if not portpair_client:
            portpair_client = self.portpair_client
        result = portpair_client.create_port_pair(**kwargs)
        pp = result['port_pair']
        self.addCleanup(
            test_utils.call_and_ignore_notfound_exc,
            portpair_client.delete_port_pair, pp['id'])
        return pp

    def _create_port_pair_group(self, portpairgroup_client=None, **kwargs):
        if not portpairgroup_client:
            portpairgroup_client = self.portpairgroup_client
        result = portpairgroup_client.create_port_pair_group(**kwargs)
        pg = result['port_pair_group']
        self.addCleanup(
            test_utils.call_and_ignore_notfound_exc,
            portpairgroup_client.delete_port_pair_group, pg['id'])
        return pg

    def _create_port_chain(self, portchain_client=None, **kwargs):
        if not portchain_client:
            portchain_client = self.portchain_client
        result = portchain_client.create_port_chain(**kwargs)
        pc = result['port_chain']
        self.addCleanup(
            test_utils.call_and_ignore_notfound_exc,
            portchain_client.delete_port_chain, pc['id'])
        self._wait_for_port_chain_status(pc, 'ACTIVE')
        return pc
