$ErrorActionPreference = 'Stop'
$bundledPython = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
if (Test-Path -LiteralPath $bundledPython) {
    & $bundledPython -u (Join-Path $PSScriptRoot 'server.py') --port 4180
} else {
    python (Join-Path $PSScriptRoot 'server.py') --port 4180
}
