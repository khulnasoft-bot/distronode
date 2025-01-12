# Copyright (c) 2018 Distronode Project
# Simplified BSD License (see licenses/simplified_bsd.txt or https://opensource.org/licenses/BSD-2-Clause)

#DistronodeRequires -CSharpUtil Distronode.Privilege

Function Get-DistronodePrivilege {
    <#
    .SYNOPSIS
    Get the status of a privilege for the current process. This returns
        $true - the privilege is enabled
        $false - the privilege is disabled
        $null - the privilege is removed from the token

    If Name is not a valid privilege name, this will throw an
    ArgumentException.

    .EXAMPLE
    Get-DistronodePrivilege -Name SeDebugPrivilege
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)][String]$Name
    )

    if (-not [Distronode.Privilege.PrivilegeUtil]::CheckPrivilegeName($Name)) {
        throw [System.ArgumentException] "Invalid privilege name '$Name'"
    }

    $process_token = [Distronode.Privilege.PrivilegeUtil]::GetCurrentProcess()
    $privilege_info = [Distronode.Privilege.PrivilegeUtil]::GetAllPrivilegeInfo($process_token)
    if ($privilege_info.ContainsKey($Name)) {
        $status = $privilege_info.$Name
        return $status.HasFlag([Distronode.Privilege.PrivilegeAttributes]::Enabled)
    }
    else {
        return $null
    }
}

Function Set-DistronodePrivilege {
    <#
    .SYNOPSIS
    Enables/Disables a privilege on the current process' token. If a privilege
    has been removed from the process token, this will throw an
    InvalidOperationException.

    .EXAMPLE
    # enable a privilege
    Set-DistronodePrivilege -Name SeCreateSymbolicLinkPrivilege -Value $true

    # disable a privilege
    Set-DistronodePrivilege -Name SeCreateSymbolicLinkPrivilege -Value $false
    #>
    [CmdletBinding(SupportsShouldProcess)]
    param(
        [Parameter(Mandatory = $true)][String]$Name,
        [Parameter(Mandatory = $true)][bool]$Value
    )

    $action = switch ($Value) {
        $true { "Enable" }
        $false { "Disable" }
    }

    $current_state = Get-DistronodePrivilege -Name $Name
    if ($current_state -eq $Value) {
        return  # no change needs to occur
    }
    elseif ($null -eq $current_state) {
        # once a privilege is removed from a token we cannot do anything with it
        throw [System.InvalidOperationException] "Cannot $($action.ToLower()) the privilege '$Name' as it has been removed from the token"
    }

    $process_token = [Distronode.Privilege.PrivilegeUtil]::GetCurrentProcess()
    if ($PSCmdlet.ShouldProcess($Name, "$action the privilege $Name")) {
        $new_state = New-Object -TypeName 'System.Collections.Generic.Dictionary`2[[System.String], [System.Nullable`1[System.Boolean]]]'
        $new_state.Add($Name, $Value)
        [Distronode.Privilege.PrivilegeUtil]::SetTokenPrivileges($process_token, $new_state) > $null
    }
}

Export-ModuleMember -Function Get-DistronodePrivilege, Set-DistronodePrivilege

