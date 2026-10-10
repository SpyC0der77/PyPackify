$ErrorActionPreference = 'Stop'
$work = Join-Path ([IO.Path]::GetTempPath()) ('vhs-demo-' + [guid]::NewGuid().ToString())
New-Item -ItemType Directory -Path $work | Out-Null
Copy-Item -LiteralPath 'pypackify.py' -Destination $work -Recurse
Copy-Item -LiteralPath 'docs/demo/config.json' -Destination $work -Recurse
Copy-Item -LiteralPath 'docs/demo/greet.py' -Destination $work -Recurse
$work
