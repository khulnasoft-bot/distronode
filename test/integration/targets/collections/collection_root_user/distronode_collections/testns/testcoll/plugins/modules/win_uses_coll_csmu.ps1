#!powershell

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#DistronodeRequires -CSharpUtil Distronode.Basic
#DistronodeRequires -CSharpUtil distronode_collections.testns.testcoll.plugins.module_utils.MyCSMU
#DistronodeRequires -CSharpUtil distronode_collections.testns.testcoll.plugins.module_utils.subpkg.subcs

$spec = @{
    options = @{
        data = @{ type = "str"; default = "called from $([distronode_collections.testns.testcoll.plugins.module_utils.MyCSMU.CustomThing]::HelloWorld())" }
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
$module.Result.subpkg = [distronode_collections.testns.testcoll.plugins.module_utils.subpkg.subcs.NestedUtil]::HelloWorld()
$module.Result.type_accelerator = "called from $([MyCSMU]::HelloWorld())"
$module.ExitJson()
