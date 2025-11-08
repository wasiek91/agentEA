# 🤖 agentEA Specialized Agents

Kompletes zestaw wyspecjalizowanych agentów Claude Code do zarządzania projektami **agentEA** (Portfolio Manager Pro + Janosik EA + Coding Agent).

## 📋 Dostępni agenci

### 1️⃣ **Code Reviewer** - Przegląd kodu
```powershell
.\run-code-reviewer.ps1
```

**Specjalizacja:**
- ✅ Analiza jakości kodu (czystość, czytelność, maintainability)
- ✅ Bezpieczeństwo (OWASP, injection, XSS, SQL injection)
- ✅ Wydajność i optymalizacja
- ✅ Design patterns i best practices
- ✅ Testy jednostkowe i integracyjne

**Kiedy użyć:**
- Przegląd nowego kodu przed merge'em
- Audyt bezpieczeństwa kodu
- Refaktoryzacja dla czytelności
- Sprawdzenie czy kod jest testowany

**Przykład:**
```powershell
# Kontynuuj ostatnią rozmowę
.\run-code-reviewer.ps1

# Nowa sesja
.\run-code-reviewer.ps1 -NewSession

# Pytanie
.\run-code-reviewer.ps1 -Query "Przejrzyj portfolio-manager-pro/main.py pod kątem bezpieczeństwa"
```

---

### 2️⃣ **RL Expert** - Konsultacje Reinforcement Learning
```powershell
.\run-rl-expert.ps1
```

**Specjalizacja:**
- 🧠 Algorytmy: PPO, DQN, A3C, DDPG, SAC
- 🧠 Hiperparametry i tuning
- 🧠 Reward shaping i design
- 🧠 Exploration vs Exploitation trade-offs
- 🧠 Stability i convergence
- 🧠 Metryki i ocena modeli
- 🧠 Environment design

**Dla agentEA:**
- Optymalizacja strategii handlu
- Risk management i drawdown control
- Portfolio optimization
- Backtesting i out-of-sample testing

**Kiedy użyć:**
- Optymalizacja modelu RL
- Tuning hiperparametrów
- Diagnoza problemów z konwergencją
- Design reward function
- Strategia exploracji

**Przykład:**
```powershell
# Kontynuuj ostatnią rozmowę
.\run-rl-expert.ps1

# Nowa sesja z konkretnym pytaniem
.\run-rl-expert.ps1 -NewSession -Query "Jak zmniejszyć drawdown w PPO?"
```

---

### 3️⃣ **Architecture Advisor** - Decyzje projektowe
```powershell
.\run-architecture.ps1
```

**Specjalizacja:**
- 🏗️ Architektura systemów (monolith vs microservices)
- 🏗️ Design patterns
- 🏗️ Scalability i performance
- 🏗️ Database design
- 🏗️ API design
- 🏗️ Message queues i async processing
- 🏗️ Deployment strategies
- 🏗️ Technical debt management

**Dla agentEA:**
- Integracja Portfolio Manager Pro + Janosik EA + Coding Agent
- PostgreSQL schema optimization
- REST API design
- Real-time monitoring architecture
- Distributed system design

**Kiedy użyć:**
- Planowanie nowej funkcji
- Decyzja monolith vs microservices
- Optymalizacja bazy danych
- Planowanie skalowania
- Architektura monitoring systemu

**Przykład:**
```powershell
# Konsultacja na nowy temat
.\run-architecture.ps1 -NewSession -Query "Jak zintegrowac Janosik EA z Portfolio Manager?"

# Kontynuuj rozmowę
.\run-architecture.ps1
```

---

### 4️⃣ **Test Generator** - Automatyzacja testów
```powershell
.\run-test-generator.ps1
```

**Specjalizacja:**
- ✅ Testy jednostkowe (pytest, unittest)
- ✅ Testy integracyjne
- ✅ Testy end-to-end
- ✅ Test coverage analysis
- ✅ Edge case identification
- ✅ Mocking i fixtures
- ✅ Performance testing
- ✅ Load testing

**Dla agentEA:**
- Testowanie strategii handlu (mock MT5 data)
- Testowanie modeli RL
- Testowanie API (mock bazy danych)
- Edge cases: market crashes, connection losses, timeout'y

**Kiedy użyć:**
- Generowanie testów do nowej funkcji
- Zwiększenie test coverage
- Testowanie edge cases
- Testy integracyjne
- Performance testing

**Przykład:**
```powershell
# Wygeneruj testy do konkretnego pliku
.\run-test-generator.ps1 -NewSession -Query "Wygeneruj testy dla portfolio-manager-pro/risk_manager.py"

# Kontynuuj rozmowę o testach
.\run-test-generator.ps1
```

---

## ⚡ Slash Commands (Szybkie operacje)

Dla szybkich operacji **bez otwierania pełnej sesji**:

### 🔍 `/analyze-strategy` - Przeanalizuj strategię
```bash
/analyze-strategy portfolio_v2.py
```
- Wydajność, risk metrics, rekomendacje
- Czas: ~2 min
- Output: Szybka ocena strategii

### 🧪 `/test-backtest` - Uruchom backtest
```bash
/test-backtest rl_strategy 1y 2023-01-01
```
- Period, return, sharpe ratio, drawdown
- Czas: ~5 min
- Output: Backtest results + CSV

### 🔎 `/check-code` - Szybka kontrola kodu
```bash
/check-code portfolio-manager-pro/main.py
```
- Linting, security, formatting
- Czas: ~2 min
- Output: Issues + recommendations

### 📝 `/generate-tests` - Template testów
```bash
/generate-tests calculate_sharpe risk_manager.py
```
- Wygeneruj szablony testów
- Czas: ~2 min
- Output: Test skeleton do implementacji

### 🧠 `/optimize-model` - Szybka konsultacja RL
```bash
/optimize-model sharpe 0.8
```
- Quick fixes dla problemu
- Czas: ~2 min
- Output: Rekomendacje + podziałania

### ✅ `/full-review` - Pełny workflow
```bash
/full-review new_feature.py
```
- Orchestruje: code check → review → architecture → tests
- Czas: ~40 min
- Output: Kompleksowy raport + podsumowanie

---

## 🔗 Integracja: Slash Commands + Agenty

### Workflow dla feature'a:

```
1. /check-code new_feature.py          ← Szybka kontrola
2. /full-review new_feature.py         ← Jeśli problemy
3. .\run-code-reviewer.ps1             ← Głębokie review
4. .\run-architecture.ps1              ← Architektura
5. /generate-tests main_func           ← Testy template
6. .\run-test-generator.ps1            ← Głębokie testy
```

### Workflow dla optymalizacji:

```
1. /analyze-strategy strategy.py        ← Szybka analiza
2. /optimize-model drawdown 25          ← Quick fixes
3. .\run-rl-expert.ps1                  ← Głębokie konsultacje
4. /test-backtest strategy.py           ← Validacja
```

### Workflow dla bug'a:

```
1. /check-code fixed_file.py            ← Linting + security
2. .\run-code-reviewer.ps1              ← Code review
3. /generate-tests fixed_function       ← Test template
4. .\run-test-generator.ps1             ← Pełne testy
5. pytest                               ← Uruchom testy
```

### Kiedy użyć czego:

| Sytuacja | Narzędzie | Czas |
|----------|-----------|------|
| **Szybka kontrola** | `/check-code` | 2 min |
| **Szybka analiza** | `/analyze-strategy` | 2 min |
| **Głębokie review** | `.\run-code-reviewer.ps1` | 15 min |
| **Architektura** | `.\run-architecture.ps1` | 20 min |
| **Optymalizacja RL** | `.\run-rl-expert.ps1` | 30 min |
| **Testy** | `.\run-test-generator.ps1` | 20 min |
| **Pełny przegląd** | `/full-review` | 40 min |

---

## 🚀 Szybki start

### Instalacja uprawnień wykonywania skryptów

Jeśli otrzymasz błąd `cannot be loaded because running scripts is disabled`:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Pierwsze użycie

1. **Zacznij od architekta** - planowanie struktury
```powershell
.\run-architecture.ps1 -NewSession -Query "Jaka powinna być architektura agentEA?"
```

2. **Potem Code Reviewer** - kontrola jakości
```powershell
.\run-code-reviewer.ps1 -NewSession
```

3. **RL Expert do optymalizacji** - tuning modeli
```powershell
.\run-rl-expert.ps1 -NewSession
```

4. **Test Generator na koniec** - testy
```powershell
.\run-test-generator.ps1 -NewSession
```

---

## 🎯 Workflow rekomendowany

### Dla nowej funkcji:

```
1. Architecture Advisor    → planowanie struktury
   .\run-architecture.ps1

2. Code Review            → kontrola implementacji
   .\run-code-reviewer.ps1

3. Test Generator         → pisanie testów
   .\run-test-generator.ps1
```

### Dla optymalizacji:

```
1. RL Expert             → analiza modelu
   .\run-rl-expert.ps1

2. Code Reviewer         → przegląd zmian
   .\run-code-reviewer.ps1

3. Test Generator        → testy regresyjne
   .\run-test-generator.ps1
```

### Dla refaktoryzacji:

```
1. Architecture Advisor  → planowanie zmian
   .\run-architecture.ps1

2. Code Reviewer         → przegląd kodu
   .\run-code-reviewer.ps1

3. Test Generator        → nowe testy
   .\run-test-generator.ps1
```

---

## 💡 Wskazówki

### Kontynuacja rozmowy

Każdy agent pamięta ostatnią rozmowę. Bez flag uruchamia się w trybie kontynuacji:

```powershell
.\run-code-reviewer.ps1          # Kontynuuje ostatnią rozmowę
.\run-code-reviewer.ps1 -NewSession  # Nowa sesja
```

### Szybkie pytania bez sesji

```powershell
.\run-architecture.ps1 -Query "Jak zbudować API dla agentEA?"
# Uruchomi jednorazową sesję z pytaniem i wyświetli odpowiedź
```

### Transferring context

Możesz przekazywać output z jednego agenta do drugiego:

```powershell
# Najpierw Architekt planuje
.\run-architecture.ps1 -NewSession

# Potem Reviewer przegląda
.\run-code-reviewer.ps1 -NewSession -Query "Przejrzyj plan architekturalny"
```

---

## 🔧 Zmiana konfiguracji

Każdy skrypt ma zapamiętaną konfigurację agenta. Aby zmienić prompt, edytuj skrypt:

```powershell
# Otwórz skrypt w edytorze
code .\run-code-reviewer.ps1

# Zmień prompt w sekcji:
# $agentConfig = @{
#   "code-reviewer" = @{
#     "prompt" = @" ... "@
```

---

## 📊 Porównanie agentów

| Aspekt | Code Reviewer | RL Expert | Architecture | Test Generator |
|--------|---------------|-----------|--------------|----------------|
| **Model** | Sonnet | Sonnet | Sonnet | Haiku |
| **Szybkość** | Średnia | Wolna | Wolna | Szybka |
| **Głębia** | Wysoka | Wysoka | Bardzo wysoka | Średnia |
| **Użycie** | QA | Optymalizacja | Planowanie | Automacja |
| **Narzędzia** | Read, Grep, Bash | Read, Grep, Bash | Read, Glob, Grep | Read, Write, Edit, Bash |

---

## 📝 Notatki

- Agenty pracują na ostatnich wersjach kodu w projekcie
- Każdy agent ma dostęp do wszystkich plików w `.claude/`
- Bezpieczeństwo: destrukcyjne komendy (`rm -rf`) wymagają potwierdzenia
- Extended Thinking jest zawsze włączony dla głębokich analiz

---

## 🐛 Troubleshooting

### Skrypt się nie uruchamia

```powershell
# Sprawdź politykę wykonywania
Get-ExecutionPolicy

# Ustaw na RemoteSigned
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Agent nie pamięta ostatniej rozmowy

```powershell
# Musisz być w tym samym folderze
cd C:\Users\HP\OneDrive\Pulpit\Cloude

# Potem uruchom
.\run-code-reviewer.ps1
```

### Błąd: "Unrecognized field"

Skrypt JSON ma limit znaków. Jeśli dostaniesz błąd JSON:
- Skróć prompt
- Usuń komentarze
- Edytuj skrypt bezpośrednio

---

## 🎓 Nauka

Każdy skrypt ma sekcję `.SYNOPSIS` i `.DESCRIPTION` z pomocą:

```powershell
Get-Help .\run-code-reviewer.ps1 -Full
```

---

**Gotowy do pracy! 🚀**

Zaproponuj agentów kolegom - są dzieleni przez Git w `.claude/settings.local.json`!
