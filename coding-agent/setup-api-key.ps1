# DeepSeek CLI - Quick API Key Setup
Write-Host "=== DeepSeek CLI - Konfiguracja Klucza API ===" -ForegroundColor Cyan
Write-Host ""

$deepseekPath = "C:\Users\HP\OneDrive\Pulpit\Cloude\coding-agent\deepseek-env\Scripts\deepseek.exe"

# Check if deepseek exists
if (-not (Test-Path $deepseekPath)) {
    Write-Host "BLAD: Nie znaleziono deepseek.exe" -ForegroundColor Red
    exit 1
}

Write-Host "[OK] DeepSeek CLI znaleziony" -ForegroundColor Green
Write-Host ""

# Check if profile exists
if (-not (Test-Path $PROFILE)) {
    Write-Host "Tworzenie profilu PowerShell..." -ForegroundColor Yellow
    New-Item -Path $PROFILE -Type File -Force | Out-Null
}

Write-Host "Profil PowerShell: $PROFILE" -ForegroundColor Cyan
Write-Host ""

# Add configuration
$config = "`n# DeepSeek CLI Configuration`n"
$config += "`$env:DEEPSEEK_API_KEY=`"YOUR_API_KEY_HERE`"`n"
$config += "Set-Alias deepseek `"$deepseekPath`"`n"
$config += "Write-Host '[DeepSeek] Alias zaladowany' -ForegroundColor Green`n"

Add-Content -Path $PROFILE -Value $config

Write-Host "[SUKCES] Konfiguracja dodana do profilu!" -ForegroundColor Green
Write-Host ""
Write-Host "TERAZ:" -ForegroundColor Yellow
Write-Host "1. Otwieram profil w Notepad..." -ForegroundColor White
Write-Host "2. Znajdz linie: YOUR_API_KEY_HERE" -ForegroundColor White
Write-Host "3. Zamien na swoj prawdziwy klucz API" -ForegroundColor White
Write-Host "4. Zapisz i zamknij Notepad" -ForegroundColor White
Write-Host ""

# Open notepad
notepad $PROFILE

Write-Host ""
Write-Host "Po zapisaniu uruchom:" -ForegroundColor Cyan
Write-Host ". `$PROFILE" -ForegroundColor White
Write-Host ""
Write-Host "Nastepnie przetestuj:" -ForegroundColor Cyan
Write-Host "deepseek chat" -ForegroundColor White
Write-Host ""
