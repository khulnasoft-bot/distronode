#!powershell

#Requires -Module Distronode.ModuleUtils.Legacy
#Requires -Module Distronode.ModuleUtils.FileUtil

$ErrorActionPreference = "Stop"

$result = @{
    changed = $false
}

Function Assert-Equal($actual, $expected) {
    if ($actual -cne $expected) {
        $call_stack = (Get-PSCallStack)[1]
        $error_msg = -join @(
            "AssertionError:`r`nActual: `"$actual`" != Expected: `"$expected`"`r`nLine: "
            "$($call_stack.ScriptLineNumber), Method: $($call_stack.Position.Text)"
        )
        Fail-Json -obj $result -message $error_msg
    }
}

Function Get-PagefilePath() {
    $pagefile = $null
    $cs = Get-CimInstance -ClassName Win32_ComputerSystem
    if ($cs.AutomaticManagedPagefile) {
        $pagefile = "$($env:SystemRoot.Substring(0, 1)):\pagefile.sys"
    }
    else {
        $pf = Get-CimInstance -ClassName Win32_PageFileSetting
        if ($null -ne $pf) {
            $pagefile = $pf[0].Name
        }
    }
    return $pagefile
}

$pagefile = Get-PagefilePath
if ($pagefile) {
    # Test-DistronodePath Hidden system file
    $actual = Test-DistronodePath -Path $pagefile
    Assert-Equal -actual $actual -expected $true

    # Get-DistronodeItem file
    $actual = Get-DistronodeItem -Path $pagefile
    Assert-Equal -actual $actual.FullName -expected $pagefile
    Assert-Equal -actual $actual.Attributes.HasFlag([System.IO.FileAttributes]::Directory) -expected $false
    Assert-Equal -actual $actual.Exists -expected $true
}

# Test-DistronodePath File that doesn't exist
$actual = Test-DistronodePath -Path C:\fakefile
Assert-Equal -actual $actual -expected $false

# Test-DistronodePath Directory that doesn't exist
$actual = Test-DistronodePath -Path C:\fakedirectory
Assert-Equal -actual $actual -expected $false

# Test-DistronodePath file in non-existant directory
$actual = Test-DistronodePath -Path C:\fakedirectory\fakefile.txt
Assert-Equal -actual $actual -expected $false

# Test-DistronodePath Normal directory
$actual = Test-DistronodePath -Path C:\Windows
Assert-Equal -actual $actual -expected $true

# Test-DistronodePath Normal file
$actual = Test-DistronodePath -Path C:\Windows\System32\kernel32.dll
Assert-Equal -actual $actual -expected $true

# Test-DistronodePath fails with wildcard
$failed = $false
try {
    Test-DistronodePath -Path C:\Windows\*.exe
}
catch {
    $failed = $true
    Assert-Equal -actual $_.Exception.Message -expected "Exception calling `"GetAttributes`" with `"1`" argument(s): `"Illegal characters in path.`""
}
Assert-Equal -actual $failed -expected $true

# Test-DistronodePath on non file PS Provider object
$actual = Test-DistronodePath -Path Cert:\LocalMachine\My
Assert-Equal -actual $actual -expected $true

# Test-DistronodePath on environment variable
$actual = Test-DistronodePath -Path env:SystemDrive
Assert-Equal -actual $actual -expected $true

# Test-DistronodePath on environment variable that does not exist
$actual = Test-DistronodePath -Path env:FakeEnvValue
Assert-Equal -actual $actual -expected $false

# Get-DistronodeItem doesn't exist with -ErrorAction SilentlyContinue param
$actual = Get-DistronodeItem -Path C:\fakefile -ErrorAction SilentlyContinue
Assert-Equal -actual $actual -expected $null

# Get-DistronodeItem directory
$actual = Get-DistronodeItem -Path C:\Windows
Assert-Equal -actual $actual.FullName -expected C:\Windows
Assert-Equal -actual $actual.Attributes.HasFlag([System.IO.FileAttributes]::Directory) -expected $true
Assert-Equal -actual $actual.Exists -expected $true

# ensure Get-DistronodeItem doesn't fail in a try/catch and -ErrorAction SilentlyContinue - stop's a trap from trapping it
try {
    $actual = Get-DistronodeItem -Path C:\fakepath -ErrorAction SilentlyContinue
}
catch {
    Fail-Json -obj $result -message "this should not fire"
}
Assert-Equal -actual $actual -expected $null

$result.data = "success"
Exit-Json -obj $result
