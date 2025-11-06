# DeepSeek CLI - Automatyczna Konfiguracja Profilu PowerShell
# Ten skrypt automatycznie doda alias i zmienną środowiskową do Twojego profilu PowerShell

Write-Host "=== DeepSeek CLI - Konfiguracja Profilu PowerShell ===" -ForegroundColor Cyan
Write-Host ""

# Ścieżka do executable DeepSeek
$deepseekPath = "C:\Users\HP\OneDrive\Pulpit\Cloude\coding-agent\deepseek-env\Scripts\deepseek.exe"

# Sprawdź czy plik istnieje
if (-not (Test-Path $deepseekPath)) {
    Write-Host "BŁĄD: Nie znaleziono deepseek.exe w:" -ForegroundColor Red
    Write-Host $deepseekPath -ForegroundColor Yellow
    Write-Host "Sprawdź czy instalacja się powiodła." -ForegroundColor Red
    exit 1
}

Write-Host "[OK] Znaleziono DeepSeek CLI w:" -ForegroundColor Green
Write-Host "     $deepseekPath" -ForegroundColor Gray
Write-Host ""

# Sprawdź czy profil PowerShell istnieje
if (-not (Test-Path $PROFILE)) {
    Write-Host "Tworzenie nowego profilu PowerShell..." -ForegroundColor Yellow
    New-Item -Path $PROFILE -Type File -Force | Out-Null
}

Write-Host "Profil PowerShell:" -ForegroundColor Cyan
Write-Host "     $PROFILE" -ForegroundColor Gray
Write-Host ""

# Przygotuj zawartość do dodania
$configContent = @"

# ===== DeepSeek CLI Configuration =====
# Dodane automatycznie przez setup-deepseek-profile.ps1

# Alias dla DeepSeek CLI
Set-Alias deepseek "$deepseekPath"

# Zmienna środowiskowa dla klucza API DeepSeek
# UWAGA: Zamień 'YOUR_API_KEY_HERE' na swój prawdziwy klucz API
# Pobierz klucz z: https://platform.deepseek.com/api_keys
`$env:DEEPSEEK_API_KEY="YOUR_API_KEY_HERE"

Write-Host "[DeepSeek CLI] Załadowano alias 'deepseek'" -ForegroundColor Green
# ===== Koniec Konfiguracji DeepSeek =====

"@

# Sprawdź czy konfiguracja już istnieje w profilu
$profileContent = Get-Content $PROFILE -Raw -ErrorAction SilentlyContinue

if ($profileContent -like "*DeepSeek CLI Configuration*") {
    Write-Host "UWAGA: Konfiguracja DeepSeek już istnieje w profilu!" -ForegroundColor Yellow
    Write-Host "Czy chcesz ją zastąpić? (T/N)" -ForegroundColor Cyan
    $response = Read-Host

    if ($response -ne "T" -and $response -ne "t") {
        Write-Host "Anulowano. Profil nie został zmieniony." -ForegroundColor Yellow
        exit 0
    }

    # Usuń starą konfigurację
    $profileContent = $profileContent -replace '(?s)# ===== DeepSeek CLI Configuration =====.*?# ===== Koniec Konfiguracji DeepSeek =====\r?\n?', ''
    Set-Content -Path $PROFILE -Value $profileContent -NoNewline
    Write-Host "Usunięto starą konfigurację." -ForegroundColor Green
}

# Dodaj nową konfigurację
Add-Content -Path $PROFILE -Value $configContent

Write-Host ""
Write-Host "[SUKCES] Konfiguracja została dodana do profilu!" -ForegroundColor Green
Write-Host ""
Write-Host "Następne kroki:" -ForegroundColor Cyan
Write-Host "  1. Otwórz profil: notepad `$PROFILE" -ForegroundColor White
Write-Host "  2. Znajdź linię: `$env:DEEPSEEK_API_KEY=`"YOUR_API_KEY_HERE`"" -ForegroundColor White
Write-Host "  3. Zamień YOUR_API_KEY_HERE na swój prawdziwy klucz API" -ForegroundColor White
Write-Host "  4. Zapisz i zamknij" -ForegroundColor White
Write-Host "  5. Przeładuj profil: . `$PROFILE" -ForegroundColor White
Write-Host "  6. Testuj: deepseek -q `"Test połączenia`"" -ForegroundColor White
Write-Host ""
Write-Host "Pobierz klucz API z:" -ForegroundColor Yellow
Write-Host "  https://platform.deepseek.com/api_keys" -ForegroundColor Cyan
Write-Host ""

# Zapytaj czy otworzyć profil teraz
Write-Host "Czy chcesz otworzyć profil w Notepad teraz? (T/N)" -ForegroundColor Cyan
$openNow = Read-Host

if ($openNow -eq "T" -or $openNow -eq "t") {
    notepad $PROFILE
    Write-Host "Otwarto profil w Notepad." -ForegroundColor Green
    Write-Host "Po edycji zapisz i uruchom: . `$PROFILE" -ForegroundColor Yellow
} else {
    Write-Host "Możesz otworzyć profil później komendą: notepad `$PROFILE" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Konfiguracja zakończona!" -ForegroundColor Green
