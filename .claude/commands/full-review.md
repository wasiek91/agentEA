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
2. **Głębokie review'u** (`.\run-code-reviewer.ps1`)
3. **Architektura** (`.\run-architecture.ps1`)
4. **Testy** (`.\run-test-generator.ps1`)
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
```powershell
.\run-code-reviewer.ps1 -NewSession -Query "Przejrzyj $1"
```
→ Bezpieczeństwo, wydajność, best practices
→ Czas: ~10 min
→ Output: Lista ulepszeń

**Jeśli major issues**: Zatrzymaj i napraw

---

### KROK 3: Architecture Check
```powershell
.\run-architecture.ps1 -NewSession -Query "Czy architektura $1 jest OK?"
```
→ Design patterns, scalability, integration
→ Czas: ~10 min
→ Output: Architectural recommendations

**Jeśli redesign potrzebny**: Zlecenie refactoru

---

### KROK 4: Test Coverage
```
/generate-tests main_function $1
```
→ Test template generation
→ Czas: ~5 min

```powershell
.\run-test-generator.ps1 -NewSession -Query "Wygeneruj comprehensive testy dla $1"
```
→ Pełne testy z edge cases
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

## Skróty:

### Jeśli mało czasu:
```
/check-code $1          ← Quick version
.\run-code-reviewer.ps1 ← Deep if needed
```

### Jeśli dużo czasu:
```
/check-code $1              ← Linting
.\run-code-reviewer.ps1     ← Code review
.\run-architecture.ps1      ← Architecture
/generate-tests             ← Test template
.\run-test-generator.ps1    ← Deep tests
pytest                      ← Run tests
```

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

## Workflow dla bug'a:

```
git checkout -b fix/bug-123
    ↓
fix code
    ↓
/check-code fixed_file.py
    ↓
.\run-code-reviewer.ps1
    ↓
/generate-tests fixed_function
    ↓
pytest ← ensure no regression
    ↓
git add . && git commit
    ↓
Push & Create PR
```

## Integration z agentami:

```
┌─ /full-review
│   ├─ /check-code (szybko)
│   ├─ .\run-code-reviewer.ps1 (głębokie)
│   ├─ .\run-architecture.ps1 (design)
│   ├─ /generate-tests (template)
│   └─ .\run-test-generator.ps1 (głębokie)
│
└─ Final: Podsumowanie + rekomendacje
```

## Success Criteria:

✅ All checks pass
✅ No security issues
✅ 80%+ test coverage
✅ Approvals z 3 agentów
✅ Ready for production

## Notatki:

- Kroki są niezależne - możesz je robić w innej kolejności
- Każdy krok ma wyjście - używaj go do następnego kroku
- Jeśli duży refaktor potrzebny - zatrzymaj się i zaplanuj z Architecture
- Zawsze runuj final tests przed push'em
