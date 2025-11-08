#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Uruchom agenta RL Expert - specjalizowanego w Reinforcement Learning

.DESCRIPTION
    Agent RL Expert specjalizuje się w:
    - Algorytmy: PPO, DQN, A3C, DDPG, SAC
    - Hiperparametry i tuning
    - Reward shaping i design
    - Exploration vs Exploitation trade-offs
    - Stability i convergence
    - Metryki i ocena modeli
    - Environment design

    Dla projektu agentEA (handler handlu):
    - Optymalizacja strategii handlu
    - Risk management i drawdown control
    - Portfolio optimization
    - Backtesting i out-of-sample testing

.PARAMETER NewSession
    Stwórz nową sesję zamiast kontynuować ostatnią

.PARAMETER Query
    Pytanie do agenta (opcjonalne)

.EXAMPLE
    .\run-rl-expert.ps1
    # Kontynuuje ostatnią rozmowę z RL Expert'em

.EXAMPLE
    .\run-rl-expert.ps1 -NewSession
    # Nowa sesja z RL Expert'em

.EXAMPLE
    .\run-rl-expert.ps1 -Query "Jak tuningować hyperparameters dla PPO?"
    # Nowa sesja z pytaniem
#>

param(
    [switch]$NewSession = $false,
    [string]$Query = ""
)

# Konfiguracja agenta RL Expert
$agentConfig = @{
    "rl-expert" = @{
        "description" = "Konsultacje Reinforcement Learning, optymalizacja modeli, hiperparametry"
        "prompt" = @"
Jesteś ekspertem Reinforcement Learning z doświadczeniem w praktycznych implementacjach. Specjalizujesz się w:
- Algorytmy: PPO, DQN, A3C, DDPG, SAC
- Hiperparametry i tuning
- Reward shaping i design
- Exploration vs Exploitation trade-offs
- Stability i convergence
- Metryki i ocena modeli
- Environment design

Dla projektu agentEA (handler handlu):
- Optymalizacja strategii handlu
- Risk management i drawdown control
- Portfolio optimization
- Backtesting i out-of-sample testing

Podawaj konkretne rekomendacje z teorią i empirią.
Pamiętaj: trading jest w prawdziwym czasie - stabilność i risk control są ważniejsze niż maksymalny profit.
"@
        "tools" = @("Read", "Grep", "Bash")
        "model" = "sonnet"
    }
} | ConvertTo-Json -Depth 10 -Compress

Write-Host "🧠 Uruchamianie RL Expert Agent..." -ForegroundColor Magenta
Write-Host "===============================================" -ForegroundColor Magenta
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
