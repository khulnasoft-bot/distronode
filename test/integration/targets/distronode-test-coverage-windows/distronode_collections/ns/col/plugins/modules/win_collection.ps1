#!powershell

#DistronodeRequires -CSharpUtil Distronode.Basic

$module = [Distronode.Basic.DistronodeModule]::Create($args, @{})
$module.ExitJson()
