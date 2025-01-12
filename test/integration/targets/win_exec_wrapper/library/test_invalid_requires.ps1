#!powershell

#Requires -Module Distronode.ModuleUtils.Legacy
# Requires -Version 20
# DistronodeRequires -OSVersion 20

# requires statement must be straight after the original # with now space, this module won't fail

Exit-Json -obj @{ output = "output"; changed = $false }
