# DeepSeek CLI - Instrukcja Konfiguracji

## Status Instalacji: ✅ ZAINSTALOWANE

DeepSeek CLI Pro zostało pomyślnie zainstalowane w osobnym środowisku Python.

---

## 📍 Lokalizacja

```
C:\Users\HP\OneDrive\Pulpit\Cloude\coding-agent\deepseek-env\
```

Executable:
```
C:\Users\HP\OneDrive\Pulpit\Cloude\coding-agent\deepseek-env\Scripts\deepseek.exe
```

---

## 🔑 Konfiguracja Klucza API

### Opcja 1: Zmienna środowiskowa (Tymczasowa - dla bieżącej sesji)

W PowerShell:
```powershell
$env:DEEPSEEK_API_KEY="TWÓJ_KLUCZ_API_TUTAJ"
```

### Opcja 2: Dodanie do profilu PowerShell (Stała konfiguracja)

1. Otwórz profil PowerShell:
```powershell
notepad $PROFILE
```

2. Dodaj na końcu pliku:
```powershell
# DeepSeek API Key
$env:DEEPSEEK_API_KEY="TWÓJ_KLUCZ_API_TUTAJ"
```

3. Zapisz i zamknij Notepad

4. Przeładuj profil:
```powershell
. $PROFILE
```

### Opcja 3: Plik .env w folderze projektu

Utwórz plik `.env` w folderze `coding-agent`:
```bash
DEEPSEEK_API_KEY=TWÓJ_KLUCZ_API_TUTAJ
```

---

## 🚀 Użycie DeepSeek CLI

### Bezpośrednie wywołanie (pełna ścieżka):
```powershell
C:\Users\HP\OneDrive\Pulpit\Cloude\coding-agent\deepseek-env\Scripts\deepseek.exe -q "Twoje pytanie"
```

### Z aktywowanym środowiskiem:
```powershell
# Aktywuj środowisko
cd C:\Users\HP\OneDrive\Pulpit\Cloude\coding-agent
.\deepseek-env\Scripts\activate

# Użyj deepseek
deepseek -q "Twoje pytanie"
```

---

## ⚡ Konfiguracja Aliasu w PowerShell (Zalecane)

### Krok 1: Dodaj alias do profilu PowerShell

```powershell
notepad $PROFILE
```

Dodaj na końcu:
```powershell
# DeepSeek CLI Alias
Set-Alias deepseek "C:\Users\HP\OneDrive\Pulpit\Cloude\coding-agent\deepseek-env\Scripts\deepseek.exe"
```

### Krok 2: Przeładuj profil

```powershell
. $PROFILE
```

### Krok 3: Testuj

```powershell
deepseek -q "Przetestuj połączenie"
```

---

## 📋 Dostępne Komendy

### Podstawowe użycie:
```powershell
# Zadaj pytanie
deepseek -q "Jak działa rekursja w Pythonie?"

# Tryb interaktywny
deepseek

# Pomoc
deepseek --help
```

### Zaawansowane opcje (jeśli obsługiwane):
```powershell
# Określ model
deepseek -q "Pytanie" --model deepseek-coder

# Długość odpowiedzi
deepseek -q "Pytanie" --max-tokens 1000

# Temperatura (kreatywność)
deepseek -q "Pytanie" --temperature 0.7
```

---

## 🔍 Weryfikacja Instalacji

Sprawdź wersję:
```powershell
C:\Users\HP\OneDrive\Pulpit\Cloude\coding-agent\deepseek-env\Scripts\deepseek.exe --version
```

Sprawdź zainstalowane pakiety:
```powershell
C:\Users\HP\OneDrive\Pulpit\Cloude\coding-agent\deepseek-env\Scripts\pip.exe list | Select-String deepseek
```

Wynik powinien pokazać:
```
deepseek-cli-pro    0.2.1
```

---

## 🌐 Alternatywa: Lokalny Model (bez API)

Jeśli chcesz używać DeepSeek lokalnie bez klucza API:

### 1. Zainstaluj Ollama
Pobierz ze strony: https://ollama.com/download

### 2. Zainstaluj model DeepSeek
```powershell
ollama pull deepseek-coder:6.7b
```

### 3. Uruchom model
```powershell
ollama run deepseek-coder:6.7b
```

---

## ⚠️ Rozwiązywanie Problemów

### Problem: "deepseek nie jest rozpoznawany jako polecenie"

**Rozwiązanie:**
- Użyj pełnej ścieżki do executable
- Lub aktywuj środowisko wirtualne
- Lub skonfiguruj alias w PowerShell (patrz sekcja wyżej)

### Problem: "API key not found"

**Rozwiązanie:**
1. Upewnij się, że ustawiłeś zmienną środowiskową `DEEPSEEK_API_KEY`
2. Sprawdź: `echo $env:DEEPSEEK_API_KEY`
3. Jeśli puste, ustaw ponownie zgodnie z instrukcją powyżej

### Problem: Konflikty z innymi agentami

**Rozwiązanie:**
- DeepSeek jest w osobnym środowisku wirtualnym (`deepseek-env`)
- Nie wpływa na inne agenty ani ich środowiska
- Każdy agent może działać niezależnie

---

## 📦 Zainstalowane Pakiety

```
deepseek-cli-pro: 0.2.1
openai: 2.7.1
rich: 14.2.0
click: 8.3.0
httpx: 0.28.1
pydantic: 2.12.4
```

---

## 🆘 Wsparcie

Dokumentacja DeepSeek:
- https://platform.deepseek.com/docs

API Documentation:
- https://platform.deepseek.com/api-docs

---

## ✅ Następne Kroki

1. **Zdobądź klucz API:** https://platform.deepseek.com/api_keys
2. **Ustaw zmienną środowiskową** zgodnie z instrukcją powyżej
3. **Skonfiguruj alias w PowerShell** dla wygody
4. **Przetestuj połączenie:** `deepseek -q "Test połączenia"`

---

## 📝 Historia Instalacji

- **Data instalacji:** 2025
- **Wersja Python:** 3.12
- **Lokalizacja:** C:\Users\HP\OneDrive\Pulpit\Cloude\coding-agent\deepseek-env
- **Status:** ✅ Gotowe do użycia (wymaga klucza API)
