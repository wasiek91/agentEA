---
allowed-tools: Read, Grep, Bash(python:*)
description: Przeanalizuj strategię handlu - szybka analiza
argument-hint: [strategy-file.py]
---

# Analyze Trading Strategy

Przeanalizuj plik strategii handlu: `$1`

## Checklist analizy:

### 1. **Wydajność**
- Czy historia pokazuje consistent returns?
- Czy jest trend wzrostu czy spadku?
- Jaki jest total return?

### 2. **Risk Metrics**
- **Maximum Drawdown**: Czy < 20%?
- **Sharpe Ratio**: Czy > 1.0?
- **Win Rate**: Jaki procent trades jest winning?
- **Profit Factor**: Czy > 1.5?

### 3. **Trade Characteristics**
- Jaka jest średnia duracja trade'a?
- Jak często strategy otwiera pozycje?
- Czy trade frequency jest realistyczna?
- Czy jest overtrading risk?

### 4. **Risk Management**
- Czy są stop-loss ordery?
- Czy są position size limity?
- Czy jest portfolio-level risk control?
- Czy drawdown constraints są respektowane?

### 5. **Potencjalne problemy**
- Curve fitting risk?
- Survival bias?
- Slippage impact?
- Commission impact?

## Output format:

```
## Wyniki analizy: [strategy-name]

**Performance**: [score 1-10]
- [key metric 1]: [value]
- [key metric 2]: [value]

**Risk**: [score 1-10]
- [concern 1]
- [concern 2]

**Rekomendacje**:
1. [action 1]
2. [action 2]

**Kiedy użyć RL Expert'a?**
- Jeśli score < 7 na obu metryach
- Run: .\run-rl-expert.ps1 -Query "Optymalizuj $1"
```

## Notatka:

Jeśli strategia potrzebuje głębokich ulepszeń, zaproponuj sesję z `/rl-expert`.
