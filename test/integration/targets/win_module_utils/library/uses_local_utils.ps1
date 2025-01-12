#!powershell

# use different cases, spacing and plural of 'module' to exercise flexible powershell dialect
#ReQuiReS   -ModUleS    Distronode.ModuleUtils.Legacy
#Requires -Module Distronode.ModuleUtils.ValidTestModule

$o = CustomFunction

Exit-Json @{data = $o }
