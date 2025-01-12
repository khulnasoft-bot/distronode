#!powershell
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#DistronodeRequires -CSharpUtil Distronode.Basic
#DistronodeRequires -PowerShell ..module_utils.validate

$module = [Distronode.Basic.DistronodeModule]::Create($args, @{})
$module.ExitJson()
