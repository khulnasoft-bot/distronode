#!powershell

#Requires -Module Distronode.ModuleUtils.Legacy
#Requires -Module Distronode.ModuleUtils.SID
#Requires -Version 3.0
#DistronodeRequires -OSVersion 6
#DistronodeRequires -Become

$output = &whoami.exe
$sid = Convert-ToSID -account_name $output.Trim()

Exit-Json -obj @{ output = $sid; changed = $false }
