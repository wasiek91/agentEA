---
allowed-tools: Read, Bash(python:*)
description: Uruchom backtest strategii na danych historycznych
argument-hint: [strategy-name] [period] [start-date]
---

# Backtest Strategy

Uruchom backtest dla strategii: `$1`

## Parametry:

- **Strategy**: `$1` (wymagane)
- **Period**: `$2` (opcjonalne: 3m, 6m, 1y, 2y - default: 1y)
- **Start Date**: `$3` (opcjonalne: YYYY-MM-DD - default: 1 rok temu)

## Procedura backtestingu:

### 1. **Walidacja danych**
- Sprawdź czy plik strategii istnieje
- Sprawdź czy są dostępne dane historyczne
- Załaduj konfigurację strategii

### 2. **Uruchom backtest**
```bash
python portfolio-manager-pro/backtester.py \
  --strategy $1 \
  --period $2 \
  --start-date $3
```

### 3. **Analiza wyników**
- **Total Return**: Jaki % gain/loss?
- **Sharpe Ratio**: Czy > 1.0?
- **Max Drawdown**: Czy < 20%?
- **Winning Trades**: Jaki % trades było winning?
- **Monthly Performance**: Czy consistent?
- **Volatility**: Czy akceptowalna?

### 4. **Out-of-Sample Test** (jeśli masz dane)
- Oddziel 20% danych na test
- Trenuj na pozostałych 80%
- Waliduj na 20% test set
- Sprawdzaj czy performance się powtarza

## Red Flags:

⚠️ **Problem**: Max Drawdown > 30%
→ Akcja: Zwiększ stop-loss lub zmniejsz position size

⚠️ **Problem**: Sharpe Ratio < 0.5
→ Akcja: Rewizja risk-adjusted returns

⚠️ **Problem**: Win Rate < 40%
→ Akcja: Sprawdź czy jest realistic, czy nie overfit

⚠️ **Problem**: Monthly returns są volatile
→ Akcja: Rozważ zmianę strategy parameters

## Kiedy użyć agentów:

- Wyniki są słabe → **`/rl-expert`** (optymalizacja)
- Chcesz zrozumieć kod → **`.\run-code-reviewer.ps1`** (przegląd)
- Chcesz nowe testy → **`/generate-tests`** (test coverage)

## Format outputu:

```
## Backtest Results: $1

**Period**: $2 | **Start Date**: $3

**Performance**:
- Total Return: [X%]
- Monthly Avg: [X%]
- Volatility: [X%]

**Risk**:
- Max Drawdown: [X%]
- Sharpe Ratio: [X]
- Profit Factor: [X]

**Trade Stats**:
- Winning Trades: [X%]
- Avg Win/Loss Ratio: [X]
- Trade Frequency: [X per month]

**Verdict**: [PASS/NEEDS_WORK]
**Next Step**: [recommendation]
```
