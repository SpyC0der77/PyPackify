Output docs/images/cli-demo.gif
Require python
Set Shell "powershell"
Set Width 1000
Set Height 650
Set FontSize 20
Set TypingSpeed 35ms
Set Framerate 10
Hide
Type "$work = & ./docs/demo/prepare.ps1; Set-Location $work; function prompt { 'demo> ' }; Clear-Host"
Enter
Sleep 1s
Show
Type "Get-Content config.json"
Enter
Sleep 2s
Type "python pypackify.py --config config.json"
Enter
Sleep 3s
Type "Get-ChildItem hello_package -Recurse | Select-Object Name"
Enter
Sleep 3s
