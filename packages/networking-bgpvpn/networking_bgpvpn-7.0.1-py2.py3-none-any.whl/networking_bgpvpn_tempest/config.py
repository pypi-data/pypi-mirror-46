# Copyright (c) 2015 Ericsson.
# All Rights Reserved.
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

from oslo_config import cfg

service_option = cfg.BoolOpt("bgpvpn",
                             default=False,
                             help="Whether or not bgpvpn is expected to be "
                                  "available")

BgpvpnGroup = [
    cfg.IntOpt('min_asn',
               default=100,
               help=("Minimum number for the range of "
                     "autonomous system number for distinguishers.")),
    cfg.IntOpt('min_nn',
               default=100,
               help=("Minimum number for the range of "
                     "assigned number for distinguishers.")),
    cfg.IntOpt('max_asn',
               default=200,
               help=("Maximum number for the range of "
                     "autonomous system number for distinguishers.")),
    cfg.IntOpt('max_nn',
               default=200,
               help=("Maximum number for the range of "
                     "assigned number for distinguishers.")),
]

bgpvpn_group = cfg.OptGroup(name="bgpvpn", title=("Networking-Bgpvpn Service "
                                                  "Options"))
