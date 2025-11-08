# 🤝 Dual Agent Workflow - Claude Code + Coding Agent

## 🎯 Filozofia: Najlepsze z Obu Światów

**Claude Code** (interaktywny) + **Coding Agent** (autonomiczny) = 💪 Super produktywność!

---

## 🔄 Master Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    TWÓJ PROJEKT                              │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────┐
        │   Potrzebujesz pomocy AI?             │
        └───────────────────────────────────────┘
                            │
                ┌───────────┴───────────┐
                │                       │
                ▼                       ▼
    ┌─────────────────────┐   ┌─────────────────────┐
    │  INTERAKTYWNA       │   │  AUTONOMICZNA       │
    │  PRACA              │   │  PRACA              │
    │                     │   │                     │
    │  npx claude         │   │  python agent.py    │
    │  (Claude Code)      │   │  (Coding Agent)     │
    └─────────────────────┘   └─────────────────────┘
                │                       │
                │                       │
                ▼                       ▼
    ┌─────────────────────┐   ┌─────────────────────┐
    │ Pair Programming    │   │ Batch Processing    │
    │ Learning            │   │ Automatyzacja       │
    │ Debugging           │   │ Background Tasks    │
    │ Design Decisions    │   │ Repetitive Work     │
    └─────────────────────┘   └─────────────────────┘
                │                       │
                └───────────┬───────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │   GOTOWY      │
                    │   PROJEKT     │
                    └───────────────┘
```

---

## 📋 Praktyczne Scenariusze

### Scenariusz 1: Nowa Aplikacja od Zera 🆕

**Faza 1: Planowanie z Claude Code (Interaktywne)**
```powershell
# Terminal 1: Uruchom Claude Code
cd C:\Users\HP\OneDrive\Pulpit\Cloude
npx claude
```

**Rozmowa:**
```
Ty: "Chcę stworzyć aplikację TODO z Flask. Pomóż mi zaplanować strukturę."

Claude: *dyskutuje z Tobą, sugeruje architekturę, best practices*

Ty: "OK, zróbmy MVC pattern z SQLite. Jak podzielić foldery?"

Claude: *tworzy strukturę folderów i podstawowe pliki*
      - app.py
      - models/
      - views/
      - controllers/
      - templates/
```

**Faza 2: Implementacja przez Coding Agent (Autonomiczne)**
```powershell
# Terminal 2: Uruchom Coding Agent
cd C:\Users\HP\OneDrive\Pulpit\Cloude\coding-agent

python agent.py --task "Zaimplementuj CRUD operations dla TODO items zgodnie ze strukturą w ../app.py"
```

**Agent sam:**
- Czyta strukturę projektu
- Implementuje wszystkie CRUD operations
- Tworzy testy
- Commituje do git

**Faza 3: Review i Polish z Claude Code**
```
Ty: "Sprawdź kod wygenerowany przez agenta"

Claude: *reviewuje, sugeruje optymalizacje*

Ty: "Dodajmy authentication"

Claude: *dodaje auth z wyjaśnieniem*
```

---

### Scenariusz 2: Refactoring Istniejącego Kodu 🔧

**Faza 1: Analiza z Claude Code**
```
Ty: "Ten kod jest zbyt skomplikowany, jak możemy to uprościć?"

Claude: *analizuje, sugeruje pattern, pokazuje przykłady*

Ty: "Świetnie! Zastosujmy Strategy Pattern"

Claude: *tworzy przykład jednej klasy*
```

**Faza 2: Bulk Refactoring przez Coding Agent**
```powershell
python agent.py --task "Zastosuj Strategy Pattern do wszystkich klas w module services/"
```

**Agent sam:**
- Znajduje wszystkie odpowiednie klasy
- Refaktoryzuje każdą
- Aktualizuje testy
- Weryfikuje że wszystko działa

**Faza 3: Verification z Claude Code**
```
Ty: "Sprawdź czy refactoring jest OK"

Claude: *code review, testy integration*
```

---

### Scenariusz 3: Bug Fixing 🐛

**Faza 1: Debug z Claude Code**
```
Ty: "Mam błąd w app.py linii 45"

Claude: *analizuje, znajduje przyczynę, wyjaśnia*

Ty: "Jak to naprawić?"

Claude: *pokazuje rozwiązanie, poprawia kod*
```

**Faza 2: Podobne Bugi - Coding Agent**
```powershell
python agent.py --task "Znajdź i napraw wszystkie podobne błędy w całym projekcie"
```

---

### Scenariusz 4: Dodawanie Features 🎨

**Workflow:**
```
1. [Claude Code] Design API endpoint z Tobą
2. [Claude Code] Stwórz pierwszy endpoint jako przykład
3. [Coding Agent] "Stwórz pozostałe 10 endpointów według tego samego wzorca"
4. [Claude Code] Review i testy integration
5. [Coding Agent] "Wygeneruj dokumentację API dla wszystkich endpointów"
```

---

## 🎮 Live Demo - Stwórzmy Coś Razem!

### Demo: Mini Blog API

**KROK 1: Ty + Claude Code (Interaktywnie)**

Najpierw razem zaprojektujmy:
```
Ty: npx claude

Potem w rozmowie:
- Zaprojektujemy strukturę DB
- Stworzymy pierwszy endpoint (POST /posts)
- Napiszemy testy dla niego
```

**KROK 2: Coding Agent (Autonomicznie)**

Potem agent dokończy resztę:
```powershell
python agent.py --task "Dodaj pozostałe CRUD endpointy (GET, PUT, DELETE) używając tego samego pattern co POST"
```

**KROK 3: Ty + Claude Code (Review)**

Wracamy do Ciebie:
```
- Sprawdzamy co zrobił agent
- Poprawiamy detale
- Dodajemy authentication
- Optymalizujemy
```

**Chcesz to zrobić TERAZ?** 🚀

---

## 🛠️ Setup dla Dual Workflow

### Przygotowanie (jednorazowe):

**1. Utwórz skrypt launcher:**

```powershell
# File: start-dual-workflow.ps1
Write-Host "=== Dual Agent Workflow ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Terminal 1: Claude Code (interaktywny)" -ForegroundColor Green
Write-Host "Terminal 2: Coding Agent (autonomiczny)" -ForegroundColor Yellow
Write-Host ""

# Uruchom dwa okna PowerShell
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'C:\Users\HP\OneDrive\Pulpit\Cloude'; Write-Host 'Claude Code - Gotowy do uruchomienia: npx claude' -ForegroundColor Green"

Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'C:\Users\HP\OneDrive\Pulpit\Cloude\coding-agent'; Write-Host 'Coding Agent - Gotowy. Użyj: python agent.py --interactive' -ForegroundColor Yellow"
```

**2. Struktura projektu dla współpracy:**

```
projekty/
├── moja-aplikacja/
│   ├── src/
│   ├── tests/
│   └── README.md
│
└── .workspace
    ├── claude-context.md      # Notatki z rozmów z Claude
    ├── agent-tasks.md         # Historia zadań dla agenta
    └── decisions.md           # Decyzje projektowe
```

---

## 📊 Kiedy Używać Którego - Quick Reference

| Zadanie | Claude Code | Coding Agent | Dlaczego? |
|---------|-------------|--------------|-----------|
| **Planning** | ✅ | ❌ | Potrzebujesz dyskusji |
| **Learning** | ✅ | ❌ | Wyjaśnienia krok po kroku |
| **Prototyping** | ✅ | ❌ | Szybkie iteracje |
| **Design Decisions** | ✅ | ❌ | Wymaga kreatywności |
| **Code Review** | ✅ | ❌ | Potrzebujesz insightów |
| **Debugging Complex** | ✅ | ❌ | Interaktywny proces |
| | | | |
| **Repetitive Tasks** | ❌ | ✅ | Automatyzacja |
| **Batch Processing** | ❌ | ✅ | Wiele podobnych operacji |
| **Boilerplate Code** | ❌ | ✅ | Powtarzalny wzorzec |
| **Testing Generation** | ❌ | ✅ | Mechaniczne |
| **Documentation** | ❌ | ✅ | Systematyczne |
| **Refactoring Bulk** | ❌ | ✅ | Wiele plików |
| | | | |
| **First Implementation** | ✅ | ❌ | Uczysz się |
| **Scaling Pattern** | ❌ | ✅ | Powtarzasz wzorzec |
| **Final Polish** | ✅ | ❌ | Optymalizacja |

---

## 🎯 Best Practices

### DO ✅

1. **Start z Claude Code**
   - Planuj architekturę
   - Twórz prototypy
   - Ucz się nowych konceptów

2. **Delegate do Coding Agent**
   - Implementacja powtarzalnych patterns
   - Bulk operations
   - Mechaniczne zadania

3. **Finish z Claude Code**
   - Code review
   - Optymalizacja
   - Dokumentacja wysokiego poziomu

### DON'T ❌

1. **Nie używaj Coding Agent do:**
   - Kreatywnych decyzji
   - Learningowych sesji
   - Niejednoznacznych zadań

2. **Nie używaj Claude Code do:**
   - Generowania 100 podobnych plików
   - Repetitive refactoring
   - Mechanicznych operacji

---

## 💬 Przykładowe Komendy

### Claude Code (Interaktywne)
```bash
npx claude

# W rozmowie:
"Pomóż mi zrozumieć ten błąd"
"Zaprojektujmy API dla user management"
"Co to jest dependency injection?"
"Zrób code review tego PR"
"Jak najlepiej zorganizować ten kod?"
```

### Coding Agent (Zadaniowe)
```bash
# Single task
python agent.py --task "Dodaj type hints do wszystkich funkcji"

# Interactive mode
python agent.py --interactive

# Dry run (test mode)
python agent.py --task "Refaktoryzuj moduł auth" --dry-run

# With confirmation
python agent.py --task "Usuń nieużywane importy" --no-confirm
```

---

## 🔗 Integracja i Komunikacja

### Shared Context (Współdzielony Kontekst)

**Utwórz plik .workspace/context.md:**
```markdown
# Project Context

## Architecture Decisions
- [2025-01-06] Używamy MVC pattern (Claude Code session)
- [2025-01-06] SQLite dla development (Claude Code)

## Completed Tasks
- [Agent] Generated all CRUD operations
- [Claude] Designed API structure
- [Agent] Added tests for all endpoints

## Next Steps
- [ ] Add authentication (Claude)
- [ ] Generate API docs (Agent)
- [ ] Performance optimization (Claude)
```

**Oba narzędzia mogą to czytać:**
```python
# W agent.py
def read_project_context():
    with open('../.workspace/context.md') as f:
        return f.read()
```

---

## 🎓 Tutorial: Twoja Pierwsza Dual Session

### Zróbmy to TERAZ! Step by step:

**Zadanie:** Stwórzmy prosty Task Manager API

#### Step 1: Claude Code - Design (5 min)
```powershell
# Otwórz Terminal 1
cd C:\Users\HP\OneDrive\Pulpit\Cloude
npx claude
```

```
Ty: "Zaprojektujmy Task Manager API. Potrzebuję:
     - Create task
     - List tasks
     - Update task
     - Delete task
     Jaka struktura będzie najlepsza?"

Ja (Claude): *Dyskutuję, sugeruję strukturę, tworzę schemat*
```

#### Step 2: Claude Code - Prototype (10 min)
```
Ty: "Stwórz pierwszy endpoint - POST /tasks"

Ja: *Tworzę kod z wyjaśnieniami*
```

#### Step 3: Coding Agent - Implementation (5 min)
```powershell
# Terminal 2
cd C:\Users\HP\OneDrive\Pulpit\Cloude\coding-agent

python agent.py --task "Używając wzorca z POST /tasks, stwórz pozostałe endpointy: GET, PUT, DELETE dla /tasks"
```

*Agent pracuje autonomicznie*

#### Step 4: Claude Code - Review (5 min)
```
Ty: "Sprawdź kod wygenerowany przez agenta w ../task-manager/"

Ja: *Reviewuję, sugeruję poprawki*
```

#### Step 5: Coding Agent - Polish (3 min)
```powershell
python agent.py --task "Dodaj error handling i logging do wszystkich endpointów"
```

#### Step 6: Claude Code - Testing (5 min)
```
Ty: "Dodajmy integration tests"

Ja: *Tworzę testy razem z Tobą*
```

**CHCESZ ZROBIĆ TO TERAZ?** Mogę przeprowadzić Cię przez cały proces! 🚀

---

## 🎉 Podsumowanie

### Dual Agent Workflow =

```
Claude Code      = Twój mózg + doświadczenie
Coding Agent     = Twoje ręce + automatyzacja
                   ────────────────────────────
                   = Super produktywny developer! 💪
```

### Złota Reguła:

> **"Myśl z Claude, Działaj przez Agent"**

---

## 🤝 Gotowy na Demo?

Powiedz mi co chcesz zbudować i przeprowadzimy pierwszy dual workflow session!

Opcje:
- **A)** Mini blog API (15 min)
- **B)** Task Manager (20 min)
- **C)** User Authentication System (30 min)
- **D)** Twój własny pomysł - powiedz mi co!

Co wybierasz? 😊
