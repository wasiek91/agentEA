#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Uruchom agenta Code Reviewer - specjalizowanego w przeglądzie kodu

.DESCRIPTION
    Agent Code Reviewer specjalizuje się w:
    - Analiza jakości kodu (czystość, czytelność, maintainability)
    - Bezpieczeństwo (OWASP, injection, XSS, SQL injection)
    - Wydajność i optymalizacja
    - Design patterns i best practices
    - Testy jednostkowe i integracyjne

.PARAMETER NewSession
    Stwórz nową sesję zamiast kontynuować ostatnią

.PARAMETER Query
    Pytanie do agenta (opcjonalne)

.EXAMPLE
    .\run-code-reviewer.ps1
    # Kontynuuje ostatnią rozmowę z Code Reviewer'em

.EXAMPLE
    .\run-code-reviewer.ps1 -NewSession
    # Nowa sesja z Code Reviewer'em

.EXAMPLE
    .\run-code-reviewer.ps1 -Query "Przejrzyj mój kod w src/"
    # Nowa sesja z pytaniem
#>

param(
    [switch]$NewSession = $false,
    [string]$Query = ""
)

# Konfiguracja agenta Code Reviewer
$agentConfig = @{
    "code-reviewer" = @{
        "description" = "Przegląd kodu, testowanie, best practices, QA"
        "prompt" = @"
Jesteś doświadczonym recenzentem kodu (Senior Code Reviewer). Specjalizujesz się w:
- Analiza jakości kodu (czystość, czytelność, maintainability)
- Bezpieczeństwo (OWASP, injection, XSS, SQL injection)
- Wydajność i optymalizacja
- Design patterns i best practices
- Testy jednostkowe i integracyjne

Zawsze sprawdzaj:
1. Czy kod jest bezpieczny?
2. Czy są potencjalne performance bottlenecks?
3. Czy są brakujące error handling?
4. Czy kod jest testowany?
5. Czy implementacja pasuje do istniejącej architektury?

Bądź konstruktywny i podawaj konkretne sugestie ulepszeń.
"@
        "tools" = @("Read", "Grep", "Glob", "Bash")
        "model" = "sonnet"
    }
} | ConvertTo-Json -Depth 10 -Compress

Write-Host "🔍 Uruchamianie Code Reviewer Agent..." -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

# Buduj komendę Claude
$claudeCmd = "claude --agents '$agentConfig'"

if ($Query) {
    $claudeCmd += " -p ""$Query"""
} elseif (!$NewSession) {
    $claudeCmd += " --continue"
}

# Wykonaj komendę
Invoke-Expression $claudeCmd
