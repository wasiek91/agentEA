---
allowed-tools: Read, Bash(python:*), Bash(git:*)
description: Konsultacja RL - optymalizuj model szybka analiza
argument-hint: [metric] [value]
---

# Optimize RL Model

Szybka konsultacja optymalizacji modelu RL

## Parametry:

- **Metric**: `$1` (wymagane: sharpe, drawdown, win_rate, loss, convergence)
- **Value**: `$2` (opcjonalne: wartość do poprawy)

## Analiza problemu:

### Jeśli `$1` = "sharpe"
**Problem**: Niska Sharpe Ratio (< 1.0)

**Quick Fixes**:
1. Zwiększ learning rate (0.0001 → 0.0003)
2. Zmień network architecture (dodaj layer)
3. Zwiększ batch size (32 → 64)
4. Zmień reward function (dodaj risk penalty)

---

### Jeśli `$1` = "drawdown"
**Problem**: Wysoki Maximum Drawdown (> 20%)

**Quick Fixes**:
1. Zmniejsz position size (50% reduction)
2. Zwiększ stop-loss buffer
3. Dodaj portfolio diversification
4. Zwiększ risk penalty w reward

---

### Jeśli `$1` = "win_rate"
**Problem**: Niska Win Rate (< 40%)

**Quick Fixes**:
1. Zmień entry signals (tighter conditions)
2. Zwiększ exit flexibility
3. Dodaj confirmation signals
4. Zmniejsz trade frequency

---

### Jeśli `$1` = "loss"
**Problem**: Training loss nie spada

**Quick Fixes**:
1. Sprawdź data quality (brakujące dane?)
2. Resetuj network weights
3. Zmniejsz learning rate (0.0001 zamiast 0.001)
4. Zwiększ training steps (epoki)
5. Sprawdź czy reward is increasing

---

### Jeśli `$1` = "convergence"
**Problem**: Model nie konwerguje

**Quick Fixes**:
1. Sprawdź reward stability
2. Zmniejsz environment complexity
3. Resetuj model
4. Zmień optimizer (Adam → SGD)
5. Zwiększ target network update frequency

## Checklist optymalizacji:

- [ ] Sprawdzić reward function
- [ ] Sprawdzić learning rate
- [ ] Sprawdzić network architecture
- [ ] Sprawdzić data quality
- [ ] Sprawdzić hyperparameters
- [ ] Uruchomić längre training (1000+ steps)
- [ ] Sprawdzić validation on test set
- [ ] Porównać z baseline

## Performance Targets:

```
RL Model Checklist
├─ Sharpe Ratio: > 1.0 ✓
├─ Win Rate: > 45% ✓
├─ Max Drawdown: < 15% ✓
├─ Profit Factor: > 2.0 ✓
└─ Convergence: < 500 steps ✓
```

## Output format:

```
## RL Optimization: $1

**Current Value**: $2
**Target**: [recommended]

**Quick Fixes**:
1. [fix 1]
2. [fix 2]
3. [fix 3]

**Recommended Order**:
1. Try [fix 1] first
2. Measure impact
3. If < 30% improvement → Deep Dive
```

## Notatki:

⚠️ **Important**: Zawsze validuj na out-of-sample data
⚠️ **Unikaj**: Overfit risk - nie optimizuj zbyt długo
✅ **Best Practice**: Train on 80%, Validate on 20%
