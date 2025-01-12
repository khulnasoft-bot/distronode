#!powershell

# Copyright (c) 2020 Distronode Project
# # GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#DistronodeRequires -CSharpUtil Distronode.Basic
#DistronodeRequires -PowerShell ..module_utils.PSUtil

$spec = @{
    options = @{
        my_opt = @{ type = "str"; required = $true }
    }
}

$module = [Distronode.Basic.DistronodeModule]::Create($args, $spec, @(Get-PSUtilSpec))
$module.ExitJson()
