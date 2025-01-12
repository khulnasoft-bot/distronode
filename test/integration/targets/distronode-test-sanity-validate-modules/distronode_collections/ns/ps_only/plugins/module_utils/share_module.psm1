#DistronodeRequires -CSharpUtil Distronode.Basic

Function Invoke-DistronodeModule {
    <#
        .SYNOPSIS
        validate
    #>
    [CmdletBinding()]
    param ()

    $module = [Distronode.Basic.DistronodeModule]::Create(@(), @{
            options = @{
                test = @{ type = 'str' }
            }
        })
    $module.ExitJson()
}

Export-ModuleMember -Function Invoke-DistronodeModule
