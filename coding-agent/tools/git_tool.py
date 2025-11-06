"""Narzędzie operacji Git do kontroli wersji."""
import subprocess
from typing import Dict, Any
from langchain_core.tools import BaseTool
from rich.console import Console
from rich.panel import Panel
from config import Config

console = Console()


class GitStatusTool(BaseTool):
    """Narzędzie do sprawdzania statusu repozytorium git."""

    name: str = "git_status"
    description: str = """Sprawdź status repozytorium git.
    Pokazuje zmodyfikowane pliki, staged zmiany i aktualną gałąź.
    Nie wymaga inputu."""

    def _run(self, query: str = "") -> str:
        """Pobierz status git."""
        try:
            result = subprocess.run(
                ["git", "status"],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode != 0:
                return f"Git status nie powiódł się: {result.stderr}"

            return result.stdout

        except FileNotFoundError:
            return "BŁĄD: Git nie jest zainstalowany lub nie znajduje się w PATH."
        except Exception as e:
            return f"BŁĄD sprawdzania statusu git: {str(e)}"

    async def _arun(self, query: str = "") -> str:
        """Wersja async (nie zaimplementowana)."""
        raise NotImplementedError("GitStatusTool nie wspiera wykonywania asynchronicznego.")


class GitCommitTool(BaseTool):
    """Narzędzie do commitowania zmian do repozytorium git."""

    name: str = "git_commit"
    description: str = """Commituj zmiany do repozytorium git.
    Input powinien być stringiem JSON z kluczami 'message' i opcjonalnie 'files'.
    Jeśli files nie podano, scommituje wszystkie zmiany (git add -A).
    Przykład: '{"message": "Dodaj implementację aplikacji todo", "files": ["app.py", "test.py"]}'
    Lub: '{"message": "Commit początkowy"}'"""

    def _run(self, query: str) -> str:
        """Commituj zmiany do git."""
        try:
            import json

            # Parsuj input
            try:
                params = json.loads(query)
                message = params.get("message", "")
                files = params.get("files", [])
            except json.JSONDecodeError:
                # Jeśli nie JSON, traktuj jako wiadomość commita
                message = query
                files = []

            if not message:
                return "BŁĄD: Nie podano wiadomości commita."

            # Pokaż plan commita
            console.print(Panel(
                f"[cyan]Wiadomość Commita:[/cyan] {message}\n"
                f"[cyan]Pliki:[/cyan] {', '.join(files) if files else 'Wszystkie zmiany'}",
                title="Git Commit",
                border_style="green"
            ))

            # Poproś o potwierdzenie
            if Config.REQUIRE_CONFIRMATION and not Config.DRY_RUN_MODE:
                response = console.input("[yellow]Commitować te zmiany? (t/n): [/yellow]")
                if response.lower() not in ['t', 'y', 'tak', 'yes']:
                    return "Commit anulowany przez użytkownika."

            # Tryb testowy
            if Config.DRY_RUN_MODE:
                return f"TRYB TESTOWY: Zostałby wykonany commit z wiadomością: {message}"

            # Dodaj pliki
            if files:
                add_result = subprocess.run(
                    ["git", "add"] + files,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
            else:
                add_result = subprocess.run(
                    ["git", "add", "-A"],
                    capture_output=True,
                    text=True,
                    timeout=30
                )

            if add_result.returncode != 0:
                return f"Git add nie powiódł się: {add_result.stderr}"

            # Commit
            commit_result = subprocess.run(
                ["git", "commit", "-m", message],
                capture_output=True,
                text=True,
                timeout=30
            )

            if commit_result.returncode != 0:
                # Sprawdź czy to dlatego że nie ma nic do commitowania
                if "nothing to commit" in commit_result.stdout.lower():
                    return "Nie ma nic do commitowania - drzewo robocze czyste."
                return f"Git commit nie powiódł się: {commit_result.stderr}"

            return f"Pomyślnie scommitowano:\n{commit_result.stdout}"

        except Exception as e:
            return f"BŁĄD commitowania do git: {str(e)}"

    async def _arun(self, query: str) -> str:
        """Wersja async (nie zaimplementowana)."""
        raise NotImplementedError("GitCommitTool nie wspiera wykonywania asynchronicznego.")


class GitDiffTool(BaseTool):
    """Narzędzie do przeglądania różnic w git."""

    name: str = "git_diff"
    description: str = """Zobacz zmiany w repozytorium git.
    Pokazuje różnice między katalogiem roboczym a ostatnim commitem.
    Input może być pusty dla wszystkich zmian, lub podaj ścieżkę pliku.
    Przykład: 'app.py' lub '' dla wszystkich plików."""

    def _run(self, query: str = "") -> str:
        """Pobierz git diff."""
        try:
            cmd = ["git", "diff"]
            if query.strip():
                cmd.append(query.strip())

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode != 0:
                return f"Git diff nie powiódł się: {result.stderr}"

            if not result.stdout:
                return "Nie wykryto żadnych zmian."

            return result.stdout

        except Exception as e:
            return f"BŁĄD pobierania git diff: {str(e)}"

    async def _arun(self, query: str = "") -> str:
        """Wersja async (nie zaimplementowana)."""
        raise NotImplementedError("GitDiffTool nie wspiera wykonywania asynchronicznego.")
