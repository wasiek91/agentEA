# Dual Agent Workflow Launcher
# Uruchamia Claude Code i Coding Agent w osobnych oknach

param(
    [switch]$Help
)

if ($Help) {
    Write-Host @"
=== Dual Agent Workflow Launcher ===

Użycie:
  .\start-dual-workflow.ps1           Uruchom oba agenty
  .\start-dual-workflow.ps1 -Help     Pokaż tę pomoc

Co robi:
  - Otwiera Terminal 1: Claude Code (interaktywny chat)
  - Otwiera Terminal 2: Coding Agent (autonomiczny)

Workflow:
  1. Użyj Claude Code do planowania i designu
  2. Użyj Coding Agent do implementacji
  3. Wróć do Claude Code do review

Dokumentacja: DUAL_AGENT_WORKFLOW.md
"@
    exit 0
}

Clear-Host
Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                                        ║" -ForegroundColor Cyan
Write-Host "║        🤝 DUAL AGENT WORKFLOW LAUNCHER 🤝             ║" -ForegroundColor Cyan
Write-Host "║                                                        ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

$claudePath = "C:\Users\HP\OneDrive\Pulpit\Cloude"
$agentPath = "C:\Users\HP\OneDrive\Pulpit\Cloude\coding-agent"

# Check paths
Write-Host "[Sprawdzanie ścieżek...]" -ForegroundColor Yellow
if (-not (Test-Path $claudePath)) {
    Write-Host "  BŁĄD: Nie znaleziono folderu Claude: $claudePath" -ForegroundColor Red
    exit 1
}
if (-not (Test-Path $agentPath)) {
    Write-Host "  BŁĄD: Nie znaleziono folderu Coding Agent: $agentPath" -ForegroundColor Red
    exit 1
}
Write-Host "  ✓ Wszystkie ścieżki OK" -ForegroundColor Green
Write-Host ""

# Launcher info
Write-Host "Uruchamiam dwa terminale..." -ForegroundColor Cyan
Write-Host ""
Write-Host "📘 Terminal 1: Claude Code (Interaktywny)" -ForegroundColor Blue
Write-Host "   - Rozmowy i planowanie" -ForegroundColor Gray
Write-Host "   - Design decisions" -ForegroundColor Gray
Write-Host "   - Code review" -ForegroundColor Gray
Write-Host "   - Learning" -ForegroundColor Gray
Write-Host ""
Write-Host "📙 Terminal 2: Coding Agent (Autonomiczny)" -ForegroundColor Yellow
Write-Host "   - Automatyczne zadania" -ForegroundColor Gray
Write-Host "   - Batch processing" -ForegroundColor Gray
Write-Host "   - Implementacja" -ForegroundColor Gray
Write-Host "   - Testy" -ForegroundColor Gray
Write-Host ""

# Launch Terminal 1 - Claude Code
Write-Host "[1/2] Uruchamiam Claude Code..." -ForegroundColor Cyan
$claudeScript = @"
`$Host.UI.RawUI.WindowTitle = 'Claude Code - Interaktywny'
Clear-Host
Write-Host '╔════════════════════════════════════════════════════════╗' -ForegroundColor Blue
Write-Host '║                                                        ║' -ForegroundColor Blue
Write-Host '║           📘 CLAUDE CODE - INTERAKTYWNY               ║' -ForegroundColor Blue
Write-Host '║                                                        ║' -ForegroundColor Blue
Write-Host '╚════════════════════════════════════════════════════════╝' -ForegroundColor Blue
Write-Host ''
Write-Host '💡 Używaj mnie do:' -ForegroundColor Cyan
Write-Host '   • Planowania architektury' -ForegroundColor White
Write-Host '   • Design decisions' -ForegroundColor White
Write-Host '   • Code review' -ForegroundColor White
Write-Host '   • Wyjaśnień i nauki' -ForegroundColor White
Write-Host ''
Write-Host '🚀 Aby rozpocząć, wpisz:' -ForegroundColor Yellow
Write-Host '   npx claude' -ForegroundColor White
Write-Host ''
cd '$claudePath'
"@

Start-Process powershell -ArgumentList "-NoExit", "-Command", $claudeScript

Start-Sleep -Seconds 1

# Launch Terminal 2 - Coding Agent
Write-Host "[2/2] Uruchamiam Coding Agent..." -ForegroundColor Cyan
$agentScript = @"
`$Host.UI.RawUI.WindowTitle = 'Coding Agent - Autonomiczny'
Clear-Host
Write-Host '╔════════════════════════════════════════════════════════╗' -ForegroundColor Yellow
Write-Host '║                                                        ║' -ForegroundColor Yellow
Write-Host '║          📙 CODING AGENT - AUTONOMICZNY                ║' -ForegroundColor Yellow
Write-Host '║                                                        ║' -ForegroundColor Yellow
Write-Host '╚════════════════════════════════════════════════════════╝' -ForegroundColor Yellow
Write-Host ''
Write-Host '🤖 Używaj mnie do:' -ForegroundColor Cyan
Write-Host '   • Automatycznych zadań' -ForegroundColor White
Write-Host '   • Batch processing' -ForegroundColor White
Write-Host '   • Implementacji wzorców' -ForegroundColor White
Write-Host '   • Generowania testów' -ForegroundColor White
Write-Host ''
Write-Host '🚀 Przykładowe komendy:' -ForegroundColor Yellow
Write-Host '   python agent.py --interactive' -ForegroundColor White
Write-Host '   python agent.py --task "Twoje zadanie"' -ForegroundColor White
Write-Host '   python agent.py --help' -ForegroundColor White
Write-Host ''
cd '$agentPath'
"@

Start-Process powershell -ArgumentList "-NoExit", "-Command", $agentScript

Write-Host ""
Write-Host "✓ Oba terminale uruchomione!" -ForegroundColor Green
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "                   QUICK START GUIDE                    " -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "1️⃣  W BLUE terminal (Claude Code):" -ForegroundColor Blue
Write-Host "    npx claude" -ForegroundColor White
Write-Host "    Następnie rozmawiaj: 'Zaprojektujmy aplikację...'" -ForegroundColor Gray
Write-Host ""
Write-Host "2️⃣  W YELLOW terminal (Coding Agent):" -ForegroundColor Yellow
Write-Host "    python agent.py --task 'Zaimplementuj według planu'" -ForegroundColor White
Write-Host ""
Write-Host "3️⃣  Wróć do BLUE terminal dla review!" -ForegroundColor Blue
Write-Host ""
Write-Host "📚 Pełna dokumentacja: DUAL_AGENT_WORKFLOW.md" -ForegroundColor Cyan
Write-Host ""
Write-Host "Naciśnij Enter aby zamknąć launcher..." -ForegroundColor Gray
Read-Host
