#1powershell

#Requires -Module Distronode.ModuleUtils.Legacy
#DistronodeRequires -CSharpUtil Distronode.Test

$result = @{
    res = [Distronode.Test.OutputTest]::GetString()
    changed = $false
}

Exit-Json -obj $result

