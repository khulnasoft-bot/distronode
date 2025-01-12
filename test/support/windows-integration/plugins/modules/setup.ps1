#!powershell

# Copyright: (c) 2018, Distronode Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#Requires -Module Distronode.ModuleUtils.Legacy

Function Get-CustomFacts {
  [cmdletBinding()]
  param (
    [Parameter(mandatory=$false)]
    $factpath = $null
  )

  if (Test-Path -Path $factpath) {
    $FactsFiles = Get-ChildItem -Path $factpath | Where-Object -FilterScript {($PSItem.PSIsContainer -eq $false) -and ($PSItem.Extension -eq '.ps1')}

    foreach ($FactsFile in $FactsFiles) {
        $out = & $($FactsFile.FullName)
        $result.distronode_facts.Add("distronode_$(($FactsFile.Name).Split('.')[0])", $out)
    }
  }
  else
  {
        Add-Warning $result "Non existing path was set for local facts - $factpath"
  }
}

Function Get-MachineSid {
    # The Machine SID is stored in HKLM:\SECURITY\SAM\Domains\Account and is
    # only accessible by the Local System account. This method get's the local
    # admin account (ends with -500) and lops it off to get the machine sid.

    $machine_sid = $null

    try {
        $admins_sid = "S-1-5-32-544"
    $admin_group = ([Security.Principal.SecurityIdentifier]$admins_sid).Translate([Security.Principal.NTAccount]).Value

        Add-Type -AssemblyName System.DirectoryServices.AccountManagement
        $principal_context = New-Object -TypeName System.DirectoryServices.AccountManagement.PrincipalContext([System.DirectoryServices.AccountManagement.ContextType]::Machine)
        $group_principal = New-Object -TypeName System.DirectoryServices.AccountManagement.GroupPrincipal($principal_context, $admin_group)
        $searcher = New-Object -TypeName System.DirectoryServices.AccountManagement.PrincipalSearcher($group_principal)
        $groups = $searcher.FindOne()

        foreach ($user in $groups.Members) {
            $user_sid = $user.Sid
            if ($user_sid.Value.EndsWith("-500")) {
                $machine_sid = $user_sid.AccountDomainSid.Value
                break
            }
        }
    } catch {
        #can fail for any number of reasons, if it does just return the original null
        Add-Warning -obj $result -message "Error during machine sid retrieval: $($_.Exception.Message)"
    }

    return $machine_sid
}

$cim_instances = @{}

Function Get-LazyCimInstance([string]$instance_name, [string]$namespace="Root\CIMV2") {
    if(-not $cim_instances.ContainsKey($instance_name)) {
        $cim_instances[$instance_name] = $(Get-CimInstance -Namespace $namespace -ClassName $instance_name)
    }

    return $cim_instances[$instance_name]
}

$result = @{
    distronode_facts = @{ }
    changed = $false
}

$grouped_subsets = @{
    min=[System.Collections.Generic.List[string]]@('date_time','distribution','dns','env','local','platform','powershell_version','user')
    network=[System.Collections.Generic.List[string]]@('all_ipv4_addresses','all_ipv6_addresses','interfaces','windows_domain', 'winrm')
    hardware=[System.Collections.Generic.List[string]]@('bios','memory','processor','uptime','virtual')
    external=[System.Collections.Generic.List[string]]@('facter')
}

# build "all" set from everything mentioned in the group- this means every value must be in at least one subset to be considered legal
$all_set = [System.Collections.Generic.HashSet[string]]@()

foreach($kv in $grouped_subsets.GetEnumerator()) {
    [void] $all_set.UnionWith($kv.Value)
}

# dynamically create an "all" subset now that we know what should be in it
$grouped_subsets['all'] = [System.Collections.Generic.List[string]]$all_set

# start with all, build up gather and exclude subsets
$gather_subset = [System.Collections.Generic.HashSet[string]]$grouped_subsets.all
$explicit_subset = [System.Collections.Generic.HashSet[string]]@()
$exclude_subset = [System.Collections.Generic.HashSet[string]]@()

$params = Parse-Args $args -supports_check_mode $true
$factpath = Get-DistronodeParam -obj $params -name "fact_path" -type "path"
$gather_subset_source = Get-DistronodeParam -obj $params -name "gather_subset" -type "list" -default "all"

foreach($item in $gather_subset_source) {
    if(([string]$item).StartsWith("!")) {
        $item = ([string]$item).Substring(1)
        if($item -eq "all") {
            $all_minus_min = [System.Collections.Generic.HashSet[string]]@($all_set)
            [void] $all_minus_min.ExceptWith($grouped_subsets.min)
            [void] $exclude_subset.UnionWith($all_minus_min)
        }
        elseif($grouped_subsets.ContainsKey($item)) {
            [void] $exclude_subset.UnionWith($grouped_subsets[$item])
        }
        elseif($all_set.Contains($item)) {
            [void] $exclude_subset.Add($item)
        }
        # NB: invalid exclude values are ignored, since that's what posix setup does
    }
    else {
        if($grouped_subsets.ContainsKey($item)) {
            [void] $explicit_subset.UnionWith($grouped_subsets[$item])
        }
        elseif($all_set.Contains($item)) {
            [void] $explicit_subset.Add($item)
        }
        else {
            # NB: POSIX setup fails on invalid value; we warn, because we don't implement the same set as POSIX
            # and we don't have platform-specific config for this...
            Add-Warning $result "invalid value $item specified in gather_subset"
        }
    }
}

[void] $gather_subset.ExceptWith($exclude_subset)
[void] $gather_subset.UnionWith($explicit_subset)

$distronode_facts = @{
    gather_subset=@($gather_subset_source)
    module_setup=$true
}

$osversion = [Environment]::OSVersion

if ($osversion.Version -lt [version]"6.2") {
    # Server 2008, 2008 R2, and Windows 7 are not tested in CI and we want to let customers know about it before
    # removing support altogether.
    $version_string = "{0}.{1}" -f ($osversion.Version.Major, $osversion.Version.Minor)
    $msg = "Windows version '$version_string' will no longer be supported or tested in the next Distronode release"
    Add-DeprecationWarning -obj $result -message $msg -version "2.11"
}

if($gather_subset.Contains('all_ipv4_addresses') -or $gather_subset.Contains('all_ipv6_addresses')) {
    $netcfg = Get-LazyCimInstance Win32_NetworkAdapterConfiguration

    # TODO: split v4/v6 properly, return in separate keys
    $ips = @()
    Foreach ($ip in $netcfg.IPAddress) {
        If ($ip) {
            $ips += $ip
        }
    }

    $distronode_facts += @{
        distronode_ip_addresses = $ips
    }
}

if($gather_subset.Contains('bios')) {
    $win32_bios = Get-LazyCimInstance Win32_Bios
    $win32_cs = Get-LazyCimInstance Win32_ComputerSystem
    $distronode_facts += @{
        distronode_bios_date = $win32_bios.ReleaseDate.ToString("MM/dd/yyyy")
        distronode_bios_version = $win32_bios.SMBIOSBIOSVersion
        distronode_product_name = $win32_cs.Model.Trim()
        distronode_product_serial = $win32_bios.SerialNumber
        # distronode_product_version = ([string] $win32_cs.SystemFamily)
    }
}

if($gather_subset.Contains('date_time')) {
    $datetime = (Get-Date)
    $datetime_utc = $datetime.ToUniversalTime()
    $date = @{
        date = $datetime.ToString("yyyy-MM-dd")
        day = $datetime.ToString("dd")
        epoch = (Get-Date -UFormat "%s")
        hour = $datetime.ToString("HH")
        iso8601 = $datetime_utc.ToString("yyyy-MM-ddTHH:mm:ssZ")
        iso8601_basic = $datetime.ToString("yyyyMMddTHHmmssffffff")
        iso8601_basic_short = $datetime.ToString("yyyyMMddTHHmmss")
        iso8601_micro = $datetime_utc.ToString("yyyy-MM-ddTHH:mm:ss.ffffffZ")
        minute = $datetime.ToString("mm")
        month = $datetime.ToString("MM")
        second = $datetime.ToString("ss")
        time = $datetime.ToString("HH:mm:ss")
        tz = ([System.TimeZoneInfo]::Local.Id)
        tz_offset = $datetime.ToString("zzzz")
        # Ensure that the weekday is in English
        weekday = $datetime.ToString("dddd", [System.Globalization.CultureInfo]::InvariantCulture)
        weekday_number = (Get-Date -UFormat "%w")
        weeknumber = (Get-Date -UFormat "%W")
        year = $datetime.ToString("yyyy")
    }

    $distronode_facts += @{
        distronode_date_time = $date
    }
}

if($gather_subset.Contains('distribution')) {
    $win32_os = Get-LazyCimInstance Win32_OperatingSystem
    $product_type = switch($win32_os.ProductType) {
        1 { "workstation" }
        2 { "domain_controller" }
        3 { "server" }
        default { "unknown" }
    }

    $installation_type = $null
    $current_version_path = "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion"
    if (Test-Path -LiteralPath $current_version_path) {
        $install_type_prop = Get-ItemProperty -LiteralPath $current_version_path -ErrorAction SilentlyContinue
        $installation_type = [String]$install_type_prop.InstallationType
    }

    $distronode_facts += @{
        distronode_distribution = $win32_os.Caption
        distronode_distribution_version = $osversion.Version.ToString()
        distronode_distribution_major_version = $osversion.Version.Major.ToString()
        distronode_os_family = "Windows"
        distronode_os_name = ($win32_os.Name.Split('|')[0]).Trim()
        distronode_os_product_type = $product_type
        distronode_os_installation_type = $installation_type
    }
}

if($gather_subset.Contains('env')) {
    $env_vars = @{ }
    foreach ($item in Get-ChildItem Env:) {
        $name = $item | Select-Object -ExpandProperty Name
        # Powershell ConvertTo-Json fails if string ends with \
        $value = ($item | Select-Object -ExpandProperty Value).TrimEnd("\")
        $env_vars.Add($name, $value)
    }

    $distronode_facts += @{
        distronode_env = $env_vars
    }
}

if($gather_subset.Contains('facter')) {
    # See if Facter is on the System Path
    Try {
        Get-Command facter -ErrorAction Stop > $null
        $facter_installed = $true
    } Catch {
        $facter_installed = $false
    }

    # Get JSON from Facter, and parse it out.
    if ($facter_installed) {
        &facter -j | Tee-Object  -Variable facter_output > $null
        $facts = "$facter_output" | ConvertFrom-Json
        ForEach($fact in $facts.PSObject.Properties) {
            $fact_name = $fact.Name
            $distronode_facts.Add("facter_$fact_name", $fact.Value)
        }
    }
}

if($gather_subset.Contains('interfaces')) {
    $netcfg = Get-LazyCimInstance Win32_NetworkAdapterConfiguration
    $ActiveNetcfg = @()
    $ActiveNetcfg += $netcfg | Where-Object {$_.ipaddress -ne $null}

    $namespaces = Get-LazyCimInstance __Namespace -namespace root
    if ($namespaces | Where-Object { $_.Name -eq "StandardCimv" }) {
        $net_adapters = Get-LazyCimInstance MSFT_NetAdapter -namespace Root\StandardCimv2
        $guid_key = "InterfaceGUID"
        $name_key = "Name"
    } else {
        $net_adapters = Get-LazyCimInstance Win32_NetworkAdapter
        $guid_key = "GUID"
        $name_key = "NetConnectionID"
    }

    $formattednetcfg = @()
    foreach ($adapter in $ActiveNetcfg)
    {
        $thisadapter = @{
            default_gateway = $null
            connection_name = $null
            dns_domain = $adapter.dnsdomain
            interface_index = $adapter.InterfaceIndex
            interface_name = $adapter.description
            macaddress = $adapter.macaddress
        }

        if ($adapter.defaultIPGateway)
        {
            $thisadapter.default_gateway = $adapter.DefaultIPGateway[0].ToString()
        }
        $net_adapter = $net_adapters | Where-Object { $_.$guid_key -eq $adapter.SettingID }
        if ($net_adapter) {
            $thisadapter.connection_name = $net_adapter.$name_key
        }

        $formattednetcfg += $thisadapter
    }

    $distronode_facts += @{
        distronode_interfaces = $formattednetcfg
    }
}

if ($gather_subset.Contains("local") -and $null -ne $factpath) {
    # Get any custom facts; results are updated in the
    Get-CustomFacts -factpath $factpath
}

if($gather_subset.Contains('memory')) {
    $win32_cs = Get-LazyCimInstance Win32_ComputerSystem
    $win32_os = Get-LazyCimInstance Win32_OperatingSystem
    $distronode_facts += @{
        # Win32_PhysicalMemory is empty on some virtual platforms
        distronode_memtotal_mb = ([math]::ceiling($win32_cs.TotalPhysicalMemory / 1024 / 1024))
        distronode_memfree_mb = ([math]::ceiling($win32_os.FreePhysicalMemory / 1024))
        distronode_swaptotal_mb = ([math]::round($win32_os.TotalSwapSpaceSize / 1024))
        distronode_pagefiletotal_mb = ([math]::round($win32_os.SizeStoredInPagingFiles / 1024))
        distronode_pagefilefree_mb = ([math]::round($win32_os.FreeSpaceInPagingFiles / 1024))
    }
}


if($gather_subset.Contains('platform')) {
    $win32_cs = Get-LazyCimInstance Win32_ComputerSystem
    $win32_os = Get-LazyCimInstance Win32_OperatingSystem
    $domain_suffix = $win32_cs.Domain.Substring($win32_cs.Workgroup.length)
    $fqdn = $win32_cs.DNSHostname

    if( $domain_suffix -ne "")
    {
        $fqdn = $win32_cs.DNSHostname + "." + $domain_suffix
    }

    try {
        $distronode_reboot_pending = Get-PendingRebootStatus
    } catch {
        # fails for non-admin users, set to null in this case
        $distronode_reboot_pending = $null
    }

    $distronode_facts += @{
        distronode_architecture = $win32_os.OSArchitecture
        distronode_domain = $domain_suffix
        distronode_fqdn = $fqdn
        distronode_hostname = $win32_cs.DNSHostname
        distronode_netbios_name = $win32_cs.Name
        distronode_kernel = $osversion.Version.ToString()
        distronode_nodename = $fqdn
        distronode_machine_id = Get-MachineSid
        distronode_owner_contact = ([string] $win32_cs.PrimaryOwnerContact)
        distronode_owner_name = ([string] $win32_cs.PrimaryOwnerName)
        # FUTURE: should this live in its own subset?
        distronode_reboot_pending = $distronode_reboot_pending
        distronode_system = $osversion.Platform.ToString()
        distronode_system_description = ([string] $win32_os.Description)
        distronode_system_vendor = $win32_cs.Manufacturer
    }
}

if($gather_subset.Contains('powershell_version')) {
    $distronode_facts += @{
        distronode_powershell_version = ($PSVersionTable.PSVersion.Major)
    }
}

if($gather_subset.Contains('processor')) {
    $win32_cs = Get-LazyCimInstance Win32_ComputerSystem
    $win32_cpu = Get-LazyCimInstance Win32_Processor
    if ($win32_cpu -is [array]) {
        # multi-socket, pick first
        $win32_cpu = $win32_cpu[0]
    }

    $cpu_list = @( )
    for ($i=1; $i -le $win32_cs.NumberOfLogicalProcessors; $i++) {
        $cpu_list += $win32_cpu.Manufacturer
        $cpu_list += $win32_cpu.Name
    }

    $distronode_facts += @{
        distronode_processor = $cpu_list
        distronode_processor_cores = $win32_cpu.NumberOfCores
        distronode_processor_count = $win32_cs.NumberOfProcessors
        distronode_processor_threads_per_core = ($win32_cpu.NumberOfLogicalProcessors / $win32_cpu.NumberofCores)
        distronode_processor_vcpus = $win32_cs.NumberOfLogicalProcessors
    }
}

if($gather_subset.Contains('uptime')) {
    $win32_os = Get-LazyCimInstance Win32_OperatingSystem
    $distronode_facts += @{
        distronode_lastboot = $win32_os.lastbootuptime.ToString("u")
        distronode_uptime_seconds = $([System.Convert]::ToInt64($(Get-Date).Subtract($win32_os.lastbootuptime).TotalSeconds))
    }
}

if($gather_subset.Contains('user')) {
    $user = [Security.Principal.WindowsIdentity]::GetCurrent()
    $distronode_facts += @{
        distronode_user_dir = $env:userprofile
        # Win32_UserAccount.FullName is probably the right thing here, but it can be expensive to get on large domains
        distronode_user_gecos = ""
        distronode_user_id = $env:username
        distronode_user_sid = $user.User.Value
    }
}

if($gather_subset.Contains('windows_domain')) {
    $win32_cs = Get-LazyCimInstance Win32_ComputerSystem
    $domain_roles = @{
        0 = "Stand-alone workstation"
        1 = "Member workstation"
        2 = "Stand-alone server"
        3 = "Member server"
        4 = "Backup domain controller"
        5 = "Primary domain controller"
    }

    $domain_role = $domain_roles.Get_Item([Int32]$win32_cs.DomainRole)

    $distronode_facts += @{
        distronode_windows_domain = $win32_cs.Domain
        distronode_windows_domain_member = $win32_cs.PartOfDomain
        distronode_windows_domain_role = $domain_role
    }
}

if($gather_subset.Contains('winrm')) {

    $winrm_https_listener_parent_paths = Get-ChildItem -Path WSMan:\localhost\Listener -Recurse -ErrorAction SilentlyContinue | `
        Where-Object {$_.PSChildName -eq "Transport" -and $_.Value -eq "HTTPS"} | Select-Object PSParentPath
    if ($winrm_https_listener_parent_paths -isnot [array]) {
       $winrm_https_listener_parent_paths = @($winrm_https_listener_parent_paths)
    }

    $winrm_https_listener_paths = @()
    foreach ($winrm_https_listener_parent_path in $winrm_https_listener_parent_paths) {
        $winrm_https_listener_paths += $winrm_https_listener_parent_path.PSParentPath.Substring($winrm_https_listener_parent_path.PSParentPath.LastIndexOf("\"))
    }

    $https_listeners = @()
    foreach ($winrm_https_listener_path in $winrm_https_listener_paths) {
        $https_listeners += Get-ChildItem -Path "WSMan:\localhost\Listener$winrm_https_listener_path"
    }

    $winrm_cert_thumbprints = @()
    foreach ($https_listener in $https_listeners) {
        $winrm_cert_thumbprints += $https_listener | Where-Object {$_.Name -EQ "CertificateThumbprint" } | Select-Object Value
    }

    $winrm_cert_expiry = @()
    foreach ($winrm_cert_thumbprint in $winrm_cert_thumbprints) {
        Try {
            $winrm_cert_expiry += Get-ChildItem -Path Cert:\LocalMachine\My | Where-Object Thumbprint -EQ $winrm_cert_thumbprint.Value.ToString().ToUpper() | Select-Object NotAfter
        } Catch {
            Add-Warning -obj $result -message "Error during certificate expiration retrieval: $($_.Exception.Message)"
        }
    }

    $winrm_cert_expirations = $winrm_cert_expiry | Sort-Object NotAfter
    if ($winrm_cert_expirations) {
        # this fact was renamed from distronode_winrm_certificate_expires due to collision with distronode_winrm_X connection var pattern
        $distronode_facts.Add("distronode_win_rm_certificate_expires", $winrm_cert_expirations[0].NotAfter.ToString("yyyy-MM-dd HH:mm:ss"))
    }
}

if($gather_subset.Contains('virtual')) {
    $machine_info = Get-LazyCimInstance Win32_ComputerSystem

    switch ($machine_info.model) {
        "Virtual Machine" {
            $machine_type="Hyper-V"
            $machine_role="guest"
        }

        "VMware Virtual Platform" {
            $machine_type="VMware"
            $machine_role="guest"
        }

        "VirtualBox" {
            $machine_type="VirtualBox"
            $machine_role="guest"
        }

        "HVM domU" {
            $machine_type="Xen"
            $machine_role="guest"
        }

        default {
            $machine_type="NA"
            $machine_role="NA"
        }
    }

    $distronode_facts += @{
        distronode_virtualization_role = $machine_role
        distronode_virtualization_type = $machine_type
    }
}

$result.distronode_facts += $distronode_facts

Exit-Json $result
