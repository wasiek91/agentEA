"""Narzędzie do wykonywania komend shell z funkcjami bezpieczeństwa."""
import subprocess
import shlex
from typing import Dict, Any
from langchain_core.tools import BaseTool
from rich.console import Console
from rich.panel import Panel
from config import Config

console = Console()


class ShellTool(BaseTool):
    """Narzędzie do bezpiecznego wykonywania komend shell."""

    name: str = "shell_executor"
    description: str = "Execute shell commands safely"

    def _run(self, command: str) -> str:
        """Wykonaj komendę shell z kontrolami bezpieczeństwa."""
        try:
            # Kontrola bezpieczeństwa: waliduj komendę
            if not self._is_command_safe(command):
                return "Error: Command blocked"

            # Pokaż komendę użytkownikowi
            console.print(Panel(
                f"[cyan]Komenda:[/cyan] {command}",
                title="Wykonywanie Shell",
                border_style="cyan"
            ))

            # Poproś o potwierdzenie jeśli włączone
            if Config.REQUIRE_CONFIRMATION and not Config.DRY_RUN_MODE:
                response = console.input("[yellow]Wykonać tę komendę? (t/n): [/yellow]")
                if response.lower() not in ['t', 'y', 'tak', 'yes']:
                    return "Wykonanie komendy anulowane przez użytkownika."

            # Tryb testowy
            if Config.DRY_RUN_MODE:
                return f"TRYB TESTOWY: Zostałaby wykonana komenda: {command}"

            # Wykonaj komendę
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300  # Timeout 5 minut
            )

            output = result.stdout + result.stderr

            if result.returncode != 0:
                return f"Error {result.returncode}: {output}"

            return output if output else ""

        except subprocess.TimeoutExpired:
            return "Error: Timeout (5 min)"
        except Exception as e:
            return f"Error: {str(e)}"

    def _is_command_safe(self, command: str) -> bool:
        """Sprawdź czy komenda przechodzi filtry bezpieczeństwa."""
        # Sprawdź czarną listę
        for blocked in Config.SHELL_BLACKLIST:
            if blocked.lower() in command.lower():
                console.print(f"[red]Zablokowano:[/red] Komenda zawiera zakazany term: {blocked}")
                return False

        # Sprawdź białą listę (pierwsze słowo powinno być na białej liście)
        try:
            # Parsuj komendę aby uzyskać pierwsze słowo
            parts = shlex.split(command)
            if not parts:
                return False

            base_command = parts[0].split('/')[-1].split('\\')[-1]  # Obsłuż ścieżki

            # Sprawdź czy podstawowa komenda jest na białej liście
            is_whitelisted = any(
                base_command.lower().startswith(allowed.lower())
                for allowed in Config.SHELL_WHITELIST
            )

            if not is_whitelisted:
                console.print(
                    f"[red]Zablokowano:[/red] Komenda '{base_command}' nie jest na białej liście. "
                    f"Dozwolone: {', '.join(Config.SHELL_WHITELIST)}"
                )
                return False

        except Exception as e:
            console.print(f"[red]Błąd parsowania komendy:[/red] {e}")
            return False

        return True

    async def _arun(self, command: str) -> str:
        """Wersja async (nie zaimplementowana)."""
        raise NotImplementedError("ShellTool nie wspiera wykonywania asynchronicznego.")
