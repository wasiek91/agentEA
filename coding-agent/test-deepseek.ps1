# Test instalacji DeepSeek CLI
# Ten skrypt sprawdzi czy DeepSeek CLI jest poprawnie zainstalowane

Write-Host "=== Test Instalacji DeepSeek CLI ===" -ForegroundColor Cyan
Write-Host ""

# Ścieżka do DeepSeek
$deepseekExe = "C:\Users\HP\OneDrive\Pulpit\Cloude\coding-agent\deepseek-env\Scripts\deepseek.exe"
$deepseekPip = "C:\Users\HP\OneDrive\Pulpit\Cloude\coding-agent\deepseek-env\Scripts\pip.exe"

# Test 1: Sprawdź czy plik executable istnieje
Write-Host "[Test 1] Sprawdzanie istnienia pliku executable..." -ForegroundColor Yellow
if (Test-Path $deepseekExe) {
    Write-Host "  [OK] Znaleziono: $deepseekExe" -ForegroundColor Green
} else {
    Write-Host "  [BŁĄD] Nie znaleziono: $deepseekExe" -ForegroundColor Red
    exit 1
}

# Test 2: Sprawdź wersję
Write-Host ""
Write-Host "[Test 2] Sprawdzanie wersji DeepSeek CLI..." -ForegroundColor Yellow
try {
    $version = & $deepseekExe --version 2>&1
    Write-Host "  [OK] Wersja: $version" -ForegroundColor Green
} catch {
    Write-Host "  [OSTRZEŻENIE] Nie udało się pobrać wersji: $_" -ForegroundColor Yellow
}

# Test 3: Sprawdź zainstalowane pakiety
Write-Host ""
Write-Host "[Test 3] Sprawdzanie zainstalowanych pakietów..." -ForegroundColor Yellow
try {
    $packages = & $deepseekPip list | Select-String -Pattern "deepseek"
    if ($packages) {
        Write-Host "  [OK] Zainstalowane pakiety DeepSeek:" -ForegroundColor Green
        $packages | ForEach-Object { Write-Host "       $_" -ForegroundColor Gray }
    } else {
        Write-Host "  [OSTRZEŻENIE] Nie znaleziono pakietów deepseek" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  [BŁĄD] Nie udało się sprawdzić pakietów: $_" -ForegroundColor Red
}

# Test 4: Sprawdź zmienną środowiskową API KEY
Write-Host ""
Write-Host "[Test 4] Sprawdzanie klucza API..." -ForegroundColor Yellow
if ($env:DEEPSEEK_API_KEY) {
    $keyLength = $env:DEEPSEEK_API_KEY.Length
    $keyPreview = $env:DEEPSEEK_API_KEY.Substring(0, [Math]::Min(10, $keyLength)) + "..."
    Write-Host "  [OK] Klucz API jest ustawiony: $keyPreview" -ForegroundColor Green
    Write-Host "       (Długość: $keyLength znaków)" -ForegroundColor Gray
} else {
    Write-Host "  [OSTRZEŻENIE] Klucz API nie jest ustawiony" -ForegroundColor Yellow
    Write-Host "                Ustaw: `$env:DEEPSEEK_API_KEY='twój_klucz'" -ForegroundColor Gray
    Write-Host "                Lub uruchom: .\setup-deepseek-profile.ps1" -ForegroundColor Gray
}

# Test 5: Sprawdź alias (jeśli istnieje)
Write-Host ""
Write-Host "[Test 5] Sprawdzanie aliasu 'deepseek'..." -ForegroundColor Yellow
$aliasExists = Get-Alias -Name deepseek -ErrorAction SilentlyContinue
if ($aliasExists) {
    Write-Host "  [OK] Alias 'deepseek' jest skonfigurowany" -ForegroundColor Green
    Write-Host "       Wskazuje na: $($aliasExists.Definition)" -ForegroundColor Gray
} else {
    Write-Host "  [INFO] Alias 'deepseek' nie jest jeszcze skonfigurowany" -ForegroundColor Cyan
    Write-Host "         Uruchom: .\setup-deepseek-profile.ps1" -ForegroundColor Gray
}

# Test 6: Test polaczenia (jesli klucz API jest ustawiony)
Write-Host ""
Write-Host "[Test 6] Test połączenia z API..." -ForegroundColor Yellow
if ($env:DEEPSEEK_API_KEY -and $env:DEEPSEEK_API_KEY -ne "YOUR_API_KEY_HERE") {
    Write-Host "  Wysyłanie testowego zapytania..." -ForegroundColor Gray
    try {
        $testQuery = "Odpowiedz jednym słowem: OK"
        $result = & $deepseekExe -q $testQuery 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  [OK] Połączenie z API działa!" -ForegroundColor Green
            Write-Host "       Odpowiedź: $result" -ForegroundColor Gray
        } else {
            Write-Host "  [BŁĄD] Połączenie nie powiodło się" -ForegroundColor Red
            Write-Host "         $result" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "  [BŁĄD] Nie udało się połączyć: $_" -ForegroundColor Red
    }
} else {
    Write-Host "  [POMINIĘTO] Brak poprawnego klucza API" -ForegroundColor Yellow
}

# Podsumowanie
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "PODSUMOWANIE TESTÓW" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

if (Test-Path $deepseekExe) {
    Write-Host "[✓] DeepSeek CLI jest zainstalowany" -ForegroundColor Green
} else {
    Write-Host "[✗] DeepSeek CLI NIE jest zainstalowany" -ForegroundColor Red
}

if ($env:DEEPSEEK_API_KEY -and $env:DEEPSEEK_API_KEY -ne "YOUR_API_KEY_HERE") {
    Write-Host "[✓] Klucz API jest skonfigurowany" -ForegroundColor Green
} else {
    Write-Host "[!] Klucz API wymaga konfiguracji" -ForegroundColor Yellow
}

if ($aliasExists) {
    Write-Host "[✓] Alias PowerShell jest skonfigurowany" -ForegroundColor Green
} else {
    Write-Host "[!] Alias PowerShell nie jest skonfigurowany" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Aby skonfigurować brakujące elementy:" -ForegroundColor Cyan
Write-Host "  1. Uruchom: .\setup-deepseek-profile.ps1" -ForegroundColor White
Write-Host "  2. Edytuj profil i dodaj klucz API" -ForegroundColor White
Write-Host "  3. Przeładuj profil: . `$PROFILE" -ForegroundColor White
Write-Host ""
Write-Host "Dokumentacja: README_DEEPSEEK.md" -ForegroundColor Gray
Write-Host ""
