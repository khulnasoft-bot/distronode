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

import distronode.module_utils.compat.typing as t

from distronode.module_utils.facts.collector import BaseFactCollector

from distronode.module_utils.facts.other.facter import FacterFactCollector
from distronode.module_utils.facts.other.ohai import OhaiFactCollector

from distronode.module_utils.facts.system.apparmor import ApparmorFactCollector
from distronode.module_utils.facts.system.caps import SystemCapabilitiesFactCollector
from distronode.module_utils.facts.system.chroot import ChrootFactCollector
from distronode.module_utils.facts.system.cmdline import CmdLineFactCollector
from distronode.module_utils.facts.system.distribution import DistributionFactCollector
from distronode.module_utils.facts.system.date_time import DateTimeFactCollector
from distronode.module_utils.facts.system.env import EnvFactCollector
from distronode.module_utils.facts.system.dns import DnsFactCollector
from distronode.module_utils.facts.system.fips import FipsFactCollector
from distronode.module_utils.facts.system.loadavg import LoadAvgFactCollector
from distronode.module_utils.facts.system.local import LocalFactCollector
from distronode.module_utils.facts.system.lsb import LSBFactCollector
from distronode.module_utils.facts.system.pkg_mgr import PkgMgrFactCollector
from distronode.module_utils.facts.system.pkg_mgr import OpenBSDPkgMgrFactCollector
from distronode.module_utils.facts.system.platform import PlatformFactCollector
from distronode.module_utils.facts.system.python import PythonFactCollector
from distronode.module_utils.facts.system.selinux import SelinuxFactCollector
from distronode.module_utils.facts.system.service_mgr import ServiceMgrFactCollector
from distronode.module_utils.facts.system.ssh_pub_keys import SshPubKeyFactCollector
from distronode.module_utils.facts.system.systemd import SystemdFactCollector
from distronode.module_utils.facts.system.user import UserFactCollector

from distronode.module_utils.facts.hardware.base import HardwareCollector
from distronode.module_utils.facts.hardware.aix import AIXHardwareCollector
from distronode.module_utils.facts.hardware.darwin import DarwinHardwareCollector
from distronode.module_utils.facts.hardware.dragonfly import DragonFlyHardwareCollector
from distronode.module_utils.facts.hardware.freebsd import FreeBSDHardwareCollector
from distronode.module_utils.facts.hardware.hpux import HPUXHardwareCollector
from distronode.module_utils.facts.hardware.hurd import HurdHardwareCollector
from distronode.module_utils.facts.hardware.linux import LinuxHardwareCollector
from distronode.module_utils.facts.hardware.netbsd import NetBSDHardwareCollector
from distronode.module_utils.facts.hardware.openbsd import OpenBSDHardwareCollector
from distronode.module_utils.facts.hardware.sunos import SunOSHardwareCollector

from distronode.module_utils.facts.network.base import NetworkCollector
from distronode.module_utils.facts.network.aix import AIXNetworkCollector
from distronode.module_utils.facts.network.darwin import DarwinNetworkCollector
from distronode.module_utils.facts.network.dragonfly import DragonFlyNetworkCollector
from distronode.module_utils.facts.network.fc_wwn import FcWwnInitiatorFactCollector
from distronode.module_utils.facts.network.freebsd import FreeBSDNetworkCollector
from distronode.module_utils.facts.network.hpux import HPUXNetworkCollector
from distronode.module_utils.facts.network.hurd import HurdNetworkCollector
from distronode.module_utils.facts.network.linux import LinuxNetworkCollector
from distronode.module_utils.facts.network.iscsi import IscsiInitiatorNetworkCollector
from distronode.module_utils.facts.network.nvme import NvmeInitiatorNetworkCollector
from distronode.module_utils.facts.network.netbsd import NetBSDNetworkCollector
from distronode.module_utils.facts.network.openbsd import OpenBSDNetworkCollector
from distronode.module_utils.facts.network.sunos import SunOSNetworkCollector

from distronode.module_utils.facts.virtual.base import VirtualCollector
from distronode.module_utils.facts.virtual.dragonfly import DragonFlyVirtualCollector
from distronode.module_utils.facts.virtual.freebsd import FreeBSDVirtualCollector
from distronode.module_utils.facts.virtual.hpux import HPUXVirtualCollector
from distronode.module_utils.facts.virtual.linux import LinuxVirtualCollector
from distronode.module_utils.facts.virtual.netbsd import NetBSDVirtualCollector
from distronode.module_utils.facts.virtual.openbsd import OpenBSDVirtualCollector
from distronode.module_utils.facts.virtual.sunos import SunOSVirtualCollector

# these should always be first due to most other facts depending on them
_base = [
    PlatformFactCollector,
    DistributionFactCollector,
    LSBFactCollector
]  # type: t.List[t.Type[BaseFactCollector]]

# These restrict what is possible in others
_restrictive = [
    SelinuxFactCollector,
    ApparmorFactCollector,
    ChrootFactCollector,
    FipsFactCollector
]  # type: t.List[t.Type[BaseFactCollector]]

# general info, not required but probably useful for other facts
_general = [
    PythonFactCollector,
    SystemCapabilitiesFactCollector,
    PkgMgrFactCollector,
    OpenBSDPkgMgrFactCollector,
    ServiceMgrFactCollector,
    CmdLineFactCollector,
    DateTimeFactCollector,
    EnvFactCollector,
    LoadAvgFactCollector,
    SshPubKeyFactCollector,
    UserFactCollector,
    SystemdFactCollector
]  # type: t.List[t.Type[BaseFactCollector]]

# virtual, this might also limit hardware/networking
_virtual = [
    VirtualCollector,
    DragonFlyVirtualCollector,
    FreeBSDVirtualCollector,
    LinuxVirtualCollector,
    OpenBSDVirtualCollector,
    NetBSDVirtualCollector,
    SunOSVirtualCollector,
    HPUXVirtualCollector
]  # type: t.List[t.Type[BaseFactCollector]]

_hardware = [
    HardwareCollector,
    AIXHardwareCollector,
    DarwinHardwareCollector,
    DragonFlyHardwareCollector,
    FreeBSDHardwareCollector,
    HPUXHardwareCollector,
    HurdHardwareCollector,
    LinuxHardwareCollector,
    NetBSDHardwareCollector,
    OpenBSDHardwareCollector,
    SunOSHardwareCollector
]  # type: t.List[t.Type[BaseFactCollector]]

_network = [
    DnsFactCollector,
    FcWwnInitiatorFactCollector,
    NetworkCollector,
    AIXNetworkCollector,
    DarwinNetworkCollector,
    DragonFlyNetworkCollector,
    FreeBSDNetworkCollector,
    HPUXNetworkCollector,
    HurdNetworkCollector,
    IscsiInitiatorNetworkCollector,
    NvmeInitiatorNetworkCollector,
    LinuxNetworkCollector,
    NetBSDNetworkCollector,
    OpenBSDNetworkCollector,
    SunOSNetworkCollector
]  # type: t.List[t.Type[BaseFactCollector]]

# other fact sources
_extra_facts = [
    LocalFactCollector,
    FacterFactCollector,
    OhaiFactCollector
]  # type: t.List[t.Type[BaseFactCollector]]

# TODO: make config driven
collectors = _base + _restrictive + _general + _virtual + _hardware + _network + _extra_facts
