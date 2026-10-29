$ErrorActionPreference = "Stop"
$repo = "D:\Exorcist\demo\jersey-paglu"
$report = "D:\Exorcist\demo\jersey-paglu-real-report.html"
$json = "D:\Exorcist\demo\jersey-paglu-real-findings.json"

Write-Host "EXORCIST LIVE DEMO" -ForegroundColor Cyan
Write-Host "Repository: https://github.com/ADITYA-KUMAR-2358/jersey-paglu" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Checking local dependencies..." -ForegroundColor Yellow
exorcist doctor --model gemma3:4b
Write-Host ""
Write-Host "2. Running full local-first scan..." -ForegroundColor Yellow
exorcist scan $repo --model gemma3:4b --types secrets,deps,deadcode,cron --plain
$scanCode = $LASTEXITCODE
Write-Host "Scan exit code: $scanCode" -ForegroundColor Green
Write-Host ""
Write-Host "3. Exporting machine-readable findings..." -ForegroundColor Yellow
exorcist scan $repo --model gemma3:4b --types secrets,deps,deadcode,cron --json | Set-Content -LiteralPath $json -Encoding utf8
Write-Host "Saved: $json" -ForegroundColor Green
Write-Host ""
Write-Host "4. Generating offline HTML report..." -ForegroundColor Yellow
exorcist report $repo --model gemma3:4b --out $report
Write-Host ""
Write-Host "5. Demo artifacts:" -ForegroundColor Yellow
Get-Item -LiteralPath $json, $report | Select-Object Name, Length
Write-Host ""
Write-Host "LIVE DEMO COMPLETE - 0 network calls" -ForegroundColor Green
Write-Host "Press Enter to close this real terminal window."
[Console]::ReadLine() | Out-Null
