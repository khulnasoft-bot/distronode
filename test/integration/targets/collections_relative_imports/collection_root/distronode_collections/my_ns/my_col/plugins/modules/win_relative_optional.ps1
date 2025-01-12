#!powershell

#DistronodeRequires -CSharpUtil Distronode.Basic -Optional
#DistronodeRequires -PowerShell ..module_utils.PSRel4 -optional

# These do not exist
#DistronodeRequires -CSharpUtil ..invalid_package.name -Optional
#DistronodeRequires -CSharpUtil ..module_utils.InvalidName -optional
#DistronodeRequires -PowerShell ..invalid_package.pwsh_name -optional
#DistronodeRequires -PowerShell ..module_utils.InvalidPwshName -Optional


$module = [Distronode.Basic.DistronodeModule]::Create($args, @{})

$module.Result.data = Invoke-FromPSRel4

$module.ExitJson()
