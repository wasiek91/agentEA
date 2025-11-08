"""Narzędzie Aider do edycji kodu wspomaganej AI."""
import subprocess
from typing import Dict, Any
from langchain_core.tools import BaseTool
from rich.console import Console
from rich.panel import Panel
from config import Config

console = Console()


class AiderTool(BaseTool):
    """Narzędzie do uruchamiania komend Aider do edycji kodu."""

    name: str = "aider_executor"
    description: str = "Execute Aider for AI code editing"

    def _run(self, query: str) -> str:
        """Wykonaj komendę Aider z podanym promptem."""
        try:
            import json

            # Parsuj input
            try:
                params = json.loads(query)
                prompt = params.get("prompt", "")
                files = params.get("files", [])
            except json.JSONDecodeError:
                # Jeśli nie JSON, traktuj jako prosty prompt
                prompt = query
                files = []

            if not prompt:
                return "Error: No prompt"

            # Zbuduj komendę Aider
            cmd_parts = ["aider"]

            # Dodaj pliki jeśli podane
            if files:
                cmd_parts.extend(files)

            # Dodaj flagę message
            cmd_parts.extend(["--message", prompt])

            # Dodaj flagę yes do auto-potwierdzenia
            cmd_parts.append("--yes")

            command = " ".join(cmd_parts)

            # Wyświetl użytkownikowi
            console.print(Panel(
                f"[cyan]Prompt:[/cyan] {prompt}\n"
                f"[cyan]Pliki:[/cyan] {', '.join(files) if files else 'Auto-wykrywanie'}\n"
                f"[cyan]Komenda:[/cyan] {command}",
                title="Wykonywanie Aider",
                border_style="green"
            ))

            # Poproś o potwierdzenie
            if Config.REQUIRE_CONFIRMATION and not Config.DRY_RUN_MODE:
                response = console.input("[yellow]Wykonać komendę Aider? (t/n): [/yellow]")
                if response.lower() not in ['t', 'y', 'tak', 'yes']:
                    return "Cancelled"

            # Tryb testowy
            if Config.DRY_RUN_MODE:
                return "Dry-run: would execute"

            # Wykonaj Aider
            result = subprocess.run(
                cmd_parts,
                capture_output=True,
                text=True,
                timeout=600
            )

            output = result.stdout + result.stderr

            if result.returncode != 0:
                return f"Error {result.returncode}: {output}"

            return output if output else ""

        except subprocess.TimeoutExpired:
            return "Error: Timeout (10 min)"
        except FileNotFoundError:
            return "Error: Aider not found"
        except Exception as e:
            return f"Error: {str(e)}"

    async def _arun(self, query: str) -> str:
        """Wersja async (nie zaimplementowana)."""
        raise NotImplementedError("AiderTool nie wspiera wykonywania asynchronicznego.")


class AiderStatusTool(BaseTool):
    """Narzędzie do sprawdzania czy Aider jest zainstalowany i działa."""

    name: str = "aider_status"
    description: str = "Check if Aider is installed"

    def _run(self, query: str = "") -> str:
        """Sprawdź status instalacji Aider."""
        try:
            result = subprocess.run(
                ["aider", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                version = result.stdout.strip()
                return f"Installed: {version}"
            else:
                return "Error: Check failed"

        except FileNotFoundError:
            return "Not installed"
        except Exception as e:
            return f"Error: {str(e)}"

    async def _arun(self, query: str = "") -> str:
        """Wersja async (nie zaimplementowana)."""
        raise NotImplementedError("AiderStatusTool nie wspiera wykonywania asynchronicznego.")
