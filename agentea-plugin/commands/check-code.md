---
allowed-tools: Read, Grep, Bash(python:*)
description: Szybka kontrola jakości kodu - bezpieczeństwo, formatowanie, linting
argument-hint: [file-or-directory]
---

# Quick Code Check

Wykonaj szybką kontrolę jakości dla: `$1`

## Kroki:

### 1. **Analiza statyczna**
```bash
# Python linting
pylint $1 --disable=all --enable=E,W

# Type checking
mypy $1 --ignore-missing-imports

# Format check
black --check $1 --diff
```

### 2. **Bezpieczeństwo**
- Sprawdzenie SQL injection risks
- Sprawdzenie hardcoded secrets
- Sprawdzenie insecure functions
- Sprawdzenie authentication/authorization

### 3. **Kod smells**
- Długie funkcje (> 50 linii)?
- Zmienne o krótkich nazwach (1-2 znaki)?
- Zbyt wiele parameters (> 4)?
- Duplicate code?

### 4. **Dokumentacja**
- Czy są docstrings?
- Czy są type hints?
- Czy są comments wyjaśniające logikę?

### 5. **Testing**
- Czy plik ma testy?
- Czy są edge cases testowane?
- Czy test coverage jest > 80%?

## Quick Fixes:

**Można zautomatyzować**:
```bash
# Autoformatowanie
black $1

# Sorting imports
isort $1

# Type checking hints
python -m py_compile $1
```

## Scoring:

**✅ PASS** (< 5 issues, all minor)
→ Gotowe do merge

**⚠️ REVIEW** (5-15 issues)
→ Wymaga przeglądu

**🔴 FAIL** (> 15 issues or security issues)
→ Wymaga refaktoryzacji + przeglądu

## Output format:

```
## Quick Code Check: $1

**Files**: [liczba]
**Total Lines**: [liczba]

**Lint Issues**: [E/W count]
**Security Issues**: [count]
**Coverage**: [%]

**Top Issues**:
1. [issue]
2. [issue]
3. [issue]

**Status**: [PASS/REVIEW/FAIL]
**Recommendation**: [action]
```
