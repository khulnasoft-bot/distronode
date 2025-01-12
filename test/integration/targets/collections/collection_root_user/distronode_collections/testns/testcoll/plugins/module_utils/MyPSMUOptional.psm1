#DistronodeRequires -CSharpUtil Distronode.Invalid -Optional
#DistronodeRequires -Powershell Distronode.ModuleUtils.Invalid -Optional
#DistronodeRequires -CSharpUtil distronode_collections.testns.testcoll.plugins.module_utils.invalid -Optional
#DistronodeRequires -CSharpUtil distronode_collections.testns.testcoll.plugins.module_utils.invalid.invalid -Optional
#DistronodeRequires -Powershell distronode_collections.testns.testcoll.plugins.module_utils.invalid -Optional
#DistronodeRequires -Powershell distronode_collections.testns.testcoll.plugins.module_utils.invalid.invalid -Optional

Function Invoke-FromUserPSMU {
    <#
    .SYNOPSIS
    Test function
    #>
    return "from optional user_mu"
}

Export-ModuleMember -Function Invoke-FromUserPSMU
