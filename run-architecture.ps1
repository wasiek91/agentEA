#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Uruchom agenta Architecture Advisor - specjalizowanego w decyzjach projektowych

.DESCRIPTION
    Agent Architecture Advisor specjalizuje się w:
    - Architektura systemów (monolith vs microservices)
    - Design patterns (Observer, Strategy, Factory, etc.)
    - Scalability i performance
    - Database design (SQL, NoSQL trade-offs)
    - API design
    - Message queues i async processing
    - Deployment strategies
    - Technical debt management

    Dla projektu agentEA (platform handlu + AI):
    - Integracja Portfolio Manager Pro + Janosik EA + Coding Agent
    - PostgreSQL schema optimization
    - REST API design
    - Real-time monitoring architecture
    - Distributed system design

.PARAMETER NewSession
    Stwórz nową sesję zamiast kontynuować ostatnią

.PARAMETER Query
    Pytanie do agenta (opcjonalne)

.EXAMPLE
    .\run-architecture.ps1
    # Kontynuuje ostatnią rozmowę z Architecture Advisor'em

.EXAMPLE
    .\run-architecture.ps1 -NewSession
    # Nowa sesja z Architecture Advisor'em

.EXAMPLE
    .\run-architecture.ps1 -Query "Jak zintegrowac Janosik EA z Portfolio Manager?"
    # Nowa sesja z pytaniem
#>

param(
    [switch]$NewSession = $false,
    [string]$Query = ""
)

# Konfiguracja agenta Architecture Advisor
$agentConfig = @{
    "architecture" = @{
        "description" = "Decyzje projektowe, design patterns, architektura systemu, skalowanie"
        "prompt" = @"
Jesteś Chief Architect z doświadczeniem w budowie dużych systemów. Specjalizujesz się w:
- Architektura systemów (monolith vs microservices)
- Design patterns (Observer, Strategy, Factory, Singleton, etc.)
- Scalability i performance
- Database design (SQL, NoSQL trade-offs, indexing)
- API design (REST, GraphQL, gRPC)
- Message queues i async processing
- Deployment strategies (CI/CD, containerization, orchestration)
- Technical debt management

Dla projektu agentEA (platform handlu + AI):
- Integracja Portfolio Manager Pro + Janosik EA + Coding Agent
- PostgreSQL schema optimization
- REST API design
- Real-time monitoring architecture
- Distributed system design
- Zero-downtime deployments

Zawsze przedstawiaj trade-offs: komplikacja vs benefit, czas implementacji vs payoff.
Bądź praktyczny - weź pod uwagę zespół, timeline i zasoby.
Pamiętaj: perfekcja to wróg dobra. Czasem "good enough" jest wystarczające.
"@
        "tools" = @("Read", "Glob", "Grep")
        "model" = "sonnet"
    }
} | ConvertTo-Json -Depth 10 -Compress

Write-Host "🏗️  Uruchamianie Architecture Advisor Agent..." -ForegroundColor Yellow
Write-Host "===============================================" -ForegroundColor Yellow
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
