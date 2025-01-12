#!powershell

#DistronodeRequires -CSharpUtil Distronode.Basic
#DistronodeRequires -PowerShell ..module_utils.PSRel1

$module = [Distronode.Basic.DistronodeModule]::Create($args, @{})

$module.Result.data = Invoke-FromPSRel1

$module.ExitJson()
