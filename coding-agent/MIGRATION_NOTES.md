# Notatki Migracji do LangChain 0.3.x

## Podsumowanie Zmian

Projekt został zaktualizowany do stabilnych wersji bibliotek:
- `langchain==0.3.18` (poprzednio 0.1.0)
- `langchain-anthropic==0.3.5` (poprzednio 0.1.1)
- `langgraph==0.2.64` (poprzednio 0.0.20)
- `langchain-core==0.3.79` (auto-zainstalowane)

## Główne Zmiany w Kodzie

### 1. Zaktualizowane Importy

#### agent.py
- `from langchain.prompts` → `from langchain_core.prompts`
- `from langchain.agents import create_tool_calling_agent` → usunięte (zastąpione nowym API)

#### Wszystkie pliki narzędzi (tools/*.py)
- `from langchain.tools import BaseTool` → `from langchain_core.tools import BaseTool`

### 2. API Tworzenia Agenta (bez zmian)

API dla langchain 0.3.x pozostaje takie samo jak w 0.1.0:
```python
self.agent = create_tool_calling_agent(self.llm, self.tools, self.prompt)
self.agent_executor = AgentExecutor(agent=self.agent, tools=self.tools, ...)
```

**Uwaga:** Wersja langchain 1.0+ ma całkowicie zmienione API i nie jest jeszcze stabilna. Zalecamy pozostanie przy wersji 0.3.x do czasu ustabilizowania się API w wersji 1.0+.

### 3. Zmiany w Parametrach

- Parametr wejściowy agenta zmieniony z `"task"` na `"input"` w promptach
- Usunięto bezpośrednie przekazywanie `"agent_scratchpad": []` - teraz jest obsługiwane przez format_to_openai_function_messages

## Instalacja Zaktualizowanych Zależności

```bash
pip install -r requirements.txt --upgrade
```

lub:

```bash
pip install "langchain>=0.3.0" "langchain-anthropic>=1.0.0" "langgraph>=1.0.0"
```

## Testowanie

Przed pełnym wdrożeniem zaleca się przetestowanie podstawowych funkcjonalności:

1. **Test podstawowy:**
```bash
python agent.py --task "Sprawdź status git" --dry-run
```

2. **Test w trybie interaktywnym:**
```bash
python agent.py --interactive
```

## Breaking Changes

1. **Moduły przeniesione do langchain_core** - podstawowe klasy jak `BaseTool`, `ChatPromptTemplate`, `MessagesPlaceholder` są teraz w `langchain_core` zamiast `langchain`
2. **Usunięcie langchain-community** - stara wersja została usunięta z powodu niekompatybilności
3. **Usunięcie langgraph-prebuilt 1.0+** - wymagała langchain-core 1.0+ który nie jest jeszcze stabilny

## Kompatybilność

- Python: >=3.9 (zalecane 3.10+)
- Wszystkie narzędzia (ShellTool, AiderTool, GitTool, FileSystemTool) są kompatybilne
- LangGraph workflow pozostaje bez zmian

## Dlaczego nie langchain 1.0+?

Podczas migracji napotkaliśmy problemy z langchain 1.0+:
- Całkowicie zmieniona struktura modułów - `AgentExecutor` nie istnieje w tym samym miejscu
- Brak stabilnego API dla agentów
- Konflikty zależności z aider-chat i innymi narzędziami
- Dokumentacja jeszcze nieaktualna

**Zalecenie:** Pozostań przy langchain 0.3.x do czasu gdy 1.0+ będzie stabilne i dobrze udokumentowane.

## Dodatkowe Uwagi

- ✅ Wszystkie testy składniowe przeszły pomyślnie
- ✅ Import agent.py działa poprawnie
- ✅ API Anthropic Claude pozostaje bez zmian
- ✅ Konfiguracja w `config.py` nie wymaga zmian
- ✅ Wszystkie funkcje bezpieczeństwa (białe/czarne listy komend) działają bez zmian

## Zainstalowane Wersje

Po migracji zainstalowane są następujące wersje:
- langchain: 0.3.18
- langchain-core: 0.3.79
- langchain-anthropic: 0.3.5
- langgraph: 0.2.64
- langgraph-checkpoint: 2.1.2
- python-dotenv: 1.1.1
- rich: 14.1.0
