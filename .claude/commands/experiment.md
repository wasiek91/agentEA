---
allowed-tools: Read, Write, Edit, Bash, Grep
description: Start eksperymentalnej sesji z checkpointing - bezpieczne testy
argument-hint: [experiment-name]
---

# Start Experimental Session

Rozpocznij eksperymentalną sesję z automatycznym checkpointing'iem!

## Co to robi:

1. **Checkpoint** - Bieżący stan kodu jest zapamiętany
2. **Eksperymentuj** - Bez strachu zmień kod
3. **Test** - Sprawdzaj czy działa
4. **Rewind** - Jeśli nie działa, wróć do tyłu (Esc+Esc)
5. **Commit** - Jak będzie OK, zacommituj do Git

## Session Types:

### 1️⃣ RL Hyperparameter Tuning
```
/experiment rl_tuning_v2
```
- Eksperymentuj z hyperparameters
- Test na backtest data
- `/rewind` jeśli performance gorzej

### 2️⃣ Strategy Refactoring
```
/experiment strategy_refactor_poc
```
- Refaktoryzuj strategy_framework.py
- Uruchom testy
- `/rewind` jeśli testy failują

### 3️⃣ Architecture Spike
```
/experiment janosik_integration
```
- Spróbuj integracji Janosik EA
- Testuj API
- `/rewind` jeśli coś się psuje

### 4️⃣ A/B Testing
```
/experiment ab_test_strategy_params
```
- Utwórz dwie wersje strategii
- Porównaj performance
- Zatrzymaj lepszą

### 5️⃣ Code Optimization
```
/experiment optimize_risk_manager
```
- Optimizuj performance kodu
- Uruchom benchmarks
- Jeśli regres → `/rewind`

## Workflow:

```
┌─────────────────────────────────┐
│ /experiment [name]              │
│ ↓                               │
│ Checkpoint: Automatycznie       │
│ ↓                               │
│ EKSPERYMENTUJ                   │
│ - zmień kod                     │
│ - uruchom testy                 │
│ - mierz metrics                 │
│ ↓                               │
│ Werdykt:                        │
│ ├─ ✅ Działa? → git commit      │
│ └─ ❌ Nie? → Esc+Esc → /rewind  │
│ ↓                               │
│ Repeat lub finish               │
└─────────────────────────────────┘
```

## Best Practices:

✅ **Plan first**: Co konkretnie chcesz testować?
✅ **Single experiment**: Jedno zagadnienie per sesję
✅ **Frequent checkpoints**: Każdy duży krok = checkpoint
✅ **Measure before/after**: Metryki przed i po
✅ **Document findings**: Notatki co nauczyłeś się

❌ **Don't**: Nie rób gigantycznych zmian naraz
❌ **Don't**: Nie zapomnij `/rewind` jeśli coś nie działa
❌ **Don't**: Nie rób commitów bez testowania

## Checkpoint Commands:

```powershell
# Otwórz menu rewind
Esc + Esc

# Możesz wybrać:
# - Rewind conversation only (keep code)
# - Rewind code only (keep conversation)
# - Rewind both (full reset)
```

## Kiedy używać:

| Scenariusz | Użyj |
|-----------|------|
| Pewny w zmianach | Regular sesja |
| Eksperymenty RL | **`/experiment`** |
| Refaktoryzacja | **`/experiment`** |
| A/B testing | **`/experiment`** |
| Nowa integracja | **`/experiment`** |
| Spike architekturalny | **`/experiment`** |

## Examples:

### RL Tuning:
```
/experiment rl_tune_sharpe
→ Zmień learning_rate
→ Zmień network architecture
→ Run backtest
→ Metrics są lepsze? Commit!
→ Metrics gorsze? /rewind
```

### Strategy Refactor:
```
/experiment refactor_buy_signal
→ Zmień buy_signal logic
→ Run unit tests
→ Run backtest
→ Wszystko zielone? Commit!
→ Coś failuje? /rewind
```

### Integration:
```
/experiment janosik_connect
→ Dodaj connection code
→ Test database link
→ Test MT5 integration
→ All working? Commit!
→ Error? /rewind
```

## Output After Experiment:

```
## Experimental Session: $1

**Checkpoint**: Created at start
**Changes Made**:
- [file1.py]: [changes]
- [file2.py]: [changes]

**Tests**:
- [test1]: ✅ PASS
- [test2]: ✅ PASS

**Metrics**:
- Before: [metric] = X
- After: [metric] = Y
- Delta: [+/- Z%]

**Verdict**: ✅ SUCCESS / ❌ FAIL

**Next Step**:
- ✅ → `git commit "feature: ..."`
- ❌ → `Esc+Esc → /rewind`
```

## Remember:

🎯 **Checkpointing = Safety Net**
🎯 **Experiment aggressively, rewind safely**
🎯 **Git = Permanent, Checkpointing = Undo**
🎯 **Solo safe, team use Git**

---

**Ready to experiment? Niech to będzie zabawe! 🚀**
