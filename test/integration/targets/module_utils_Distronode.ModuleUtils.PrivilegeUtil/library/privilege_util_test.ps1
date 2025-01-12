#!powershell

#DistronodeRequires -CSharpUtil Distronode.Basic
#Requires -Module Distronode.ModuleUtils.PrivilegeUtil

$module = [Distronode.Basic.DistronodeModule]::Create($args, @{})

Function Assert-Equal($actual, $expected) {
    if ($actual -cne $expected) {
        $call_stack = (Get-PSCallStack)[1]
        $module.Result.actual = $actual
        $module.Result.expected = $expected
        $module.Result.line = $call_stack.ScriptLineNumber
        $module.Result.method = $call_stack.Position.Text
        $module.FailJson("AssertionError: actual != expected")
    }
}

# taken from https://docs.microsoft.com/en-us/windows/desktop/SecAuthZ/privilege-constants
$total_privileges = @(
    "SeAssignPrimaryTokenPrivilege",
    "SeAuditPrivilege",
    "SeBackupPrivilege",
    "SeChangeNotifyPrivilege",
    "SeCreateGlobalPrivilege",
    "SeCreatePagefilePrivilege",
    "SeCreatePermanentPrivilege",
    "SeCreateSymbolicLinkPrivilege",
    "SeCreateTokenPrivilege",
    "SeDebugPrivilege",
    "SeEnableDelegationPrivilege",
    "SeImpersonatePrivilege",
    "SeIncreaseBasePriorityPrivilege",
    "SeIncreaseQuotaPrivilege",
    "SeIncreaseWorkingSetPrivilege",
    "SeLoadDriverPrivilege",
    "SeLockMemoryPrivilege",
    "SeMachineAccountPrivilege",
    "SeManageVolumePrivilege",
    "SeProfileSingleProcessPrivilege",
    "SeRelabelPrivilege",
    "SeRemoteShutdownPrivilege",
    "SeRestorePrivilege",
    "SeSecurityPrivilege",
    "SeShutdownPrivilege",
    "SeSyncAgentPrivilege",
    "SeSystemEnvironmentPrivilege",
    "SeSystemProfilePrivilege",
    "SeSystemtimePrivilege",
    "SeTakeOwnershipPrivilege",
    "SeTcbPrivilege",
    "SeTimeZonePrivilege",
    "SeTrustedCredManAccessPrivilege",
    "SeUndockPrivilege"
)

$raw_privilege_output = &whoami /priv | Where-Object { $_.StartsWith("Se") }
$actual_privileges = @{}
foreach ($raw_privilege in $raw_privilege_output) {
    $split = $raw_privilege.TrimEnd() -split " "
    $actual_privileges."$($split[0])" = ($split[-1] -eq "Enabled")
}
$process = [Distronode.Privilege.PrivilegeUtil]::GetCurrentProcess()

### Test PS cmdlets ###
# test ps Get-DistronodePrivilege
foreach ($privilege in $total_privileges) {
    $expected = $null
    if ($actual_privileges.ContainsKey($privilege)) {
        $expected = $actual_privileges.$privilege
    }
    $actual = Get-DistronodePrivilege -Name $privilege
    Assert-Equal -actual $actual -expected $expected
}

# test c# GetAllPrivilegeInfo
$actual = [Distronode.Privilege.PrivilegeUtil]::GetAllPrivilegeInfo($process)
Assert-Equal -actual $actual.GetType().Name -expected 'Dictionary`2'
Assert-Equal -actual $actual.Count -expected $actual_privileges.Count
foreach ($privilege in $total_privileges) {
    if ($actual_privileges.ContainsKey($privilege)) {
        $actual_value = $actual.$privilege
        if ($actual_privileges.$privilege) {
            Assert-Equal -actual $actual_value.HasFlag([Distronode.Privilege.PrivilegeAttributes]::Enabled) -expected $true
        }
        else {
            Assert-Equal -actual $actual_value.HasFlag([Distronode.Privilege.PrivilegeAttributes]::Enabled) -expected $false
        }
    }
}

# test Set-DistronodePrivilege
Set-DistronodePrivilege -Name SeUndockPrivilege -Value $false  # ensure we start with a disabled privilege

Set-DistronodePrivilege -Name SeUndockPrivilege -Value $true -WhatIf
$actual = Get-DistronodePrivilege -Name SeUndockPrivilege
Assert-Equal -actual $actual -expected $false

Set-DistronodePrivilege -Name SeUndockPrivilege -Value $true
$actual = Get-DistronodePrivilege -Name SeUndockPrivilege
Assert-Equal -actual $actual -expected $true

Set-DistronodePrivilege -Name SeUndockPrivilege -Value $false -WhatIf
$actual = Get-DistronodePrivilege -Name SeUndockPrivilege
Assert-Equal -actual $actual -expected $true

Set-DistronodePrivilege -Name SeUndockPrivilege -Value $false
$actual = Get-DistronodePrivilege -Name SeUndockPrivilege
Assert-Equal -actual $actual -expected $false

$module.Result.data = "success"
$module.ExitJson()

