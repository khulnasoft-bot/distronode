#powershell

#Requires -Module Distronode.ModuleUtils.Legacy

$params = Parse-Args $args

$path = Get-DistronodeParam -Obj $params -Name path -Type path

Exit-Json @{ path = $path }
