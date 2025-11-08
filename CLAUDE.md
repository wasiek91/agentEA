# CLAUDE.md

**JĘZYK: POLSKI** 🇵🇱 - Wszystkie komunikaty i odpowiedzi powinny być w języku polskim.

Plik zawiera wskazówki dla Claude Code (claude.ai/code) podczas pracy z tym repozytorium.

## Przegląd Projektu

**Cloude** to zaawansowany ekosystem handlu AI łączący trzy niezależne projekty ze wspólną infrastrukturą PostgreSQL:

1. **Portfolio Manager Pro** (Ukończony) - Platforma do zarządzania portfelem wielu strategii z optymalizacją RL
2. **Janosik EA** (W trakcie) - Specjalizowany bot handlu Forex z ciągłym uczeniem
3. **Coding Agent** (Produkcja) - Autonomiczny asystent rozwoju AI wykorzystujący LangGraph

Filozofia hybrydowego przepływu: Używaj Claude Code do interaktywnych decyzji projektowych, przeglądu kodu i nauki; użyj Coding Agent do wsadowego generowania kodu i powtarzalnych zadań; użyj platform handlowych do wykonania na żywo lub testów wstecznych.

## Przegląd Architektury

### Komponenty Systemu

```
Claude Code (Interaktywny)
    ↓
┌───────────────────────────────────┐
│ Portfolio Manager Pro             │ ← Platforma Enterprise (Fazy 1-8 gotowe)
│ - 10-100+ strategii               │
│ - Optymalizacja RL                │
│ - REST API + Dashboard            │
│ - Gotowe do rozproszonego wdrożenia│
└───────────────────────────────────┘

Janosik EA (Specjalizowany)
    ↓
┌───────────────────────────────────┐
│ Janosik EA                        │ ← Zaawansowany trader (Fazy 1-2 w trakcie)
│ - 1-2 specjalizowane strategie    │
│ - Fokus XAUUSD/NASDAQ             │
│ - Ciągłe uczenie RL               │
│ - Kapitał demo $100k              │
└───────────────────────────────────┘

Coding Agent (Autonomiczny)
    ↓
┌───────────────────────────────────┐
│ Coding Agent                      │ ← Automatyzacja wsadowa (Gotowe do produkcji)
│ - Przepływ LangGraph              │
│ - Bezpieczne wykonanie CLI        │
│ - Generowanie kodu za pomocą Aider│
│ - Automatyzacja Git               │
└───────────────────────────────────┘
         ↓
    ┌────────────┐
    │ PostgreSQL │  51.77.58.92:1993
    │ bazadanych │  (pawwasfx)
    └────────────┘
         ↓
    ┌────────────┐
    │  MT5 API   │  Lokalny lub Zdalny SSH
    └────────────┘
```

## Projekty Główne

### 1. Portfolio Manager Pro (Ukończony)

**Lokalizacja**: `portfolio-manager-pro/`

**Status**: Fazy 1-8 ukończone (Gotowe do produkcji)

**Cel**: Platforma handlu enterprise'owego z wielu strategii i samouczącą się optymalizacją RL, monitoringiem w czasie rzeczywistym i zdolnościami rozproszonego wdrażania.

**Kluczowe funkcje**:
- 10-100+ jednoczesnych strategii z głosowaniem ensemble
- Optymalizacja oparta na RL (algorytmy PPO/DQN)
- REST API do zarządzania zdalnego (port 8000)
- Dashboard Dash w czasie rzeczywistym z wizualizacją Plotly
- Wielowarstwowe zarządzanie ryzykiem (poziom portfela, strategii, pozycji)
- Wsparcie MT5 lokalnie i zdalnie (oparte na SSH)
- Pełny dziennik audytu i rejestracja zgodności
- Silnik backtestingu z powtórzeniem danych historycznych
- Cel 99,9% dostępności podczas godzin rynkowych

**Stack technologiczny**: FastAPI, Dash/Plotly, SQLAlchemy ORM, Stable-Baselines3, PyTorch, Paramiko (SSH)

**Polecenia programistyczne**:
```bash
cd portfolio-manager-pro
pip install -r requirements.txt
python main.py                     # Uruchom orkiestrator handlu na żywo
python api_server.py               # Uruchom REST API (port 8000)
python dashboard.py                # Uruchom dashboard monitorowania
python backtester.py               # Uruchom test wsteczny
python rl_engine.py                # Trenuj modele RL
pytest tests/ && black . && mypy .  # Sprawdzenia jakości kodu
```

**Baza danych**: PostgreSQL (9 tabel: strategies, market_data, signals, trades, positions, portfolio_metrics, rl_training, audit_logs, alerts)

**Operacje zdalne**: Katalog `remote_mt5_scripts/` zawiera skrypty po stronie serwera do interakcji MT5 przy uruchamianiu na VPS

### 2. Janosik EA (W trakcie)

**Lokalizacja**: `janosik-ea/`

**Status**: Fazy 1-2 w trakcie

**Cel**: Specjalizowany bot handlu Forex o wysokiej precyzji z ciągłym uczeniem RL, skupiający się na XAUUSD (Złoto) i NASDAQ.

**Kluczowe funkcje**:
- Hybrydowa architektura Python + Expert Advisor MQL5
- Skoncentrowana strategia: 1-2 specjalizowane strategie w porównaniu z 10-100+ w Portfolio Manager
- Ciągłe codzienne przeszkolenie RL
- Strategia hedgingu (jednoczesne pozycje long/short)
- Ścisłe limity ryzyka: progi spadku 4%-8%-12%, max strata dziennie 5%
- Maksymalnie 3 transakcje dziennie
- Kapitał demo $100k
- Oczekiwanie na test połączenia PostgreSQL

**Stack technologiczny**: MT5 API, Python, PostgreSQL, Stable-Baselines3, backtrader, ta (Technical Analysis)

**Polecenia programistyczne**:
```bash
cd janosik-ea
pip install -r requirements.txt   # Instaluj zależności
python config.py              # Sprawdź konfigurację
python core_database.py       # Inicjalizuj/testuj bazę danych
python core_mt5.py            # Testuj połączenie MT5
# Planowane: python scripts/train_rl_model.py, python scripts/backtest_strategies.py
```

**Baza danych**: PostgreSQL (7 planowanych tabel: market_data, strategies, trades, daily_stats, rl_training, positions, performance_metrics)

**Kluczowa różnica od Portfolio Manager**: Podejście specjalizowane z głębszą optymalizacją na strategię w stosunku do szerokiej dywersyfikacji

### 3. Coding Agent (Gotowy do produkcji)

**Lokalizacja**: `coding-agent/`

**Status**: Gotowy do produkcji

**Cel**: Autonomiczny asystent rozwoju AI do wsadowego generowania kodu, refaktoryzacji i automatyzacji przepływów pracy za pomocą orkiestracji LangGraph.

**Funkcje**:
- Przepływ Planowanie → Wykonanie → Weryfikacja (maszyna stanów LangGraph)
- Bezpieczne wykonanie CLI (na liście: npm, git, python, aider, ls, mkdir, itp.)
- Generowanie kodu wspieranego AI za pośrednictwem integracji Aider
- Automatyzacja refaktoryzacji wsadowej (implementacje wzorów, typy, itp.)
- Automatyzacja Git (commit, diff, śledzenie stanu)
- Tryb dry-run do bezpiecznego podglądu zadań
- Automatyczne podpowiedzi potwierdzenia dla bezpieczeństwa

**Stack technologiczny**: LangChain, LangGraph, Google Gemini (lub DeepSeek), Aider, Rich CLI

**Polecenia programistyczne**:
```bash
cd coding-agent
pip install -r requirements.txt   # Instaluj zależności

# Wykonanie zadań wsadowych
python agent.py --task "Twoim opis zadania"        # Pojedyncze zadanie
python agent.py --interactive                      # Tryb interaktywny
python agent.py --dry-run                          # Podgląd bez wykonania
python agent.py --no-confirm                       # Pomiń potwierdzenia
python setup.py                                    # Weryfikuj instalację
```

**Dostępne narzędzia**: shell_executor, aider_executor, git_status, git_commit, git_diff, read_file, list_directory, file_exists

## Struktura katalogów

```
/
├── portfolio-manager-pro/          # Platforma enterprise
│   ├── main.py                     # Orkiestrator (200+ linii)
│   ├── config.py                   # Konfiguracja (300+ linii)
│   ├── database.py                 # SQLAlchemy ORM (400+ linii)
│   ├── api_server.py               # REST API FastAPI
│   ├── dashboard.py                # Monitorowanie Dash
│   ├── backtester.py               # Testowanie historyczne
│   ├── rl_engine.py                # Trening RL (500+ linii)
│   ├── strategy_framework.py        # Bazowa strategia + implementacje
│   ├── risk_manager.py             # Kontrola ryzyka portfela
│   ├── mt5_connector.py            # Integracja MT5 (300+ linii)
│   ├── remote_mt5_scripts/         # Interakcja MT5 po stronie serwera
│   ├── requirements.txt
│   └── ARCHITECTURE.md             # Dokument projektowy 2000+ linii
│
├── janosik-ea/                     # Specjalizowany trader
│   ├── config.py                   # Parametry handlu
│   ├── core_database.py            # PostgreSQL ORM
│   ├── core_mt5.py                 # Integracja MT5
│   ├── requirements.txt
│   ├── PROJECT_STRUCTURE.md
│   └── PROGRESS_SUMMARY.md
│
├── coding-agent/                   # Agent autonomiczny
│   ├── agent.py                    # Przepływ LangGraph (300+ linii)
│   ├── config.py                   # Konfiguracja
│   ├── setup.py                    # Weryfikacja instalacji
│   ├── tools/
│   │   ├── shell_tool.py           # Bezpieczne wykonanie CLI
│   │   ├── aider_tool.py           # Generowanie kodu
│   │   ├── git_tool.py             # Kontrola wersji
│   │   └── filesystem_tool.py      # Operacje na plikach
│   ├── requirements.txt
│   └── README.md
│
├── package.json                    # Node.js (Claude Code)
├── .env                            # Główna konfiguracja środowiska
├── CLAUDE.md                       # Ten plik
├── DUAL_AGENT_WORKFLOW.md          # Przewodnik przepływu
├── start-dual-workflow.ps1         # Launcher podwójny
└── .claude/                        # Ustawienia Claude Code
```

## Popularne polecenia programistyczne

### Uruchomienie podwójnego przepływu
```powershell
.\start-dual-workflow.ps1    # Uruchamia Claude Code + Coding Agent w oddzielnych terminalach
```

### Interaktywny Claude Code
```bash
npx claude                   # Uruchom sesję programowania w parze
# Użyj do: Decyzji architekturalnych, przeglądu kodu, debugowania, nauki
```

### Portfolio Manager Pro
```bash
cd portfolio-manager-pro
pip install -r requirements.txt   # Instaluj zależności

# Handel na żywo
python main.py                    # Uruchom orkiestrator (zarządza wszystkimi strategiami)

# Monitorowanie i zarządzanie
python api_server.py              # REST API na porcie 8000
python dashboard.py               # Dashboard Dash w czasie rzeczywistym
python backtester.py              # Testuj strategie na danych historycznych
python rl_engine.py               # Trenuj modele RL

# Jakość kodu
pytest tests/ && black . && mypy . # Uruchom testy, formatowanie, sprawdzenie typów
```

### Janosik EA
```bash
cd janosik-ea
pip install -r requirements.txt   # Instaluj zależności

# Weryfikacja konfiguracji
python config.py                  # Sprawdź parametry handlu
python core_database.py           # Inicjalizuj/testuj PostgreSQL
python core_mt5.py                # Testuj połączenie MT5

# Kolejne fazy (jeszcze nie zaimplementowane)
# python scripts/train_rl_model.py
# python scripts/backtest_strategies.py
# python scripts/live_trading.py
```

### Coding Agent (Automatyzacja wsadowa)
```bash
cd coding-agent
pip install -r requirements.txt   # Instaluj zależności

# Wykonanie zadań wsadowych
python agent.py --task "Refaktoryzuj wszystkie komponenty do TypeScript"
python agent.py --task "Dodaj kompleksowe docstringi do wszystkich funkcji"
python agent.py --task "Wygeneruj testy jednostkowe dla math_utils.py"

# Tryb interaktywny (wpisz wiele zadań)
python agent.py --interactive

# Bezpieczny podgląd (bez wykonania)
python agent.py --task "..." --dry-run

# Pomiń podpowiedzi potwierdzenia (używaj ostrożnie)
python agent.py --task "..." --no-confirm

# Weryfikuj konfigurację
python setup.py
```

## Infrastruktura wspólna

### Baza danych PostgreSQL
- **Host**: 51.77.58.92
- **Port**: 1993 (niestandardowy)
- **Użytkownik**: pawwasfx
- **Baza danych**: bazadanych
- **Używane przez**: Portfolio Manager Pro, Janosik EA
- **Połączenie**: Pulane przez SQLAlchemy, dostęp SSH dla wdrażania zdalnego

### Integracja MetaTrader5
- **Portfolio Manager Pro**: Wsparcie lokalnego API MT5 + zdalne skrypty oparte na SSH
- **Janosik EA**: Lokalny API MT5 (hybrydowy Python + Expert Advisor MQL5)
- **Operacje zdalne**: `portfolio-manager-pro/remote_mt5_scripts/` dla wdrażania na VPS
  - `get_balance.py` - Kapitał konta/saldo
  - `get_candles.py` - Historyczne dane OHLCV
  - `get_positions.py` - Śledzenie otwartych pozycji
  - `place_order.py` - Wykonanie transakcji

## Konfiguracja i zmienne środowiskowe

### Zmienne środowiskowe
Każdy projekt używa plików `.env`. Skopiuj `.env.example` do `.env` i skonfiguruj:

**Projekty handlu** (Portfolio Manager Pro, Janosik EA):
```env
# Baza danych
DATABASE_URL=postgresql://pawwasfx:password@51.77.58.92:1993/bazadanych

# MT5 lokalnie
MT5_ACCOUNT=twój_numer_konta
MT5_PASSWORD=twoje_hasło
MT5_SERVER=MetaTrader5-Server

# Parametry handlu
INITIAL_CAPITAL=100000
MAX_DRAWDOWN_PCT=8
DAILY_LOSS_LIMIT=5000
```

**Coding Agent** (coding-agent/.env):
```env
# Backend LLM
GEMINI_API_KEY=twój_klucz  # Lub ustaw na DeepSeek
MODEL_NAME=gemini-1.5-flash-latest

# Ustawienia bezpieczeństwa
DRY_RUN_MODE=false
REQUIRE_CONFIRMATION=true

# Rejestrowanie
VERBOSE=true
LANGUAGE=pl
```

## Wzorce użytkowania

### Wzorzec 1: Interaktywny projekt z Claude Code
Używaj Claude Code do:
- Decyzji architektonicznych i planowania
- Przeglądu kodu i debugowania
- Złożonego rozwiązywania problemów
- Nauki i dokumentacji

```bash
npx claude
# Uruchom sesję interaktywną i omów swoje wymagania
```

### Wzorzec 2: Automatyzacja wsadowa z Coding Agent
Używaj Coding Agent do:
- Wsadowego generowania kodu za pomocą Aider
- Dużych refaktoryzacji (np. typy, implementacje wzorów)
- Powtarzalnych operacji na plikach
- Przepływów Git i zbiorczych commitów

```bash
python coding-agent/agent.py --task "Dodaj typy do wszystkich plików Python w portfolio-manager-pro/"
```

### Wzorzec 3: Wdrażanie systemu handlu
1. Opracuj strategię w Claude Code (planowanie interaktywne)
2. Wdrażaj z Coding Agent (wsadowe generowanie kodu)
3. Testuj z backtesterem Portfolio Manager (`python backtester.py`)
4. Wdrażaj do handlu na żywo z REST API (`python api_server.py`)
5. Monitoruj za pomocą dashboarda Dash (`python dashboard.py`)

### Wzorzec 4: Specjalizowany vs. Enterprise
- **Użyj Janosik EA** dla: Pojedyncza strategia o wysokiej precyzji, fokus XAUUSD/NASDAQ, ścisła kontrola spadku
- **Użyj Portfolio Manager Pro** dla: Zdywersyfikowanych strategii, głosowania ensemble, maksymalna automatyzacja, rozproszone wdrażanie

## Kluczowe szczegóły implementacji

### Bezpieczeństwo Coding Agent
- **Wykonanie CLI na liście**: npm, git, python, aider, ls, mkdir, itp.
- **Zablokowane destrukcyjne polecenia**: rm, del, format, dd, mkfs, itp.
- **Limity czasu**: 5 minut dla poleceń shell, 10 minut dla operacji Aider
- **Limity plików**: Maksymalnie czytanie 1MB pliku, aby zapobiec problemom pamięci
- **Podpowiedzi potwierdzenia**: Zatwierdzenie użytkownika wymagane, chyba że flaga `--no-confirm`

### Zarządzanie ryzykiem handlu
- **Portfolio Manager Pro**: Wielowarstwowe (poziom portfela, strategii, pozycji)
- **Janosik EA**: Ścisłe progi (poziomy spadku 4%-8%-12%, limit straty dziennie 5%, max 3 transakcje)
- **Oba systemy**: Monitorowanie w czasie rzeczywistym z dziennikami audytu dla zgodności

### Przepływ LangGraph (Coding Agent)
```
Węzeł planowania → Węzeł wykonania → Węzeł weryfikacji
   ↓                ↓                    ↓
Analizuj zadanie   Wykonaj narzędzia    Sprawdź wyniki
Utwórz plan        z filtrami bezpieczeństwa  Automatyczne odzyskanie
Rozłóż             Kontynuuj lub zakończ
```

## Ważne pliki i ich przeznaczenie

### Portfolio Manager Pro
- `main.py` - Centralny orkiestrator, uruchamia wszystkie strategie równolegle
- `strategy_framework.py` - Klasa BaseStrategy + implementacje RSI/MA/niestandardowe
- `risk_manager.py` - Kontrola ryzyka na poziomie portfela i wymiarowanie pozycji
- `rl_engine.py` - Trening PPO/DQN Stable-Baselines3
- `ARCHITECTURE.md` - Dokument projektowy 2000+ linii (przeczytaj pierwszy)

### Janosik EA
- `config.py` - Wszystkie parametry handlu (kapitał, spadek, limity ryzyka)
- `core_database.py` - PostgreSQL ORM ze schematami tabel
- `core_mt5.py` - Pobieranie danych MetaTrader5 i wykonanie zleceń
- `PROJECT_STRUCTURE.md` - Pełny przegląd architektury

### Coding Agent
- `agent.py` - Orkiestracja przepływu LangGraph
- `config.py` - Konfiguracja z ładowaniem zmiennych środowiskowych
- `tools/shell_tool.py` - Bezpieczne wykonanie poleceń z listą
- `tools/aider_tool.py` - Integracja z Aider do generowania kodu

## Odwołania do dokumentacji

- **Pełny przewodnik przepływu podwójnego**: `DUAL_AGENT_WORKFLOW.md`
- **Architektura Portfolio Manager**: `portfolio-manager-pro/ARCHITECTURE.md` (2000+ linii)
- **Wdrażanie handlu**: `README_START_HERE.txt` (przewodnik wdrażania)
- **Szczegóły Coding Agent**: `coding-agent/README.md`
- **Szybkie odniesienie**: `QUICK_REFERENCE.md`

## Rozwiązywanie problemów

**Błąd połączenia PostgreSQL**: Sprawdź `DATABASE_URL` w `.env` i zweryfikuj dostęp sieciowy do 51.77.58.92:1993

**Błąd połączenia MT5**: Upewnij się, że terminal MT5 jest uruchomiony (lokalnie) lub dostęp SSH skonfigurowany (zdalnie)

**Narzędzie Coding Agent zablokowane**: Przejrzyj listę w `coding-agent/config.py` lub dodaj polecenie, jeśli jest bezpieczne

**Model RL nie trenuje**: Sprawdź dzienniki w `portfolio-manager-pro/rl_engine.py` i zweryfikuj, czy tabela market_data PostgreSQL ma wystarczającą liczbę historycznych świeczników
