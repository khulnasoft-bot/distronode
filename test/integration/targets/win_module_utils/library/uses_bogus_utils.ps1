#!powershell

# this should fail
#Requires -Module Distronode.ModuleUtils.BogusModule

Exit-Json @{ data = "success" }
