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
0. Checkpoint            → /experiment new_feature_v1
   (lub Esc+Esc → pamiętaj checkpoint)

1. Architecture Advisor    → planowanie struktury
   .\run-architecture.ps1

2. Code Review            → kontrola implementacji
   .\run-code-reviewer.ps1

3. Test Generator         → pisanie testów
   .\run-test-generator.ps1

4. Finalize              → Jeśli OK → git commit
                            Jeśli błędy → Esc+Esc → /rewind
```

### Dla optymalizacji:

```
0. Checkpoint            → /experiment rl_optimization
   (bezpieczne eksperymenty!)

1. RL Expert             → analiza modelu
   .\run-rl-expert.ps1

2. Backtest              → /test-backtest strategy.py
   (validuj zmiany)

3. Code Reviewer         → przegląd zmian
   .\run-code-reviewer.ps1

4. Test Generator        → testy regresyjne
   .\run-test-generator.ps1

5. Finalize              → Jeśli metrics lepsze → git commit
                            Jeśli regression → /rewind
```

### Dla refaktoryzacji:

```
0. Checkpoint            → /experiment refactor_spike
   (eksperymentuj bez strachu)

1. Architecture Advisor  → planowanie zmian
   .\run-architecture.ps1

2. Code Reviewer         → przegląd kodu
   .\run-code-reviewer.ps1

3. Test Generator        → nowe testy
   .\run-test-generator.ps1

4. Validate              → Wszystkie testy green?
   .\run-test-generator.ps1

5. Finalize              → Jeśli OK → git commit
                            Jeśli problemy → /rewind
```

---

## 🎬 Checkpointing - Bezpieczne Eksperymenty

Claude Code automatycznie śledzi wszystkie twoje zmiany w pliku. Jeśli coś pójdzie nie tak, możesz wrócić do poprzedniego stanu!

### Jak to działa:

**Przed każdą zmianą** → Automatyczny checkpoint
**Esc + Esc** lub `/rewind` → Wróć do dowolnego punktu

### Use Cases dla agentEA:

#### 1️⃣ **Eksperymenty z RL bez ryzyka**
```
1. Checkpoint: Baseline model
2. Zmień hyperparameters
3. Training nie działa? → /rewind
4. Spróbuj inne parametry
```
✅ Bezpieczeństwo: zawsze wróć do working version

#### 2️⃣ **Refaktoryzacja architekturalna**
```
1. Checkpoint: Current code
2. Refaktoryzuj strategy_framework.py
3. Tests failują? → /rewind
4. Spróbuj inne podejście
```

#### 3️⃣ **A/B Testing strategii**
```
1. Strategy A (checkpoint)
2. Zmień parametry
3. Performance gorzej? → /rewind
4. Spróbuj Strategy B
```

#### 4️⃣ **Integracja bez strachu**
```
1. Portfolio Manager v1 (checkpoint)
2. Integruj Janosik EA
3. Połączenie się psuje? → /rewind
4. Debuguj wolniej
```

#### 5️⃣ **Iteracyjne ulepszenia**
```
1. Feature v1 (checkpoint)
2. Improvements v1
3. Regression? → /rewind
4. Improve v2
```

### Komendy:

```powershell
# Otwórz menu rewind
Esc + Esc

# Lub użyj komendy
/rewind

# Lub slash command dla expedited sesji
/experiment
```

### Co się trackuje:

✅ Edycje plików (Edit, Write narzędzia)
✅ Conversation history

❌ Nie track: Bash command changes (rm, mv, cp)
❌ Nie track: External changes poza Claude Code

### Best Practices:

| Praktyka | Opis |
|----------|------|
| **Plan before experiment** | Wiedzieć co chcesz testować |
| **Frequent checkpoints** | Każdy krok = nowy checkpoint |
| **Use /rewind liberally** | Nie bój się eksperymentować |
| **Git for permanent** | Checkpoint = undo, Git = historia |
| **Team workflows** | Checkpoints są lokalne, Git to udział |

### Limity checkpointing'u:

⚠️ **Czas**: Checkpoints persystują 30 dni (konfigurowalnie)
⚠️ **Sesje**: Tylko pliki edytowane w TEJ sesji
⚠️ **Bash**: Komendy bash nie są trackowane
⚠️ **Nie zamienia Git**: To jest "undo", nie "historia"

### Workflow: Eksperymentalna sesja

```
1. /experiment                    ← Start sesji z checkpoint
2. Eksperymentuj bez strachu
3. Jeśli OK → git commit
4. Jeśli nie OK → /rewind → spróbuj znowu
```

---

## ⚙️ Hooks Automation - Automatyzacja Przepływu Pracy

Hooks to automatyczne skrypty, które uruchamiają się w odpowiedzi na zdarzenia w Claude Code. Zwiększają bezpieczeństwo, formatowanie i spójność projektu.

### 🔧 Dostępne Hooks

#### 1️⃣ **Pre-Commit Validation** (Przed committem)
**Plik**: `.claude/hooks/pre-commit-validation.py`

Sprawdza przed każdym `git commit`:
- ✅ Testy projektów (pytest)
- ✅ Coverage analysis
- ✅ Secrets detection (hasła, klucze API)
- ✅ Type checking (mypy)

**Zachowanie**:
- ✅ Commit BLOKOWANY jeśli: testy failują, coverage za niskie, sekrety znalezione
- ✅ Commit DOZWOLONY jeśli: wszystko OK

**Przykład**:
```bash
git commit -m "feat: add new strategy"
# Hook uruchomi się automatycznie
# Wynik: ✅ All checks passed! lub ❌ Tests failed!
```

---

#### 2️⃣ **Post-Write Auto-Formatting** (Po każdym write/edit)
**Plik**: `.claude/hooks/post-write-format.sh`

Automatycznie formatuje Python pliki po każdej edycji:
- 🎨 Black (code formatting)
- 🎨 isort (import sorting)
- 🎨 mypy (type checking - opcjonalny)

**Zachowanie**:
- Uruchamia się automatycznie po każdym `Write` lub `Edit` narzędziem
- Ciche uruchomienie (brak komunikatów o sukcesie)
- Ignoruje błędy jeśli narzędzia nie zainstalowane

**Przykład**:
```bash
# Editujesz: portfolio-manager-pro/main.py
# Hook automatycznie uruchomi: black main.py && isort main.py
# Wynik: Kod zawsze sformatowany!
```

---

#### 3️⃣ **Pre-Bash Safety** (Przed poleceniami bash) ⚠️
**Plik**: `.claude/hooks/pre-bash-safety.py`

Blokuje niebezpieczne polecenia bash:
- 🛑 `rm -rf /` (wipe systemu)
- 🛑 `git push --force` (rewrite historii)
- 🛑 `dd if=... of=/dev/sd*` (wipe dysku)
- 🛑 `mkfs.* | format` (format dysku)
- ⚠️ `sudo apt | sudo yum | sudo brew` (ostrzeżenie)

**Zachowanie**:
- Polecenie BLOKOWANE natychmiast
- Zwraca błąd z opisem dlaczego
- Wymagana edycja polecenia przed ponowieniem

**Przykład**:
```bash
rm -rf /
# Hook: ❌ Blocked: rm -rf / (system wipe!)
```

---

#### 4️⃣ **Session Setup** (Na starcie sesji)
**Plik**: `.claude/hooks/session-setup.sh`

Automatycznie ustawia środowisko na starcie sesji:
- 📦 Ładuje zmienne z `.env`
- 🗄️ Sprawdza połączenie PostgreSQL
- 📚 Pokazuje ostatnie git branche

**Zachowanie**:
- Uruchamia się raz na starcie
- Ciche (wynik wyświetlany w logs)
- Kontynuuje nawet jeśli coś failnie

**Przykład**:
```
🚀 Setting up agentEA session...
📦 Loading .env...
🗄️  Checking database...
✅ Database connected
📚 Recent branches:
   master 1a2b3c4 [5 minutes ago]
   feature-rl 5e6f7g8 [2 hours ago]
✅ Session ready!
```

---

### 🔌 Konfiguracja Hooks

Hooks konfiguruje się w `.claude/settings.local.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash(git commit:*)",
        "hooks": [
          {
            "type": "command",
            "command": "python \"$CLAUDE_PROJECT_DIR/.claude/hooks/pre-commit-validation.py\"",
            "timeout": 60
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$CLAUDE_PROJECT_DIR/.claude/hooks/post-write-format.sh\"",
            "timeout": 30
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "matcher": "startup|resume",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$CLAUDE_PROJECT_DIR/.claude/hooks/session-setup.sh\"",
            "timeout": 20
          }
        ]
      }
    ]
  }
}
```

---

### 🎬 Zdarzenia Hooks

| Event | Matcher | Hooks | Timeout |
|-------|---------|-------|---------|
| **PreToolUse** | Przed narzędziem | Może zablokować | 60s |
| **PostToolUse** | Po narzędziem | Formatowanie | 30s |
| **SessionStart** | Start sesji | Setup env | 20s |

---

### 🚀 Setup Hooks

#### Instalacja uprawnień (Linux/Mac):

```bash
chmod +x .claude/hooks/*.sh
chmod +x .claude/hooks/*.py
```

#### Weryfikacja instalacji:

```bash
# Sprawdź czy pliki istnieją
ls -la .claude/hooks/

# Test hook'ów
python .claude/hooks/pre-commit-validation.py < /dev/null
bash .claude/hooks/post-write-format.sh < /dev/null
```

#### Na Windowsie (PowerShell):

Hook'i działają automatycznie (bash/python uruchamiane przez Claude Code).

Aby testować ręcznie:
```powershell
python .claude/hooks/pre-commit-validation.py
bash .claude/hooks/post-write-format.sh
```

---

### 📊 Workflow z Hooks

```
1. Editujesz plik Python
   ↓
2. Claude Code uruchamia Write/Edit
   ↓
3. Post-Write Hook uruchomi się automatycznie
   ↓
4. Plik sformatowany (black, isort, mypy)
   ↓
5. Kontynuujesz pracę z czystym kodem
```

```
1. Robisz git commit
   ↓
2. Claude Code uruchamia Bash(git commit)
   ↓
3. Pre-Commit Hook uruchomi się
   ↓
4. Sprawdzanie testów, coverage, secrets
   ↓
5. ✅ Commit zatwierdzona lub ❌ zablokowana
```

---

### 💡 Best Practices

| Praktyka | Opis |
|----------|------|
| **Śledź logi** | Sprawdzaj output hook'ów |
| **Nie ignoruj błędów** | Jeśli hook się nie uruchomił, coś może być nie tak |
| **Testy najpierw** | Zawsze run `pytest` przed committem |
| **Secrets nigdy** | Nigdy nie commituj `.env` lub klucze API |
| **Backup antes** | Zrób `git push` regularnie |

---

### 🐛 Troubleshooting

#### Hook się nie uruchomił

```bash
# 1. Sprawdź czy plik istnieje
ls .claude/hooks/

# 2. Sprawdź czy ma uprawnienia (Linux/Mac)
ls -l .claude/hooks/

# 3. Sprawdź settings.local.json - czy hook jest skonfigurowany
cat .claude/settings.local.json | grep -A 10 "hooks"
```

#### Hook failuje

```bash
# Test manualne
python .claude/hooks/pre-commit-validation.py
bash .claude/hooks/post-write-format.sh

# Powinno pokazać co jest nie tak
```

#### Format nie działa po edycji

```bash
# Sprawdzić czy black/isort zainstalowane
pip list | grep -E "black|isort"

# Zainstalować jeśli brakuje
pip install black isort
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
