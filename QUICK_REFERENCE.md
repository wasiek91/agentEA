# 🚀 Quick Reference - Dual Agent Workflow

## 📍 Lokalizacje

```
Claude Code:    C:\Users\HP\OneDrive\Pulpit\Cloude\
Coding Agent:   C:\Users\HP\OneDrive\Pulpit\Cloude\coding-agent\
```

---

## ⚡ Szybki Start

```powershell
# Uruchom oba agenty jednocześnie:
.\start-dual-workflow.ps1
```

**LUB ręcznie:**

```powershell
# Terminal 1: Claude Code
cd C:\Users\HP\OneDrive\Pulpit\Cloude
npx claude

# Terminal 2: Coding Agent
cd C:\Users\HP\OneDrive\Pulpit\Cloude\coding-agent
python agent.py --interactive
```

---

## 🎯 Kiedy Używać Którego?

| Zadanie | Claude Code | Coding Agent |
|---------|:-----------:|:------------:|
| Planowanie | ✅ | ❌ |
| Design | ✅ | ❌ |
| Learning | ✅ | ❌ |
| Prototyping | ✅ | ❌ |
| Code Review | ✅ | ❌ |
| Debugging | ✅ | ❌ |
| | | |
| Repetitive Tasks | ❌ | ✅ |
| Batch Processing | ❌ | ✅ |
| Boilerplate | ❌ | ✅ |
| Tests Generation | ❌ | ✅ |
| Documentation | ❌ | ✅ |
| Bulk Refactoring | ❌ | ✅ |

---

## 💬 Przykładowe Komendy

### Claude Code (Interaktywny)
```bash
npx claude

# Potem w rozmowie:
"Zaprojektujmy REST API"
"Pomóż mi zrozumieć ten błąd"
"Zrób code review"
"Jak najlepiej zorganizować ten kod?"
```

### Coding Agent (Zadaniowy)
```bash
# Interactive mode
python agent.py --interactive

# Single task
python agent.py --task "Dodaj type hints"

# Dry run
python agent.py --task "..." --dry-run
```

---

## 🔄 Typowy Workflow

```
1. [Claude]  Planuj i projektuj
      ↓
2. [Claude]  Stwórz prototyp/przykład
      ↓
3. [Agent]   Zaimplementuj resztę
      ↓
4. [Claude]  Review i optymalizacja
      ↓
5. [Agent]   Testy i dokumentacja
      ↓
6. [Claude]  Final polish
```

---

## 🎨 Przykładowe Scenariusze

### Nowa Funkcja
```
1. Claude:  "Zaprojektuj API endpoint dla users"
2. Claude:  Tworzy POST /users jako przykład
3. Agent:   --task "Dodaj GET, PUT, DELETE używając tego wzorca"
4. Claude:  Review i testy
```

### Refactoring
```
1. Claude:  "Jak refaktoryzować ten moduł?"
2. Claude:  Pokazuje przykład na 1 pliku
3. Agent:   --task "Zastosuj do wszystkich plików w folderze"
4. Claude:  Weryfikacja
```

### Bug Fix
```
1. Claude:  Debug i znajdź przyczynę
2. Claude:  Napraw pierwszy case
3. Agent:   --task "Znajdź i napraw podobne bugi"
4. Claude:  Testy regression
```

---

## 📁 Przydatne Pliki

- `DUAL_AGENT_WORKFLOW.md` - Pełna dokumentacja
- `start-dual-workflow.ps1` - Launcher
- `PROJECT_ROADMAP.md` - Roadmap projektu
- `TODO_PORTABLE_AGENT.md` - Plany na przyszłość

---

## 🆘 Pomoc

### Claude Code nie działa?
```powershell
# Sprawdź czy zainstalowane
cd C:\Users\HP\OneDrive\Pulpit\Cloude
npm list @anthropic-ai/claude-code

# Reinstalacja
npm install
```

### Coding Agent nie działa?
```powershell
cd C:\Users\HP\OneDrive\Pulpit\Cloude\coding-agent

# Sprawdź środowisko
python --version

# Sprawdź zależności
pip list | grep langchain
```

### DeepSeek nie działa?
```powershell
# Sprawdź API key
echo $env:DEEPSEEK_API_KEY

# Test instalacji
.\test-deepseek-simple.ps1
```

---

## 💡 Pro Tips

✅ **Zawsze zaczynaj od Claude** - planowanie jest kluczowe
✅ **Agent dla repetycji** - nie marnuj czasu na podobne zadania
✅ **Claude dla review** - świeże spojrzenie zawsze pomaga
✅ **Zapisuj decyzje** - prowadź .workspace/decisions.md
✅ **Commituj często** - obie narzędzia mogą używać git

❌ **Nie używaj Agent do kreatywnych decyzji**
❌ **Nie używaj Claude do 100 podobnych plików**
❌ **Nie przeskakuj planowania** - dobry plan = lepszy kod

---

## 🔑 Klawisze Skrótów

```
Ctrl+C          - Przerwij wykonywanie
Ctrl+D          - Wyjdź z trybu interaktywnego
Ctrl+L          - Wyczyść terminal
↑/↓            - Historia komend
Tab            - Autocomplete
```

---

## 🎯 Złota Zasada

> **"Myśl z Claude, Działaj przez Agent"**

```
Claude Code  = Twój mózg 🧠
Coding Agent = Twoje ręce 🤚
             = Super produktywność! 🚀
```

---

**Ostatnia aktualizacja:** 2025
**Wersja:** 1.0

---

*Wydrukuj i trzymaj pod ręką! 📄*
