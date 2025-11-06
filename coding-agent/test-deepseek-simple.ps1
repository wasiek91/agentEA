# Simple DeepSeek CLI Test Script
Write-Host "=== DeepSeek CLI Installation Test ===" -ForegroundColor Cyan
Write-Host ""

$deepseekExe = "C:\Users\HP\OneDrive\Pulpit\Cloude\coding-agent\deepseek-env\Scripts\deepseek.exe"

# Test 1: Check if executable exists
Write-Host "[Test 1] Checking executable..." -ForegroundColor Yellow
if (Test-Path $deepseekExe) {
    Write-Host "  [OK] Found: $deepseekExe" -ForegroundColor Green
} else {
    Write-Host "  [ERROR] Not found: $deepseekExe" -ForegroundColor Red
    exit 1
}

# Test 2: Check version
Write-Host ""
Write-Host "[Test 2] Checking version..." -ForegroundColor Yellow
try {
    $version = & $deepseekExe --version 2>&1
    Write-Host "  [OK] Version: $version" -ForegroundColor Green
} catch {
    Write-Host "  [WARNING] Could not get version" -ForegroundColor Yellow
}

# Test 3: Check API key
Write-Host ""
Write-Host "[Test 3] Checking API key..." -ForegroundColor Yellow
if ($env:DEEPSEEK_API_KEY) {
    Write-Host "  [OK] API key is set" -ForegroundColor Green
} else {
    Write-Host "  [WARNING] API key not set" -ForegroundColor Yellow
    Write-Host "           Set with: `$env:DEEPSEEK_API_KEY='your_key'" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Installation test complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Run: .\setup-deepseek-profile.ps1" -ForegroundColor White
Write-Host "2. Add your API key to PowerShell profile" -ForegroundColor White
Write-Host "3. Reload profile: . `$PROFILE" -ForegroundColor White
Write-Host ""
