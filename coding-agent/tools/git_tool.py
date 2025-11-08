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
    description: str = "Check git repository status"

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
                return f"Error: {result.stderr}"

            return result.stdout

        except FileNotFoundError:
            return "Error: Git not installed"
        except Exception as e:
            return f"Error: {str(e)}"

    async def _arun(self, query: str = "") -> str:
        """Wersja async (nie zaimplementowana)."""
        raise NotImplementedError("GitStatusTool nie wspiera wykonywania asynchronicznego.")


class GitCommitTool(BaseTool):
    """Narzędzie do commitowania zmian do repozytorium git."""

    name: str = "git_commit"
    description: str = "Commit changes to git"

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
                return "Error: No commit message"

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
                return f"Error: {add_result.stderr}"

            # Commit
            commit_result = subprocess.run(
                ["git", "commit", "-m", message],
                capture_output=True,
                text=True,
                timeout=30
            )

            if commit_result.returncode != 0:
                if "nothing to commit" in commit_result.stdout.lower():
                    return "Nothing to commit"
                return f"Error: {commit_result.stderr}"

            return commit_result.stdout

        except Exception as e:
            return f"Error: {str(e)}"

    async def _arun(self, query: str) -> str:
        """Wersja async (nie zaimplementowana)."""
        raise NotImplementedError("GitCommitTool nie wspiera wykonywania asynchronicznego.")


class GitDiffTool(BaseTool):
    """Narzędzie do przeglądania różnic w git."""

    name: str = "git_diff"
    description: str = "View git changes/diff"

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
                return f"Error: {result.stderr}"

            if not result.stdout:
                return "No changes"

            return result.stdout

        except Exception as e:
            return f"Error: {str(e)}"

    async def _arun(self, query: str = "") -> str:
        """Wersja async (nie zaimplementowana)."""
        raise NotImplementedError("GitDiffTool nie wspiera wykonywania asynchronicznego.")
