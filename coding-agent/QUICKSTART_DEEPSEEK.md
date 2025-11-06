# DeepSeek CLI - Quick Start Guide

## ✅ Status Instalacji: ZAKOŃCZONE

DeepSeek CLI Pro został pomyślnie zainstalowany i jest gotowy do użycia!

---

## 🚀 Szybki Start (3 kroki)

### Krok 1: Zdobądź klucz API
Odwiedź: https://platform.deepseek.com/api_keys
Zarejestruj się i skopiuj swój klucz API.

### Krok 2: Skonfiguruj środowisko
Uruchom w PowerShell (w folderze coding-agent):
```powershell
.\setup-deepseek-profile.ps1
```
Postępuj zgodnie z instrukcjami i wklej swój klucz API.

### Krok 3: Przetestuj
```powershell
# Przeładuj profil PowerShell
. $PROFILE

# Testuj DeepSeek
deepseek chat
```

---

## 📍 Lokalizacja Instalacji

```
Folder główny:
C:\Users\HP\OneDrive\Pulpit\Cloude\coding-agent\

Środowisko wirtualne:
C:\Users\HP\OneDrive\Pulpit\Cloude\coding-agent\deepseek-env\

Executable:
C:\Users\HP\OneDrive\Pulpit\Cloude\coding-agent\deepseek-env\Scripts\deepseek.exe
```

---

## 💡 Podstawowe Użycie

### Dostępne Komendy:

```powershell
# Tryb interaktywny (chat)
deepseek chat

# Wygeneruj odpowiedź na prompt
deepseek generate "Napisz funkcję sortującą w Pythonie"

# Lista dostępnych modeli
deepseek models

# Konfiguracja API
deepseek configure

# Pomoc
deepseek --help
```

### Przykłady:

```powershell
# Zadaj szybkie pytanie
deepseek generate "Wyjaśnij co to jest rekursja"

# Tryb interaktywny dla dłuższej rozmowy
deepseek chat

# Generowanie kodu
deepseek generate "Stwórz REST API w Flask z 3 endpointami"
```

---

## 🔧 Konfiguracja Ręczna

Jeśli nie chcesz używać automatycznego skryptu:

### Opcja A: Zmienna środowiskowa (Tymczasowa)
```powershell
$env:DEEPSEEK_API_KEY="twój_klucz_api_tutaj"
```

### Opcja B: Profil PowerShell (Stała)
1. Otwórz profil: `notepad $PROFILE`
2. Dodaj na końcu:
```powershell
$env:DEEPSEEK_API_KEY="twój_klucz_api_tutaj"
Set-Alias deepseek "C:\Users\HP\OneDrive\Pulpit\Cloude\coding-agent\deepseek-env\Scripts\deepseek.exe"
```
3. Zapisz i zamknij
4. Przeładuj: `. $PROFILE`

### Opcja C: Plik .env
Utwórz plik `.env` w folderze coding-agent:
```bash
DEEPSEEK_API_KEY=twój_klucz_api_tutaj
```

---

## 🧪 Testowanie Instalacji

### Test 1: Prosty test instalacji
```powershell
.\test-deepseek-simple.ps1
```

### Test 2: Sprawdź wersję
```powershell
C:\Users\HP\OneDrive\Pulpit\Cloude\coding-agent\deepseek-env\Scripts\deepseek.exe --version
```

### Test 3: Sprawdź pomoc
```powershell
deepseek --help
```

---

## 📦 Zainstalowane Komponenty

```
deepseek-cli-pro: 0.2.1
openai: 2.7.1
rich: 14.2.0
click: 8.3.0
markdown: 3.10
httpx: 0.28.1
pydantic: 2.12.4
```

---

## ⚠️ Rozwiązywanie Problemów

### Problem: "deepseek nie jest rozpoznawany"
**Rozwiązanie:**
- Użyj pełnej ścieżki: `C:\Users\HP\OneDrive\Pulpit\Cloude\coding-agent\deepseek-env\Scripts\deepseek.exe`
- Lub uruchom skrypt konfiguracyjny: `.\setup-deepseek-profile.ps1`

### Problem: "ModuleNotFoundError: No module named 'markdown'"
**Rozwiązanie:**
```powershell
C:\Users\HP\OneDrive\Pulpit\Cloude\coding-agent\deepseek-env\Scripts\pip.exe install markdown
```

### Problem: "API key not found"
**Rozwiązanie:**
1. Sprawdź czy zmienna jest ustawiona: `echo $env:DEEPSEEK_API_KEY`
2. Jeśli pusta, ustaw: `$env:DEEPSEEK_API_KEY="twój_klucz"`
3. Lub uruchom: `.\setup-deepseek-profile.ps1`

### Problem: Konflikty z innymi agentami
**Rozwiązanie:**
- DeepSeek jest w osobnym środowisku wirtualnym
- Nie ma konfliktów z innymi agentami (Claude, Anthropic, itp.)
- Każdy agent działa niezależnie

---

## 📚 Przydatne Pliki

```
README_DEEPSEEK.md          - Pełna dokumentacja
QUICKSTART_DEEPSEEK.md      - Ten plik (szybki start)
setup-deepseek-profile.ps1  - Automatyczna konfiguracja profilu
test-deepseek-simple.ps1    - Test instalacji
.env.deepseek.example       - Przykładowy plik .env
```

---

## 🔗 Linki

- **API Keys:** https://platform.deepseek.com/api_keys
- **Dokumentacja:** https://platform.deepseek.com/docs
- **API Docs:** https://platform.deepseek.com/api-docs
- **DeepSeek Website:** https://www.deepseek.com

---

## 🎯 Następne Kroki

1. ✅ Instalacja zakończona
2. ⏭️ Zdobądź klucz API z https://platform.deepseek.com/api_keys
3. ⏭️ Uruchom `.\setup-deepseek-profile.ps1`
4. ⏭️ Wklej klucz API do profilu PowerShell
5. ⏭️ Przetestuj: `deepseek chat`

---

## 🆘 Potrzebujesz pomocy?

Sprawdź pełną dokumentację w pliku: **README_DEEPSEEK.md**

---

*Instalacja wykonana automatycznie przez AI Coding Agent*
