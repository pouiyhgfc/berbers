# Serve deze site op http://127.0.0.1:<poort>/ (standaard 8080).
# Gebruik: .\serve.ps1   of   .\serve.ps1 8765
$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
$port = 8080
if ($args.Count -ge 1) { $port = [int]$args[0] }
Set-Location $root
python -m http.server $port --bind 127.0.0.1 --directory $root
