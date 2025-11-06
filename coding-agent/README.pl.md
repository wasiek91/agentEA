# AI Coding Agent - Polski Agent Kodowania

Inteligentny agent AI kodowania oparty na Claude Sonnet 4.5, LangChain i LangGraph, który automatyzuje zadania programistyczne poprzez integrację narzędzi CLI.

## Funkcje

- **Workflow LangGraph**: Uporządkowany cykl planowanie-wykonanie-weryfikacja
- **Integracja Narzędzi CLI**: Bezpieczne wykonywanie komend npm, git, python, node i aider
- **Integracja Aider**: Wykorzystanie Aider do generowania i edycji kodu wspomaganego AI
- **Automatyzacja Git**: Automatyczna kontrola wersji i śledzenie zmian
- **Operacje na Plikach**: Czytanie plików, listowanie katalogów, sprawdzanie istnienia
- **Bezpieczeństwo Przede Wszystkim**: Biała/czarna lista komend, potwierdzenia, tryb testowy
- **Tryb Interaktywny i CLI**: Używaj jako jednorazowej komendy lub sesji interaktywnej
- **Pełna Automatyzacja**: Domyślnie BEZ pytania o potwierdzenie - agent działa automatycznie!

## Szybki Start

### 1. Instalacja Zależności

```bash
cd coding-agent
pip install -r requirements.txt
```

### 2. Konfiguracja Klucza API

Klucz API jest już skonfigurowany w pliku `.env`!

### 3. (Opcjonalnie) Zainstaluj Aider

```bash
pip install aider-chat
```

### 4. Użycie

```bash
# Tryb jednorazowy
python agent.py --task "Listuj pliki w aktualnym katalogu"

# Tryb interaktywny
python agent.py --interactive

# Pomoc
python agent.py --help
```

## Przykłady Użycia

### Przykład 1: Prosta Komenda
```bash
python agent.py --task "Sprawdź status git"
```

### Przykład 2: Tworzenie Aplikacji
```bash
python agent.py --task "Stwórz prostą aplikację Flask hello world w pliku app.py"
```

### Przykład 3: Tryb Interaktywny
```bash
python agent.py --interactive

Podaj zadanie: Listuj wszystkie pliki Python w katalogu tools
Podaj zadanie: Przeczytaj config.py
Podaj zadanie: Sprawdź git status
Podaj zadanie: exit
```

### Przykład 4: Złożone Zadanie
```bash
python agent.py --task "Stwórz aplikację todo z Flask z funkcjami dodawania, listowania i usuwania, następnie napisz testy pytest"
```

## Dostępne Komendy

```bash
# Podstawowe użycie
python agent.py --task "twoje zadanie"
python agent.py --interactive
python agent.py -i

# Opcje
--dry-run              # Tryb testowy (pokazuje co by zostało wykonane)
--no-confirm           # Pomiń potwierdzenia (domyślnie już wyłączone)
--help                 # Pokaż pomoc
```

## Architektura

```
┌─────────────────────────────────────────────────────┐
│              AI Coding Agent (Polski)                │
│                                                      │
│  ┌──────────┐    ┌───────────┐    ┌─────────────┐ │
│  │Planowanie│───▶│ Wykonanie │───▶│Weryfikacja  │ │
│  └──────────┘    └───────────┘    └─────────────┘ │
│       │               │                    │        │
│       └───────────────┴────────────────────┘        │
│                       │                             │
└───────────────────────┼─────────────────────────────┘
                        │
        ┌───────────────┴───────────────┐
        │                               │
   ┌────▼────┐                    ┌────▼────┐
   │Narzędzia│                    │   LLM   │
   └─────────┘                    └─────────┘
        │                              │
   ┌────┴────┬────────┬─────────┐    │
   │         │        │         │     │
 Shell    Aider    Git   System     │
                      Plików         │
                                      │
                              Claude Sonnet 4.5
```

### Dostępne Narzędzia

#### Shell Tool (`shell_executor`)
- Wykonuj bezpieczne komendy CLI
- **Biała lista**: npm, git, python, node, aider, ls, dir, pwd, cd, cat, mkdir, touch
- **Czarna lista**: rm, del, format, dd, mkfs i inne destrukcyjne komendy
- Automatyczna filtracja bezpieczeństwa

#### Narzędzia Aider
- `aider_executor`: Uruchom Aider do tworzenia/modyfikacji kodu z AI
- `aider_status`: Sprawdź status instalacji Aider

#### Narzędzia Git
- `git_status`: Zobacz status repozytorium
- `git_commit`: Commituj zmiany z automatycznym stagingiem
- `git_diff`: Zobacz różnice w plikach

#### Narzędzia Systemu Plików
- `read_file`: Czytaj zawartość plików (max 1MB)
- `list_directory`: Listuj zawartość katalogów
- `file_exists`: Sprawdź istnienie pliku/katalogu

## Konfiguracja

Edytuj `.env` aby dostosować ustawienia:

```env
# Konfiguracja API (SKONFIGUROWANE!)
ANTHROPIC_API_KEY=twój_klucz

# Model
MODEL_NAME=claude-sonnet-4-5-20250929

# Ustawienia Bezpieczeństwa
DRY_RUN_MODE=false                # true = tryb testowy
REQUIRE_CONFIRMATION=false         # false = pełna automatyzacja (DOMYŚLNE!)

# Ustawienia Agenta
VERBOSE=true                      # Pokaż szczegółowe logi
LANGUAGE=pl                       # Język (pl lub en)
```

## Przykładowe Workflow

### Workflow 1: Tworzenie Aplikacji Todo

```bash
python agent.py --task "Stwórz aplikację todo z Flask z funkcjami dodawania, listowania i usuwania oraz testy pytest"
```

**Co robi agent**:
1. **Planowanie**: Rozłożenie na kroki (stwórz Flask app, dodaj endpointy, napisz testy)
2. **Wykonanie**: Używa Aider do generowania kodu, uruchamia testy
3. **Weryfikacja**: Sprawdza wyniki testów
4. **Git Commit**: Automatycznie commituje działający kod

### Workflow 2: Analiza Kodu

```bash
python agent.py --interactive

> Przeczytaj config.py i podsumuj dostępne opcje konfiguracji
> Sprawdź czy są jakieś pliki Python w aktualnym katalogu
> Pokaż status git
```

### Workflow 3: Automatyczna Praca

```bash
python agent.py --task "Zainstaluj express z npm i stwórz podstawowy serwer"
```

Agent wykona to AUTOMATYCZNIE bez pytania!

## Struktura Projektu

```
coding-agent/
├── agent.py                    # Główny agent (Polski!)
├── config.py                   # Zarządzanie konfiguracją
├── requirements.txt            # Zależności Python
├── setup.py                    # Skrypt weryfikacji setupu
├── .env                        # Konfiguracja (GOTOWE!)
├── .env.example               # Szablon
├── .gitignore                 # Wykluczenia Git
├── README.md                  # Dokumentacja angielska
├── README.pl.md               # Ta dokumentacja (Polska!)
├── QUICKSTART.md              # Szybki start
└── tools/                     # Implementacje narzędzi (wszystkie po polsku!)
    ├── __init__.py
    ├── shell_tool.py          # Wykonywanie shell
    ├── aider_tool.py          # Integracja Aider
    ├── git_tool.py            # Operacje Git
    └── filesystem_tool.py     # Operacje na plikach
```

## Funkcje Bezpieczeństwa

### 1. Biała/Czarna Lista Komend
- Tylko zatwierdzone komendy mogą być wykonane
- Destrukcyjne komendy są automatycznie blokowane

### 2. Potwierdzenia Użytkownika (Opcjonalne)
- Domyślnie WYŁĄCZONE dla pełnej automatyzacji
- Włącz ustawiając `REQUIRE_CONFIRMATION=true` w `.env`

### 3. Tryb Testowy
```bash
python agent.py --task "twoje zadanie" --dry-run
```
- Podgląd wszystkich operacji bez wykonywania
- Idealny do testowania

### 4. Timeouty
- Komendy shell: 5 minut
- Komendy Aider: 10 minut

### 5. Limity Rozmiaru Plików
- Maksymalny rozmiar czytanego pliku: 1MB

## Rozwiązywanie Problemów

### "ANTHROPIC_API_KEY not found"
- Plik `.env` już istnieje i jest skonfigurowany!
- Jeśli problem występuje, sprawdź czy klucz jest poprawny

### "Aider not found"
```bash
pip install aider-chat
```

### "Komenda zablokowana przez filtr"
- Sprawdź białą listę w `config.py`
- Upewnij się że komenda jest bezpieczna
- Dodaj do białej listy jeśli odpowiednie

## Polecenia w Języku Naturalnym

Agent rozumie polskie komendy! Przykłady:

```bash
python agent.py --task "Stwórz prostą aplikację webową"
python agent.py --task "Dodaj testy do mojego kodu"
python agent.py --task "Napraw błędy w pliku app.py"
python agent.py --task "Zcommituj wszystkie zmiany do git"
python agent.py --task "Pokaż mi wszystkie pliki Python"
```

## Tryb Pełnej Automatyzacji

**DOMYŚLNIE WŁĄCZONY!** Agent ma pełną kontrolę i nie pyta o potwierdzenie.

```python
# W config.py i .env:
REQUIRE_CONFIRMATION = false  # DOMYŚLNIE!
```

Agent:
- ✅ Automatycznie wykonuje wszystkie bezpieczne komendy
- ✅ Używa Aider bez pytania
- ✅ Commituje do Git automatycznie
- ✅ Działa aż do ukończenia zadania
- ⚠️ Nadal blokuje destrukcyjne komendy (rm, del, format)

Aby WŁĄCZYĆ potwierdzenia:
```env
REQUIRE_CONFIRMATION=true
```

## Wskazówki

1. **Bądź Konkretny**: Zamiast "zrób aplikację", powiedz "stwórz aplikację Flask z endpointem /hello zwracającym JSON"

2. **Podziel Złożone Zadania**: Dla dużych projektów, uruchom wiele mniejszych zadań w trybie interaktywnym

3. **Użyj Trybu Testowego**: Przetestuj złożone zadania z `--dry-run` najpierw

4. **Zaufaj Agentowi**: Z wyłączonymi potwierdzeniami agent ma pełną kontrolę - zaufaj mu!

5. **Zacznij Prosto**: Zacznij od listowania i czytania plików aby się oswoić

## Technologie

- **LangChain**: Framework aplikacji LLM
- **LangGraph**: Orkiestracja workflow ze zarządzaniem stanem
- **Claude Sonnet 4.5**: Najnowszy model Anthropic
- **langchain-anthropic**: Oficjalna integracja Anthropic
- **Rich**: Piękne formatowanie terminala
- **Python-dotenv**: Zarządzanie środowiskiem
- **Aider** (opcjonalnie): Programowanie parami z AI

## Status

**GOTOWY DO UŻYCIA!**

- ✅ Wszystkie komponenty przetłumaczone na polski
- ✅ Pełna automatyzacja domyślnie włączona
- ✅ Klucz API skonfigurowany
- ✅ Bezpieczeństwo zapewnione
- ✅ Gotowy do pracy!

## Przykłady Rzeczywistego Użycia

### Szybka Analiza Projektu
```bash
python agent.py --interactive

> Listuj wszystkie pliki w projekcie
> Przeczytaj package.json i powiedz jakie są zależności
> Sprawdź git status
> exit
```

### Automatyczne Tworzenie Kodu
```bash
python agent.py --task "Stwórz REST API z Express.js z endpointami GET /users i POST /users, dodaj walidację i obsługę błędów"
```

### Refaktoryzacja i Testy
```bash
python agent.py --task "Przejrzyj wszystkie pliki .py, dodaj docstringi i type hints, następnie stwórz testy jednostkowe"
```

## Wsparcie

Aby uzyskać pomoc:
- Sprawdź sekcję Rozwiązywanie Problemów
- Przejrzyj dokumentację narzędzi w plikach źródłowych
- Upewnij się że wszystkie zależności są poprawnie zainstalowane
- Spróbuj uruchomić z flagami `--dry-run` i `--verbose`

## Licencja

MIT License - używaj i modyfikuj według potrzeb.

---

**Miłego kodowania z AI!** 🚀

Agent jest gotowy i czeka na Twoje polecenia po polsku!
