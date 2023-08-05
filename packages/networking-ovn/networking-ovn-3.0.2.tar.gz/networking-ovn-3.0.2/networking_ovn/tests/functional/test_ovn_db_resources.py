# Copyright 2016 Red Hat, Inc.
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


import mock
import netaddr

from neutron_lib.utils import net as n_net
from oslo_config import cfg
from ovsdbapp.backend.ovs_idl import idlutils

from networking_ovn.common import config as ovn_config
from networking_ovn.tests.functional import base


class TestNBDbResources(base.TestOVNFunctionalBase):

    def setUp(self):
        super(TestNBDbResources, self).setUp()
        self.fake_api = mock.MagicMock()
        self.fake_api.idl = self.monitor_nb_db_idl
        self.fake_api._tables = self.monitor_nb_db_idl.tables
        self.orig_get_random_mac = n_net.get_random_mac
        cfg.CONF.set_override('quota_subnet', -1, group='QUOTAS')
        ovn_config.cfg.CONF.set_override('ovn_metadata_enabled',
                                         False,
                                         group='ovn')

    def tearDown(self):
        super(TestNBDbResources, self).tearDown()

    def _verify_dhcp_option_rows(self, expected_dhcp_options_rows):
        expected_dhcp_options_rows = list(expected_dhcp_options_rows.values())
        observed_dhcp_options_rows = []
        for row in self.monitor_nb_db_idl.tables['DHCP_Options'].rows.values():
            observed_dhcp_options_rows.append({
                'cidr': row.cidr, 'external_ids': row.external_ids,
                'options': row.options})

        self.assertItemsEqual(expected_dhcp_options_rows,
                              observed_dhcp_options_rows)

    def _verify_dhcp_option_row_for_port(self, port_id,
                                         expected_lsp_dhcpv4_options,
                                         expected_lsp_dhcpv6_options=None):
        lsp = idlutils.row_by_value(self.monitor_nb_db_idl,
                                    'Logical_Switch_Port', 'name', port_id,
                                    None)

        if lsp.dhcpv4_options:
            observed_lsp_dhcpv4_options = {
                'cidr': lsp.dhcpv4_options[0].cidr,
                'external_ids': lsp.dhcpv4_options[0].external_ids,
                'options': lsp.dhcpv4_options[0].options}
        else:
            observed_lsp_dhcpv4_options = {}

        if lsp.dhcpv6_options:
            observed_lsp_dhcpv6_options = {
                'cidr': lsp.dhcpv6_options[0].cidr,
                'external_ids': lsp.dhcpv6_options[0].external_ids,
                'options': lsp.dhcpv6_options[0].options}
        else:
            observed_lsp_dhcpv6_options = {}

        if expected_lsp_dhcpv6_options is None:
            expected_lsp_dhcpv6_options = {}

        self.assertEqual(expected_lsp_dhcpv4_options,
                         observed_lsp_dhcpv4_options)
        self.assertEqual(expected_lsp_dhcpv6_options,
                         observed_lsp_dhcpv6_options)

    def _get_subnet_dhcp_mac(self, subnet):

        mac_key = 'server_id' if subnet['ip_version'] == 6 else 'server_mac'
        dhcp_options = self.mech_driver._nb_ovn.get_subnet_dhcp_options(
            subnet['id'])
        return dhcp_options.get('options', {}).get(
            mac_key) if dhcp_options else None

    def test_dhcp_options(self):
        """Test for DHCP_Options table rows

        When a new subnet is created, a new row has to be created in the
        DHCP_Options table for this subnet with the dhcp options stored
        in the DHCP_Options.options column.
        When ports are created for this subnet (with IPv4 address set and
        DHCP enabled in the subnet), the
        Logical_Switch_Port.dhcpv4_options column should refer to the
        appropriate row of DHCP_Options.

        In cases where a port has extra DHCPv4 options defined, a new row
        in the DHCP_Options table should be created for this port and
        Logical_Switch_Port.dhcpv4_options colimn should refer to this row.

        In order to map the DHCP_Options row to the subnet (and to a port),
        subnet_id is stored in DHCP_Options.external_ids column.
        For DHCP_Options row which belongs to a port, port_id is also stored
        in the DHCP_Options.external_ids along with the subnet_id.
        """

        n1 = self._make_network(self.fmt, 'n1', True)
        created_subnets = {}
        expected_dhcp_options_rows = {}
        dhcp_mac = {}

        for cidr in ['10.0.0.0/24', '20.0.0.0/24', '30.0.0.0/24',
                     '40.0.0.0/24', 'aef0::/64', 'bef0::/64']:
            ip_version = netaddr.IPNetwork(cidr).ip.version

            res = self._create_subnet(self.fmt, n1['network']['id'], cidr,
                                      ip_version=ip_version)
            subnet = self.deserialize(self.fmt, res)['subnet']
            created_subnets[cidr] = subnet
            dhcp_mac[subnet['id']] = self._get_subnet_dhcp_mac(subnet)

            if ip_version == 4:
                options = {'server_id': cidr.replace('0/24', '1'),
                           'server_mac': dhcp_mac[subnet['id']],
                           'lease_time': str(12 * 60 * 60),
                           'mtu': str(n1['network']['mtu']),
                           'router': subnet['gateway_ip']}
            else:
                options = {'server_id': dhcp_mac[subnet['id']]}

            expected_dhcp_options_rows[subnet['id']] = {
                'cidr': cidr,
                'external_ids': {'subnet_id': subnet['id']},
                'options': options}

        for (cidr, enable_dhcp, gateway_ip) in [
                ('50.0.0.0/24', False, '50.0.0.1'),
                ('60.0.0.0/24', True, None),
                ('cef0::/64', False, 'cef0::1'),
                ('def0::/64', True, None)]:
            ip_version = netaddr.IPNetwork(cidr).ip.version
            res = self._create_subnet(self.fmt, n1['network']['id'], cidr,
                                      ip_version=ip_version,
                                      enable_dhcp=enable_dhcp,
                                      gateway_ip=gateway_ip)
            subnet = self.deserialize(self.fmt, res)['subnet']
            created_subnets[cidr] = subnet
            dhcp_mac[subnet['id']] = self._get_subnet_dhcp_mac(subnet)
            if enable_dhcp:
                if ip_version == 4:
                    options = {}
                else:
                    options = {'server_id': dhcp_mac[subnet['id']]}
                expected_dhcp_options_rows[subnet['id']] = {
                    'cidr': cidr,
                    'external_ids': {'subnet_id': subnet['id']},
                    'options': options}

        # create a subnet with dns nameservers and host routes
        n2 = self._make_network(self.fmt, 'n2', True)
        res = self._create_subnet(
            self.fmt, n2['network']['id'], '10.0.0.0/24',
            dns_nameservers=['7.7.7.7', '8.8.8.8'],
            host_routes=[{'destination': '30.0.0.0/24',
                          'nexthop': '10.0.0.4'},
                         {'destination': '40.0.0.0/24',
                          'nexthop': '10.0.0.8'}])

        subnet = self.deserialize(self.fmt, res)['subnet']
        dhcp_mac[subnet['id']] = self._get_subnet_dhcp_mac(subnet)

        static_routes = ('{30.0.0.0/24,10.0.0.4, 40.0.0.0/24,'
                         '10.0.0.8, 0.0.0.0/0,10.0.0.1}')
        expected_dhcp_options_rows[subnet['id']] = {
            'cidr': '10.0.0.0/24',
            'external_ids': {'subnet_id': subnet['id']},
            'options': {'server_id': '10.0.0.1',
                        'server_mac': dhcp_mac[subnet['id']],
                        'lease_time': str(12 * 60 * 60),
                        'mtu': str(n2['network']['mtu']),
                        'router': subnet['gateway_ip'],
                        'dns_server': '{7.7.7.7, 8.8.8.8}',
                        'classless_static_route': static_routes}}

        # create an IPv6 subnet with dns nameservers
        res = self._create_subnet(
            self.fmt, n2['network']['id'], 'ae10::/64', ip_version=6,
            dns_nameservers=['be10::7', 'be10::8'])

        subnet = self.deserialize(self.fmt, res)['subnet']
        dhcp_mac[subnet['id']] = self._get_subnet_dhcp_mac(subnet)

        expected_dhcp_options_rows[subnet['id']] = {
            'cidr': 'ae10::/64',
            'external_ids': {'subnet_id': subnet['id']},
            'options': {'server_id': dhcp_mac[subnet['id']],
                        'dns_server': '{be10::7, be10::8}'}}

        # Verify that DHCP_Options rows are created for these subnets or not
        self._verify_dhcp_option_rows(expected_dhcp_options_rows)

        for cidr in ['20.0.0.0/24', 'aef0::/64']:
            subnet = created_subnets[cidr]
            # Disable dhcp in subnet and verify DHCP_Options
            data = {'subnet': {'enable_dhcp': False}}
            req = self.new_update_request('subnets', data, subnet['id'])
            req.get_response(self.api)
            options = expected_dhcp_options_rows.pop(subnet['id'])
            self._verify_dhcp_option_rows(expected_dhcp_options_rows)

            # Re-enable dhcp in subnet and verify DHCP_Options
            n_net.get_random_mac = mock.Mock()
            n_net.get_random_mac.return_value = dhcp_mac[subnet['id']]
            data = {'subnet': {'enable_dhcp': True}}
            req = self.new_update_request('subnets', data, subnet['id'])
            req.get_response(self.api)
            expected_dhcp_options_rows[subnet['id']] = options
            self._verify_dhcp_option_rows(expected_dhcp_options_rows)

        n_net.get_random_mac = self.orig_get_random_mac

        # Create a port and verify if Logical_Switch_Port.dhcpv4_options
        # is properly set or not
        subnet = created_subnets['40.0.0.0/24']
        subnet_v6 = created_subnets['aef0::/64']
        p = self._make_port(
            self.fmt, n1['network']['id'],
            fixed_ips=[
                {'subnet_id': subnet['id']},
                {'subnet_id': subnet_v6['id']}])

        self._verify_dhcp_option_row_for_port(
            p['port']['id'], expected_dhcp_options_rows[subnet['id']],
            expected_dhcp_options_rows[subnet_v6['id']])
        self._verify_dhcp_option_rows(expected_dhcp_options_rows)

        # create a port with dhcp disabled subnet
        subnet = created_subnets['50.0.0.0/24']

        p = self._make_port(self.fmt, n1['network']['id'],
                            fixed_ips=[{'subnet_id': subnet['id']}])

        self._verify_dhcp_option_row_for_port(p['port']['id'], {})
        self._verify_dhcp_option_rows(expected_dhcp_options_rows)

        # Delete the first subnet created
        subnet = created_subnets['10.0.0.0/24']
        req = self.new_delete_request('subnets', subnet['id'])
        req.get_response(self.api)

        # Verify that DHCP_Options rows are deleted or not
        del expected_dhcp_options_rows[subnet['id']]
        self._verify_dhcp_option_rows(expected_dhcp_options_rows)

    def test_port_dhcp_options(self):
        dhcp_mac = {}
        n1 = self._make_network(self.fmt, 'n1', True)
        res = self._create_subnet(self.fmt, n1['network']['id'], '10.0.0.0/24')
        subnet = self.deserialize(self.fmt, res)['subnet']
        dhcp_mac[subnet['id']] = self._get_subnet_dhcp_mac(subnet)
        res = self._create_subnet(self.fmt, n1['network']['id'], 'aef0::/64',
                                  ip_version=6)
        subnet_v6 = self.deserialize(self.fmt, res)['subnet']
        dhcp_mac[subnet_v6['id']] = self._get_subnet_dhcp_mac(subnet_v6)

        expected_dhcp_options_rows = {
            subnet['id']: {
                'cidr': '10.0.0.0/24',
                'external_ids': {'subnet_id': subnet['id']},
                'options': {'server_id': '10.0.0.1',
                            'server_mac': dhcp_mac[subnet['id']],
                            'lease_time': str(12 * 60 * 60),
                            'mtu': str(n1['network']['mtu']),
                            'router': subnet['gateway_ip']}},
            subnet_v6['id']: {
                'cidr': 'aef0::/64',
                'external_ids': {'subnet_id': subnet_v6['id']},
                'options': {'server_id': dhcp_mac[subnet_v6['id']]}}}
        expected_dhcp_v4_options_rows = {
            subnet['id']: expected_dhcp_options_rows[subnet['id']]}
        expected_dhcp_v6_options_rows = {
            subnet_v6['id']: expected_dhcp_options_rows[subnet_v6['id']]}
        data = {
            'port': {'network_id': n1['network']['id'],
                     'tenant_id': self._tenant_id,
                     'device_owner': 'compute:None',
                     'fixed_ips': [{'subnet_id': subnet['id']}],
                     'extra_dhcp_opts': [{'ip_version': 4, 'opt_name': 'mtu',
                                          'opt_value': '1100'},
                                         {'ip_version': 4,
                                          'opt_name': 'ntp-server',
                                          'opt_value': '8.8.8.8'}]}}
        port_req = self.new_create_request('ports', data, self.fmt)
        port_res = port_req.get_response(self.api)
        p1 = self.deserialize(self.fmt, port_res)

        expected_dhcp_options_rows['v4-' + p1['port']['id']] = {
            'cidr': '10.0.0.0/24',
            'external_ids': {'subnet_id': subnet['id'],
                             'port_id': p1['port']['id']},
            'options': {'server_id': '10.0.0.1',
                        'server_mac': dhcp_mac[subnet['id']],
                        'lease_time': str(12 * 60 * 60),
                        'mtu': '1100',
                        'router': subnet['gateway_ip'],
                        'ntp_server': '8.8.8.8'}}
        expected_dhcp_v4_options_rows['v4-' + p1['port']['id']] = \
            expected_dhcp_options_rows['v4-' + p1['port']['id']]
        data = {
            'port': {'network_id': n1['network']['id'],
                     'tenant_id': self._tenant_id,
                     'device_owner': 'compute:None',
                     'fixed_ips': [{'subnet_id': subnet['id']}],
                     'extra_dhcp_opts': [{'ip_version': 4,
                                          'opt_name': 'ip-forward-enable',
                                          'opt_value': '1'},
                                         {'ip_version': 4,
                                          'opt_name': 'tftp-server',
                                          'opt_value': '10.0.0.100'},
                                         {'ip_version': 4,
                                          'opt_name': 'dns-server',
                                          'opt_value': '20.20.20.20'}]}}

        port_req = self.new_create_request('ports', data, self.fmt)
        port_res = port_req.get_response(self.api)
        p2 = self.deserialize(self.fmt, port_res)

        expected_dhcp_options_rows['v4-' + p2['port']['id']] = {
            'cidr': '10.0.0.0/24',
            'external_ids': {'subnet_id': subnet['id'],
                             'port_id': p2['port']['id']},
            'options': {'server_id': '10.0.0.1',
                        'server_mac': dhcp_mac[subnet['id']],
                        'lease_time': str(12 * 60 * 60),
                        'mtu': str(n1['network']['mtu']),
                        'router': subnet['gateway_ip'],
                        'ip_forward_enable': '1',
                        'tftp_server': '10.0.0.100',
                        'dns_server': '20.20.20.20'}}
        expected_dhcp_v4_options_rows['v4-' + p2['port']['id']] = \
            expected_dhcp_options_rows['v4-' + p2['port']['id']]
        data = {
            'port': {'network_id': n1['network']['id'],
                     'tenant_id': self._tenant_id,
                     'device_owner': 'compute:None',
                     'fixed_ips': [{'subnet_id': subnet_v6['id']}],
                     'extra_dhcp_opts': [{'ip_version': 6,
                                          'opt_name': 'dns-server',
                                          'opt_value': 'aef0::1'},
                                         {'ip_version': 6,
                                          'opt_name': 'domain-search',
                                          'opt_value': 'foo-domain'}]}}
        port_req = self.new_create_request('ports', data, self.fmt)
        port_res = port_req.get_response(self.api)
        p3 = self.deserialize(self.fmt, port_res)
        expected_dhcp_options_rows['v6-' + p3['port']['id']] = {
            'cidr': 'aef0::/64',
            'external_ids': {'subnet_id': subnet_v6['id'],
                             'port_id': p3['port']['id']},
            'options': {'server_id': dhcp_mac[subnet_v6['id']],
                        'dns_server': 'aef0::1',
                        'domain_search': 'foo-domain'}}
        expected_dhcp_v6_options_rows['v6-' + p3['port']['id']] = \
            expected_dhcp_options_rows['v6-' + p3['port']['id']]
        data = {
            'port': {'network_id': n1['network']['id'],
                     'tenant_id': self._tenant_id,
                     'device_owner': 'compute:None',
                     'fixed_ips': [{'subnet_id': subnet['id']},
                                   {'subnet_id': subnet_v6['id']}],
                     'extra_dhcp_opts': [{'ip_version': 4,
                                          'opt_name': 'tftp-server',
                                          'opt_value': '100.0.0.100'},
                                         {'ip_version': 6,
                                          'opt_name': 'dns-server',
                                          'opt_value': 'aef0::100'},
                                         {'ip_version': 6,
                                          'opt_name': 'domain-search',
                                          'opt_value': 'bar-domain'}]}}
        port_req = self.new_create_request('ports', data, self.fmt)
        port_res = port_req.get_response(self.api)
        p4 = self.deserialize(self.fmt, port_res)
        expected_dhcp_options_rows['v6-' + p4['port']['id']] = {
            'cidr': 'aef0::/64',
            'external_ids': {'subnet_id': subnet_v6['id'],
                             'port_id': p4['port']['id']},
            'options': {'server_id': dhcp_mac[subnet_v6['id']],
                        'dns_server': 'aef0::100',
                        'domain_search': 'bar-domain'}}
        expected_dhcp_options_rows['v4-' + p4['port']['id']] = {
            'cidr': '10.0.0.0/24',
            'external_ids': {'subnet_id': subnet['id'],
                             'port_id': p4['port']['id']},
            'options': {'server_id': '10.0.0.1',
                        'server_mac': dhcp_mac[subnet['id']],
                        'lease_time': str(12 * 60 * 60),
                        'mtu': str(n1['network']['mtu']),
                        'router': subnet['gateway_ip'],
                        'tftp_server': '100.0.0.100'}}
        expected_dhcp_v4_options_rows['v4-' + p4['port']['id']] = \
            expected_dhcp_options_rows['v4-' + p4['port']['id']]
        expected_dhcp_v6_options_rows['v6-' + p4['port']['id']] = \
            expected_dhcp_options_rows['v6-' + p4['port']['id']]
        self._verify_dhcp_option_rows(expected_dhcp_options_rows)

        self._verify_dhcp_option_row_for_port(
            p1['port']['id'],
            expected_dhcp_options_rows['v4-' + p1['port']['id']])
        self._verify_dhcp_option_row_for_port(
            p2['port']['id'],
            expected_dhcp_options_rows['v4-' + p2['port']['id']])
        self._verify_dhcp_option_row_for_port(
            p3['port']['id'], {},
            expected_lsp_dhcpv6_options=expected_dhcp_options_rows[
                'v6-' + p3['port']['id']])
        self._verify_dhcp_option_row_for_port(
            p4['port']['id'],
            expected_dhcp_options_rows['v4-' + p4['port']['id']],
            expected_lsp_dhcpv6_options=expected_dhcp_options_rows[
                'v6-' + p4['port']['id']])

        # Update the subnet with dns_server. It should get propagated
        # to the DHCP options of the p1. Note that it should not get
        # propagate to DHCP options of port p2 because, it has overridden
        # dns-server in the Extra DHCP options.
        data = {'subnet': {'dns_nameservers': ['7.7.7.7', '8.8.8.8']}}
        req = self.new_update_request('subnets', data, subnet['id'])
        req.get_response(self.api)

        for i in [subnet['id'], 'v4-' + p1['port']['id'],
                  'v4-' + p4['port']['id']]:
            expected_dhcp_options_rows[i]['options']['dns_server'] = (
                '{7.7.7.7, 8.8.8.8}')

        self._verify_dhcp_option_rows(expected_dhcp_options_rows)

        # Update the port p2 by removing dns-server and tfp-server in the
        # extra DHCP options. dns-server option from the subnet DHCP options
        # should be updated in the p2 DHCP options
        data = {'port': {'extra_dhcp_opts': [{'ip_version': 4,
                                              'opt_name': 'ip-forward-enable',
                                              'opt_value': '0'},
                                             {'ip_version': 4,
                                              'opt_name': 'tftp-server',
                                              'opt_value': None},
                                             {'ip_version': 4,
                                              'opt_name': 'dns-server',
                                              'opt_value': None}]}}
        port_req = self.new_update_request('ports', data, p2['port']['id'])
        port_req.get_response(self.api)
        p2_expected = expected_dhcp_options_rows['v4-' + p2['port']['id']]
        p2_expected['options']['dns_server'] = '{7.7.7.7, 8.8.8.8}'

        p2_expected['options']['ip_forward_enable'] = '0'

        del p2_expected['options']['tftp_server']
        self._verify_dhcp_option_rows(expected_dhcp_options_rows)

        # Test subnet DHCP disabling and enabling
        for (subnet_id, expect_subnet_rows_disabled,
             expect_port_v4_row_disabled, expect_port_v6_row_disabled) in [
            (subnet['id'], expected_dhcp_v6_options_rows, {},
             expected_dhcp_options_rows['v6-' + p4['port']['id']]),
            (subnet_v6['id'], expected_dhcp_v4_options_rows,
             expected_dhcp_options_rows['v4-' + p4['port']['id']], {})]:
            # Disable subnet's DHCP and verify DHCP_Options,
            data = {'subnet': {'enable_dhcp': False}}
            req = self.new_update_request('subnets', data, subnet_id)
            req.get_response(self.api)
            # DHCP_Options belonging to the subnet or it's ports should be all
            # removed, current DHCP_Options should be equal to
            # expect_subnet_rows_disabled
            self._verify_dhcp_option_rows(expect_subnet_rows_disabled)
            # Verify that the corresponding port DHCP options were cleared
            # and the others were not affected.
            self._verify_dhcp_option_row_for_port(
                p4['port']['id'], expect_port_v4_row_disabled,
                expect_port_v6_row_disabled)
            # Re-enable dhcpv4 in subnet and verify DHCP_Options
            n_net.get_random_mac = mock.Mock()
            n_net.get_random_mac.return_value = dhcp_mac[subnet_id]
            data = {'subnet': {'enable_dhcp': True}}
            req = self.new_update_request('subnets', data, subnet_id)
            req.get_response(self.api)
            self._verify_dhcp_option_rows(expected_dhcp_options_rows)
            self._verify_dhcp_option_row_for_port(
                p4['port']['id'],
                expected_dhcp_options_rows['v4-' + p4['port']['id']],
                expected_dhcp_options_rows['v6-' + p4['port']['id']])
        n_net.get_random_mac = self.orig_get_random_mac

        # Disable dhcp in p2
        data = {'port': {'extra_dhcp_opts': [{'ip_version': 4,
                                              'opt_name': 'dhcp_disabled',
                                              'opt_value': 'true'}]}}
        port_req = self.new_update_request('ports', data, p2['port']['id'])
        port_req.get_response(self.api)

        del expected_dhcp_options_rows['v4-' + p2['port']['id']]
        self._verify_dhcp_option_rows(expected_dhcp_options_rows)

        # delete port p1.
        port_req = self.new_delete_request('ports', p1['port']['id'])
        port_req.get_response(self.api)

        del expected_dhcp_options_rows['v4-' + p1['port']['id']]
        self._verify_dhcp_option_rows(expected_dhcp_options_rows)

        # delete the IPv6 extra DHCP options for p4
        data = {'port': {'extra_dhcp_opts': [{'ip_version': 6,
                                              'opt_name': 'dns-server',
                                              'opt_value': None},
                                             {'ip_version': 6,
                                              'opt_name': 'domain-search',
                                              'opt_value': None}]}}
        port_req = self.new_update_request('ports', data, p4['port']['id'])
        port_req.get_response(self.api)
        del expected_dhcp_options_rows['v6-' + p4['port']['id']]

        self._verify_dhcp_option_rows(expected_dhcp_options_rows)

    def test_port_dhcp_opts_add_and_remove_extra_dhcp_opts(self):
        """Orphaned DHCP_Options row.

        In this test case a port is created with extra DHCP options.
        Since it has extra DHCP options a new row in the DHCP_Options is
        created for this port.
        Next the port is updated to delete the extra DHCP options.
        After the update, the Logical_Switch_Port.dhcpv4_options for this port
        should refer to the subnet DHCP_Options and the DHCP_Options row
        created for this port earlier should be deleted.
        """
        dhcp_mac = {}
        n1 = self._make_network(self.fmt, 'n1', True)
        res = self._create_subnet(self.fmt, n1['network']['id'], '10.0.0.0/24')
        subnet = self.deserialize(self.fmt, res)['subnet']
        dhcp_mac[subnet['id']] = self._get_subnet_dhcp_mac(subnet)
        res = self._create_subnet(self.fmt, n1['network']['id'], 'aef0::/64',
                                  ip_version=6)
        subnet_v6 = self.deserialize(self.fmt, res)['subnet']
        dhcp_mac[subnet_v6['id']] = self._get_subnet_dhcp_mac(subnet_v6)
        expected_dhcp_options_rows = {
            subnet['id']: {
                'cidr': '10.0.0.0/24',
                'external_ids': {'subnet_id': subnet['id']},
                'options': {'server_id': '10.0.0.1',
                            'server_mac': dhcp_mac[subnet['id']],
                            'lease_time': str(12 * 60 * 60),
                            'mtu': str(n1['network']['mtu']),
                            'router': subnet['gateway_ip']}},
            subnet_v6['id']: {
                'cidr': 'aef0::/64',
                'external_ids': {'subnet_id': subnet_v6['id']},
                'options': {'server_id': dhcp_mac[subnet_v6['id']]}}}

        data = {
            'port': {'network_id': n1['network']['id'],
                     'tenant_id': self._tenant_id,
                     'device_owner': 'compute:None',
                     'extra_dhcp_opts': [{'ip_version': 4, 'opt_name': 'mtu',
                                          'opt_value': '1100'},
                                         {'ip_version': 4,
                                          'opt_name': 'ntp-server',
                                          'opt_value': '8.8.8.8'},
                                         {'ip_version': 6,
                                          'opt_name': 'dns-server',
                                          'opt_value': 'aef0::100'}]}}
        port_req = self.new_create_request('ports', data, self.fmt)
        port_res = port_req.get_response(self.api)
        p1 = self.deserialize(self.fmt, port_res)['port']

        expected_dhcp_options_rows['v4-' + p1['id']] = {
            'cidr': '10.0.0.0/24',
            'external_ids': {'subnet_id': subnet['id'],
                             'port_id': p1['id']},
            'options': {'server_id': '10.0.0.1',
                        'server_mac': dhcp_mac[subnet['id']],
                        'lease_time': str(12 * 60 * 60),
                        'mtu': '1100',
                        'router': subnet['gateway_ip'],
                        'ntp_server': '8.8.8.8'}}

        expected_dhcp_options_rows['v6-' + p1['id']] = {
            'cidr': 'aef0::/64',
            'external_ids': {'subnet_id': subnet_v6['id'],
                             'port_id': p1['id']},
            'options': {'server_id': dhcp_mac[subnet_v6['id']],
                        'dns_server': 'aef0::100'}}

        self._verify_dhcp_option_rows(expected_dhcp_options_rows)
        # The Logical_Switch_Port.dhcp(v4/v6)_options should refer to the
        # port DHCP options.
        self._verify_dhcp_option_row_for_port(
            p1['id'], expected_dhcp_options_rows['v4-' + p1['id']],
            expected_dhcp_options_rows['v6-' + p1['id']])

        # Now update the port to delete the extra DHCP options
        data = {'port': {'extra_dhcp_opts': [{'ip_version': 4,
                                              'opt_name': 'mtu',
                                              'opt_value': None},
                                             {'ip_version': 4,
                                              'opt_name': 'ntp-server',
                                              'opt_value': None}]}}
        port_req = self.new_update_request('ports', data, p1['id'])
        port_req.get_response(self.api)

        # DHCP_Options row created for the port earlier should have been
        # deleted.
        del expected_dhcp_options_rows['v4-' + p1['id']]
        self._verify_dhcp_option_rows(expected_dhcp_options_rows)
        # The Logical_Switch_Port.dhcpv4_options for this port should refer to
        # the subnet DHCP options.
        self._verify_dhcp_option_row_for_port(
            p1['id'], expected_dhcp_options_rows[subnet['id']],
            expected_dhcp_options_rows['v6-' + p1['id']])

        # update the port again with extra DHCP options.
        data = {'port': {'extra_dhcp_opts': [{'ip_version': 4,
                                              'opt_name': 'mtu',
                                              'opt_value': '1200'},
                                             {'ip_version': 4,
                                              'opt_name': 'tftp-server',
                                              'opt_value': '8.8.8.8'}]}}

        port_req = self.new_update_request('ports', data, p1['id'])
        port_req.get_response(self.api)

        expected_dhcp_options_rows['v4-' + p1['id']] = {
            'cidr': '10.0.0.0/24',
            'external_ids': {'subnet_id': subnet['id'],
                             'port_id': p1['id']},
            'options': {'server_id': '10.0.0.1',
                        'server_mac': dhcp_mac[subnet['id']],
                        'lease_time': str(12 * 60 * 60),
                        'mtu': '1200',
                        'router': subnet['gateway_ip'],
                        'tftp_server': '8.8.8.8'}}
        self._verify_dhcp_option_rows(expected_dhcp_options_rows)
        self._verify_dhcp_option_row_for_port(
            p1['id'], expected_dhcp_options_rows['v4-' + p1['id']],
            expected_dhcp_options_rows['v6-' + p1['id']])

        # Disable DHCPv4 for this port. The DHCP_Options row created for this
        # port should be get deleted.
        data = {'port': {'extra_dhcp_opts': [{'ip_version': 4,
                                              'opt_name': 'dhcp_disabled',
                                              'opt_value': 'true'}]}}
        port_req = self.new_update_request('ports', data, p1['id'])
        port_req.get_response(self.api)

        del expected_dhcp_options_rows['v4-' + p1['id']]
        self._verify_dhcp_option_rows(expected_dhcp_options_rows)
        # The Logical_Switch_Port.dhcpv4_options for this port should be
        # empty.
        self._verify_dhcp_option_row_for_port(
            p1['id'], {}, expected_dhcp_options_rows['v6-' + p1['id']])

        # Disable DHCPv6 for this port. The DHCP_Options row created for this
        # port should be get deleted.
        data = {'port': {'extra_dhcp_opts': [{'ip_version': 6,
                                              'opt_name': 'dhcp_disabled',
                                              'opt_value': 'true'}]}}
        port_req = self.new_update_request('ports', data, p1['id'])
        port_req.get_response(self.api)

        del expected_dhcp_options_rows['v6-' + p1['id']]
        self._verify_dhcp_option_rows(expected_dhcp_options_rows)
        # The Logical_Switch_Port.dhcpv4_options for this port should be
        # empty.
        self._verify_dhcp_option_row_for_port(p1['id'], {})


class TestNBDbResourcesOverTcp(TestNBDbResources):
    def get_ovsdb_server_protocol(self):
        return 'tcp'


class TestNBDbResourcesOverSsl(TestNBDbResources):
    def get_ovsdb_server_protocol(self):
        return 'ssl'
