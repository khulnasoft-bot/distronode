#!powershell

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# Test builtin C# still works with -Optional
#DistronodeRequires -CSharpUtil Distronode.Basic -Optional

# Test no failure when importing an invalid builtin C# and pwsh util with -Optional
#DistronodeRequires -CSharpUtil Distronode.Invalid -Optional
#DistronodeRequires -PowerShell Distronode.ModuleUtils.Invalid -Optional

# Test valid module_util still works with -Optional
#DistronodeRequires -CSharpUtil distronode_collections.testns.testcoll.plugins.module_utils.MyCSMUOptional -Optional
#DistronodeRequires -Powershell distronode_collections.testns.testcoll.plugins.module_utils.MyPSMUOptional -Optional

# Test no failure when importing an invalid collection C# and pwsh util with -Optional
#DistronodeRequires -CSharpUtil distronode_collections.testns.testcoll.plugins.module_utils.invalid -Optional
#DistronodeRequires -CSharpUtil distronode_collections.testns.testcoll.plugins.module_utils.invalid.invalid -Optional
#DistronodeRequires -Powershell distronode_collections.testns.testcoll.plugins.module_utils.invalid -Optional
#DistronodeRequires -Powershell distronode_collections.testns.testcoll.plugins.module_utils.invalid.invalid -Optional

$spec = @{
    options = @{
        data = @{ type = "str"; default = "called $(Invoke-FromUserPSMU)" }
    }
    supports_check_mode = $true
}
$module = [Distronode.Basic.DistronodeModule]::Create($args, $spec)

$module.Result.data = $module.Params.data
$module.Result.csharp = [MyCSMU]::HelloWorld()

$module.ExitJson()
