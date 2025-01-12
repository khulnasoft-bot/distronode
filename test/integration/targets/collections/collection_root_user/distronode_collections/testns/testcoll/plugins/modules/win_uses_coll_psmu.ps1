#!powershell

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#DistronodeRequires -CSharpUtil Distronode.Basic
#DistronodeRequires -Powershell distronode_collections.testns.testcoll.plugins.module_utils.MyPSMU
#DistronodeRequires -PowerShell distronode_collections.testns.testcoll.plugins.module_utils.subpkg.subps

$spec = @{
    options = @{
        data = @{ type = "str"; default = "called from $(Invoke-FromUserPSMU)" }
    }
    supports_check_mode = $true
}
$module = [Distronode.Basic.DistronodeModule]::Create($args, $spec)
$data = $module.Params.data

if ($data -eq "crash") {
    throw "boom"
}

$module.Result.ping = $data
$module.Result.source = "user"
$module.Result.subpkg = Invoke-SubUserPSMU
$module.ExitJson()
