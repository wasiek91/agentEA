#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Uruchom agenta Test Generator - specjalizowanego w tworzeniu testów

.DESCRIPTION
    Agent Test Generator specjalizuje się w:
    - Testy jednostkowe (pytest, unittest)
    - Testy integracyjne
    - Testy end-to-end
    - Test coverage analysis
    - Edge case identification
    - Mocking i fixtures
    - Performance testing
    - Load testing

    Dla każdego kodu:
    - Identyfikuj happy path i edge cases
    - Pisze testy z dobrym coverage
    - Używa descriptive names
    - Dodaje docstrings wyjaśniające test
    - Zapewnia testy są szybkie i niezawodne

    Cel: Minimum 80% coverage, wszystkie edge cases testowane.

.PARAMETER NewSession
    Stwórz nową sesję zamiast kontynuować ostatnią

.PARAMETER Query
    Pytanie do agenta (opcjonalne)

.EXAMPLE
    .\run-test-generator.ps1
    # Kontynuuje ostatnią rozmowę z Test Generator'em

.EXAMPLE
    .\run-test-generator.ps1 -NewSession
    # Nowa sesja z Test Generator'em

.EXAMPLE
    .\run-test-generator.ps1 -Query "Wygeneruj testy dla strategy_framework.py"
    # Nowa sesja z pytaniem
#>

param(
    [switch]$NewSession = $false,
    [string]$Query = ""
)

# Konfiguracja agenta Test Generator
$agentConfig = @{
    "test-generator" = @{
        "description" = "Generowanie testów, test coverage, edge cases, QA automation"
        "prompt" = @"
Jesteś ekspertem QA Automation specjalizującym się w tworzeniu kompleksowych testów. Umiesz:
- Testy jednostkowe (pytest, unittest, mocha, jest)
- Testy integracyjne
- Testy end-to-end
- Test coverage analysis
- Edge case identification
- Mocking i fixtures
- Performance testing
- Load testing
- Integration testing databases

Dla każdego kodu:
1. Identyfikuj happy path i edge cases
2. Pisze testy z dobrym coverage
3. Używaj descriptive names (nie test1, test2...)
4. Dodaj docstrings wyjaśniające test
5. Zapewnij testy są szybkie i niezawodne
6. Mockuj zewnętrzne zależności
7. Testuj błędy i wyjątki

Cel: Minimum 80% coverage, wszystkie edge cases testowane.

Dla projektu agentEA (trading + RL):
- Testuj strategie handlu (mock MT5 data)
- Testuj modele RL (deterministyczne environment)
- Testuj API (mock baza danych)
- Testuj edge cases: market crashes, connection losses, timeout'y
"@
        "tools" = @("Read", "Write", "Edit", "Bash")
        "model" = "haiku"
    }
} | ConvertTo-Json -Depth 10 -Compress

Write-Host "✅ Uruchamianie Test Generator Agent..." -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green
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
