---
allowed-tools: Read, Grep, Bash(git:*), Bash(python:*)
description: Pełny przegląd - kod + architektura + testy workflow
argument-hint: [file-or-feature]
---

# Full Review Workflow

Wykonaj kompleksowy przegląd dla: `$1`

## Co to robi:

Orchestruje pełny workflow review:
1. **Szybka kontrola kodu** (`/check-code`)
2. **Głębokie review'u** (Agent Code Reviewer)
3. **Architektura** (Agent Architecture Advisor)
4. **Testy** (Agent Test Generator)
5. **Finał** - podsumowanie

## Kroki:

### KROK 1: Szybka kontrola
```
/check-code $1
```
→ Linting, security, formatting check
→ Czas: ~2 min

**Jeśli FAIL**: Zatrzymaj, popraw, wróć

---

### KROK 2: Code Review (głębokie)

Użyj Code Reviewer skill do głębokie analizy bezpieczeństwa, wydajności, best practices

→ Czas: ~10 min
→ Output: Lista ulepszeń

**Jeśli major issues**: Zatrzymaj i napraw

---

### KROK 3: Architecture Check

Użyj Architecture Advisor skill do oceny design patterns, scalability, integration

→ Czas: ~10 min
→ Output: Architectural recommendations

**Jeśli redesign potrzebny**: Zlecenie refactoru

---

### KROK 4: Test Coverage
```
/generate-tests main_function $1
```

Użyj Test Generator skill do comprehensive testów z edge cases

→ Czas: ~15 min

**Uruchom testy**:
```bash
pytest test_$1.py -v --cov
```

---

### KROK 5: Podsumowanie

Zbierz wszystkie wyniki:

```
## Full Review Summary: $1

### 📋 Quick Check
Status: [PASS/FAIL]
Issues: [N]

### 🔍 Code Review
Issues: [N major, M minor]
Top concerns: [list]

### 🏗️ Architecture
Rating: [good/needs-work/redesign]
Recommendations: [list]

### ✅ Tests
Coverage: [%]
Status: [complete/gaps]

### 📊 Final Verdict
READY: [ ] / NEEDS_WORK: [ ] / BLOCKED: [ ]

### 🎯 Next Steps
1. [action]
2. [action]
3. [action]
```

## Tempo:

- **Quick Review**: Tylko KROK 1 + 2 (~15 min)
- **Standard Review**: KROKI 1-4 (~40 min)
- **Comprehensive**: KROKI 1-5 + detailed analysis (~60 min)

## Workflow dla feature'a:

```
git checkout -b feature/new-feature
    ↓
code changes
    ↓
/full-review src/new_feature.py
    ↓
Fix issues iteratively
    ↓
git add . && git commit
    ↓
Push & Create PR
```

## Success Criteria:

✅ All checks pass
✅ No security issues
✅ 80%+ test coverage
✅ Approvals z agentów
✅ Ready for production
