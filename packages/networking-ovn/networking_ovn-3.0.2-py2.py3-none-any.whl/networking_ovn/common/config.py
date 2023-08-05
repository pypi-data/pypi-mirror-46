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

from oslo_config import cfg
from ovsdbapp.backend.ovs_idl import vlog

from networking_ovn._i18n import _
from neutron_lib.api.definitions import portbindings


VLOG_LEVELS = {'CRITICAL': vlog.CRITICAL, 'ERROR': vlog.ERROR, 'WARNING':
               vlog.WARN, 'INFO': vlog.INFO, 'DEBUG': vlog.DEBUG}

ovn_opts = [
    cfg.StrOpt('ovn_nb_connection',
               default='tcp:127.0.0.1:6641',
               help=_('The connection string for the OVN_Northbound OVSDB.\n'
                      'Use tcp:IP:PORT for TCP connection.\n'
                      'Use ssl:IP:PORT for SSL connection. The '
                      'ovn_nb_private_key, ovn_nb_certificate and '
                      'ovn_nb_ca_cert are mandatory.\n'
                      'Use unix:FILE for unix domain socket connection.')),
    cfg.StrOpt('ovn_nb_private_key',
               default='',
               help=_('The PEM file with private key for SSL connection to '
                      'OVN-NB-DB')),
    cfg.StrOpt('ovn_nb_certificate',
               default='',
               help=_('The PEM file with certificate that certifies the '
                      'private key specified in ovn_nb_private_key')),
    cfg.StrOpt('ovn_nb_ca_cert',
               default='',
               help=_('The PEM file with CA certificate that OVN should use to'
                      ' verify certificates presented to it by SSL peers')),
    cfg.StrOpt('ovn_sb_connection',
               default='tcp:127.0.0.1:6642',
               help=_('The connection string for the OVN_Southbound OVSDB.\n'
                      'Use tcp:IP:PORT for TCP connection.\n'
                      'Use ssl:IP:PORT for SSL connection. The '
                      'ovn_sb_private_key, ovn_sb_certificate and '
                      'ovn_sb_ca_cert are mandatory.\n'
                      'Use unix:FILE for unix domain socket connection.')),
    cfg.StrOpt('ovn_sb_private_key',
               default='',
               help=_('The PEM file with private key for SSL connection to '
                      'OVN-SB-DB')),
    cfg.StrOpt('ovn_sb_certificate',
               default='',
               help=_('The PEM file with certificate that certifies the '
                      'private key specified in ovn_sb_private_key')),
    cfg.StrOpt('ovn_sb_ca_cert',
               default='',
               help=_('The PEM file with CA certificate that OVN should use to'
                      ' verify certificates presented to it by SSL peers')),
    cfg.IntOpt('ovsdb_connection_timeout',
               default=180,
               help=_('Timeout in seconds for the OVSDB '
                      'connection transaction')),
    cfg.IntOpt('ovsdb_probe_interval',
               min=0,
               default=0,
               help=_('The probe interval in for the OVSDB session in '
                      'milliseconds. If this is zero, it disables the '
                      'connection keepalive feature. If non-zero the value '
                      'will be forced to at least 1000 milliseconds. Probing '
                      'is disabled by default.')),
    cfg.StrOpt('neutron_sync_mode',
               default='log',
               choices=('off', 'log', 'repair'),
               help=_('The synchronization mode of OVN_Northbound OVSDB '
                      'with Neutron DB.\n'
                      'off - synchronization is off \n'
                      'log - during neutron-server startup, '
                      'check to see if OVN is in sync with '
                      'the Neutron database. '
                      ' Log warnings for any inconsistencies found so'
                      ' that an admin can investigate \n'
                      'repair - during neutron-server startup, automatically'
                      ' create resources found in Neutron but not in OVN.'
                      ' Also remove resources from OVN'
                      ' that are no longer in Neutron.')),
    cfg.BoolOpt('ovn_l3_mode',
                default=True,
                deprecated_for_removal=True,
                deprecated_reason="This option is no longer used. Native L3 "
                                  "support in OVN is always used.",
                help=_('Whether to use OVN native L3 support. Do not change '
                       'the value for existing deployments that contain '
                       'routers.')),
    cfg.StrOpt("ovn_l3_scheduler",
               default='leastloaded',
               choices=('leastloaded', 'chance'),
               help=_('The OVN L3 Scheduler type used to schedule router '
                      'gateway ports on hypervisors/chassis. \n'
                      'leastloaded - chassis with fewest gateway ports '
                      'selected \n'
                      'chance - chassis randomly selected')),
    cfg.StrOpt("vif_type",
               deprecated_for_removal=True,
               deprecated_reason="The port VIF type is now determined based "
                                 "on the OVN chassis information when the "
                                 "port is bound to a host.",
               default=portbindings.VIF_TYPE_OVS,
               help=_("Type of VIF to be used for ports valid values are "
                      "(%(ovs)s, %(dpdk)s) default %(ovs)s") % {
                          "ovs": portbindings.VIF_TYPE_OVS,
                          "dpdk": portbindings.VIF_TYPE_VHOST_USER},
               choices=[portbindings.VIF_TYPE_OVS,
                        portbindings.VIF_TYPE_VHOST_USER]),
    cfg.StrOpt("vhost_sock_dir",
               default="/var/run/openvswitch",
               help=_("The directory in which vhost virtio socket "
                      "is created by all the vswitch daemons")),
    cfg.IntOpt('dhcp_default_lease_time',
               default=(12 * 60 * 60),
               help=_('Default least time (in seconds) to use with '
                      'OVN\'s native DHCP service.')),
    cfg.StrOpt("ovsdb_log_level",
               default="INFO",
               choices=list(VLOG_LEVELS.keys()),
               help=_("The log level used for OVSDB")),
    cfg.BoolOpt('ovn_metadata_enabled',
                default=False,
                help=_('Whether to use metadata service.'))
]

cfg.CONF.register_opts(ovn_opts, group='ovn')


def list_opts():
    return [
        ('ovn', ovn_opts),
    ]


def get_ovn_nb_connection():
    return cfg.CONF.ovn.ovn_nb_connection


def get_ovn_nb_private_key():
    return cfg.CONF.ovn.ovn_nb_private_key


def get_ovn_nb_certificate():
    return cfg.CONF.ovn.ovn_nb_certificate


def get_ovn_nb_ca_cert():
    return cfg.CONF.ovn.ovn_nb_ca_cert


def get_ovn_sb_connection():
    return cfg.CONF.ovn.ovn_sb_connection


def get_ovn_sb_private_key():
    return cfg.CONF.ovn.ovn_sb_private_key


def get_ovn_sb_certificate():
    return cfg.CONF.ovn.ovn_sb_certificate


def get_ovn_sb_ca_cert():
    return cfg.CONF.ovn.ovn_sb_ca_cert


def get_ovn_ovsdb_timeout():
    return cfg.CONF.ovn.ovsdb_connection_timeout


def get_ovn_ovsdb_probe_interval():
    return cfg.CONF.ovn.ovsdb_probe_interval


def get_ovn_neutron_sync_mode():
    return cfg.CONF.ovn.neutron_sync_mode


def is_ovn_l3():
    return cfg.CONF.ovn.ovn_l3_mode


def get_ovn_l3_scheduler():
    return cfg.CONF.ovn.ovn_l3_scheduler


def get_ovn_vhost_sock_dir():
    return cfg.CONF.ovn.vhost_sock_dir


def get_ovn_dhcp_default_lease_time():
    return cfg.CONF.ovn.dhcp_default_lease_time


def get_ovn_ovsdb_log_level():
    return VLOG_LEVELS[cfg.CONF.ovn.ovsdb_log_level]


def is_ovn_metadata_enabled():
    return cfg.CONF.ovn.ovn_metadata_enabled
