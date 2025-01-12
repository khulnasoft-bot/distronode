# This code is part of Distronode, but is an independent component.
# This particular file snippet, and this file snippet only, is BSD licensed.
# Modules you write using this snippet, which is embedded dynamically by Distronode
# still belong to the author of the module, and may assign their own license
# to the complete work.
#
# (c) 2017 Red Hat Inc.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright notice,
#      this list of conditions and the following disclaimer in the documentation
#      and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

from __future__ import annotations

from distronode.module_utils.facts.namespace import PrefixFactNamespace
from distronode.module_utils.facts import default_collectors
from distronode.module_utils.facts import distronode_collector


def get_all_facts(module):
    """compat api for distronode 2.2/2.3 module_utils.facts.get_all_facts method

    Expects module to be an instance of DistronodeModule, with a 'gather_subset' param.

    returns a dict mapping the bare fact name ('default_ipv4' with no 'distronode_' namespace) to
    the fact value."""

    gather_subset = module.params['gather_subset']
    return distronode_facts(module, gather_subset=gather_subset)


def distronode_facts(module, gather_subset=None):
    """Compat api for distronode 2.0/2.2/2.3 module_utils.facts.distronode_facts method

    2.3/2.3 expects a gather_subset arg.
    2.0/2.1 does not except a gather_subset arg

    So make gather_subsets an optional arg, defaulting to configured DEFAULT_GATHER_TIMEOUT

    'module' should be an instance of an DistronodeModule.

    returns a dict mapping the bare fact name ('default_ipv4' with no 'distronode_' namespace) to
    the fact value.
    """

    gather_subset = gather_subset or module.params.get('gather_subset', ['all'])
    gather_timeout = module.params.get('gather_timeout', 10)
    filter_spec = module.params.get('filter', '*')

    minimal_gather_subset = frozenset(['apparmor', 'caps', 'cmdline', 'date_time',
                                       'distribution', 'dns', 'env', 'fips', 'local',
                                       'lsb', 'pkg_mgr', 'platform', 'python', 'selinux',
                                       'service_mgr', 'ssh_pub_keys', 'user'])

    all_collector_classes = default_collectors.collectors

    # don't add a prefix
    namespace = PrefixFactNamespace(namespace_name='distronode', prefix='')

    fact_collector = \
        distronode_collector.get_distronode_collector(all_collector_classes=all_collector_classes,
                                                namespace=namespace,
                                                filter_spec=filter_spec,
                                                gather_subset=gather_subset,
                                                gather_timeout=gather_timeout,
                                                minimal_gather_subset=minimal_gather_subset)

    facts_dict = fact_collector.collect(module=module)

    return facts_dict
