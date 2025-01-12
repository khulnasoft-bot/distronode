#!powershell
# Copyright: (c) Distronode Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#DistronodeRequires -CSharpUtil Distronode.Basic

$spec = @{
    options = @{
        hello = @{ type = 'str'; required = $true }
    }
    supports_check_mode = $true
}

$module = [Distronode.Basic.DistronodeModule]::Create($args, $spec)

$hello = $module.Params.hello

$module.Result.msg = $hello
$module.Result.changed = $false

$module.ExitJson()
