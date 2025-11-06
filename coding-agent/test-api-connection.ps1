# Test DeepSeek API Connection
Write-Host "=== Test Polaczenia z DeepSeek API ===" -ForegroundColor Cyan
Write-Host ""

# Load profile to get API key
. $PROFILE

Write-Host "[Test 1] Sprawdzanie klucza API..." -ForegroundColor Yellow
if ($env:DEEPSEEK_API_KEY -and $env:DEEPSEEK_API_KEY -ne "YOUR_API_KEY_HERE") {
    $keyLength = $env:DEEPSEEK_API_KEY.Length
    Write-Host "  [OK] Klucz API jest ustawiony (dlugosc: $keyLength znakow)" -ForegroundColor Green
} else {
    Write-Host "  [BLAD] Klucz API nie jest ustawiony" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[Test 2] Testowanie polaczenia z API..." -ForegroundColor Yellow
Write-Host "  Wysylanie zapytania do DeepSeek..." -ForegroundColor Gray

$deepseekExe = "C:\Users\HP\OneDrive\Pulpit\Cloude\coding-agent\deepseek-env\Scripts\deepseek.exe"

try {
    $result = & $deepseekExe generate "Odpowiedz jednym slowem: OK" 2>&1

    if ($LASTEXITCODE -eq 0) {
        Write-Host "  [OK] Polaczenie dziala!" -ForegroundColor Green
        Write-Host "  Odpowiedz: $result" -ForegroundColor Gray
    } else {
        Write-Host "  [BLAD] Polaczenie nie powiodlo sie" -ForegroundColor Red
        Write-Host "  $result" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  [BLAD] Wystapil blad: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "Test zakonczony!" -ForegroundColor Cyan
