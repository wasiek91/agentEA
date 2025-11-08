"""Główny AI Coding Agent z workflow LangGraph."""
import sys
import argparse
from typing import TypedDict, Annotated, Sequence
import operator
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langgraph.graph import StateGraph, END
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn

from config import Config
from tools import (
    ShellTool,
    AiderTool,
    AiderStatusTool,
    GitStatusTool,
    GitCommitTool,
    GitDiffTool,
    ReadFileTool,
    ListDirectoryTool,
    FileExistsTool,
)

console = Console()


# Definicja stanu dla grafu
class AgentState(TypedDict):
    """Stan dla workflow agenta."""
    task: str
    plan: str
    messages: Annotated[Sequence[str], operator.add]
    current_step: int
    max_steps: int
    completed: bool
    error: str


class CodingAgent:
    """AI Coding Agent z workflow LangGraph."""

    def __init__(self):
        """Inicjalizacja coding agenta."""
        # Walidacja konfiguracji
        Config.validate()

        # Inicjalizacja LLM
        self.llm = ChatGoogleGenerativeAI(
            model=Config.MODEL_NAME,
            google_api_key=Config.GEMINI_API_KEY,
            temperature=0,
            convert_system_message_to_human=True
        )

        # Inicjalizacja narzędzi
        self.tools = [
            ShellTool(),
            AiderTool(),
            AiderStatusTool(),
            GitStatusTool(),
            GitCommitTool(),
            GitDiffTool(),
            ReadFileTool(),
            ListDirectoryTool(),
            FileExistsTool(),
        ]

        # Utworzenie promptu
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """Expert AI coding assistant. Available tools: shell_executor, aider_executor, aider_status, git_status, git_commit, git_diff, read_file, list_directory, file_exists.

Guidelines: Check files exist, verify outputs, use git, test code, avoid destructive ops.
Current directory: {cwd}
Respond in Polish."""),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        # Utworzenie agenta dla langchain 0.3.x
        self.agent = create_tool_calling_agent(self.llm, self.tools, self.prompt)
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=Config.VERBOSE,
            max_iterations=Config.MAX_ITERATIONS,
            handle_parsing_errors=True
        )

        # Budowa grafu workflow
        self.workflow = self._build_workflow()

    def _build_workflow(self) -> StateGraph:
        """Budowa workflow LangGraph."""
        workflow = StateGraph(AgentState)

        # Dodanie nodów
        workflow.add_node("planning", self._planning_node)
        workflow.add_node("execution", self._execution_node)
        workflow.add_node("verification", self._verification_node)

        # Dodanie krawędzi
        workflow.set_entry_point("planning")
        workflow.add_edge("planning", "execution")
        workflow.add_edge("execution", "verification")

        # Dodanie warunkowej krawędzi z verification
        workflow.add_conditional_edges(
            "verification",
            self._should_continue,
            {
                "continue": "execution",
                "end": END
            }
        )

        return workflow.compile()

    def _planning_node(self, state: AgentState) -> AgentState:
        """Node planowania: Analizuj zadanie i twórz plan."""
        console.print(Panel(
            "[bold cyan]Faza Planowania[/bold cyan]\n"
            f"Zadanie: {state['task']}",
            border_style="cyan"
        ))

        # Użyj LLM do utworzenia planu
        planning_prompt = f"""Plan for: {state['task']}

Numbered steps:
1. Files to create/modify
2. Commands to run
3. Success criteria

Respond in Polish."""

        response = self.llm.invoke(planning_prompt)
        plan = response.content

        console.print(Panel(
            Markdown(plan),
            title="Plan",
            border_style="green"
        ))

        state["plan"] = plan
        state["messages"] = [f"Utworzono plan:\n{plan}"]
        state["current_step"] = 0

        return state

    def _execution_node(self, state: AgentState) -> AgentState:
        """Node wykonawczy: Wykonaj plan używając narzędzi."""
        console.print(Panel(
            f"[bold yellow]Faza Wykonawcza[/bold yellow]\n"
            f"Krok {state['current_step'] + 1} z {state['max_steps']}",
            border_style="yellow"
        ))

        try:
            # Pobierz aktualny katalog roboczy
            import os
            cwd = os.getcwd()

            # Wykonaj używając agenta
            result = self.agent_executor.invoke({
                "input": state["task"],
                "cwd": cwd
            })

            output = result.get("output", "Brak outputu")

            console.print(Panel(
                output,
                title="Wynik Wykonania",
                border_style="green"
            ))

            state["messages"] = [f"Krok wykonania {state['current_step'] + 1}: {output}"]
            state["current_step"] += 1

        except Exception as e:
            error_msg = f"Błąd podczas wykonywania: {str(e)}"
            console.print(f"[red]{error_msg}[/red]")
            state["error"] = error_msg
            state["completed"] = True

        return state

    def _verification_node(self, state: AgentState) -> AgentState:
        """Node weryfikacji: Zweryfikuj wyniki wykonania."""
        if state.get("error"):
            state["completed"] = True
            console.print("[red]Error - task failed[/red]")
        elif state["current_step"] >= state["max_steps"]:
            state["completed"] = True
            console.print("[green]Done - max steps reached[/green]")
        else:
            console.print("[yellow]Continuing...[/yellow]")

        return state

    def _should_continue(self, state: AgentState) -> str:
        """Zdecyduj czy kontynuować czy zakończyć."""
        if state.get("completed", False):
            return "end"
        return "continue"

    def run(self, task: str):
        """Uruchom agenta z danym zadaniem."""
        console.print(Panel(
            f"[bold magenta]AI Coding Agent Uruchomiony[/bold magenta]\n\n"
            f"Zadanie: {task}\n"
            f"Model: {Config.MODEL_NAME}\n"
            f"Tryb Testowy: {Config.DRY_RUN_MODE}\n"
            f"Potwierdzenia: {'Wyłączone' if not Config.REQUIRE_CONFIRMATION else 'Włączone'}",
            border_style="magenta"
        ))

        # Inicjalizacja stanu
        initial_state = AgentState(
            task=task,
            plan="",
            messages=[],
            current_step=0,
            max_steps=5,  # Limit iteracji
            completed=False,
            error=""
        )

        try:
            # Uruchom workflow
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task_progress = progress.add_task("Uruchamianie agenta...", total=None)

                final_state = self.workflow.invoke(initial_state)

                progress.update(task_progress, completed=True)

            # Wyświetl wyniki
            console.print(Panel(
                "[bold green]Zadanie Ukończone![/bold green]",
                border_style="green"
            ))

            if final_state.get("error"):
                console.print(f"[red]Napotkano błędy: {final_state['error']}[/red]")

        except KeyboardInterrupt:
            console.print("\n[yellow]Agent przerwany przez użytkownika.[/yellow]")
        except Exception as e:
            console.print(f"[red]Błąd agenta: {str(e)}[/red]")


def interactive_mode():
    """Uruchom agenta w trybie interaktywnym."""
    console.print(Panel(
        "[bold magenta]AI Coding Agent - Tryb Interaktywny[/bold magenta]\n"
        "Wpisz 'exit' lub 'quit' aby zakończyć.\n"
        "Wpisz 'help' aby zobaczyć dostępne komendy.",
        border_style="magenta"
    ))

    agent = CodingAgent()

    while True:
        try:
            task = console.input("\n[cyan]Podaj zadanie:[/cyan] ")

            if task.lower() in ['exit', 'quit', 'q', 'wyjdz', 'koniec']:
                console.print("[yellow]Do widzenia![/yellow]")
                break

            if task.lower() in ['help', 'pomoc']:
                console.print("[bold]Commands:[/bold] exit/quit, help. Type task in natural language.")
                continue

            if not task.strip():
                continue

            agent.run(task)

        except KeyboardInterrupt:
            console.print("\n[yellow]Przerwano. Wpisz 'exit' aby wyjść.[/yellow]")
        except Exception as e:
            console.print(f"[red]Błąd: {str(e)}[/red]")


def main():
    """Główny punkt wejścia."""
    parser = argparse.ArgumentParser(
        description="AI Coding Agent - Automatyzuj zadania programistyczne z AI"
    )
    parser.add_argument(
        "--task",
        type=str,
        help="Zadanie do wykonania (użyj cudzysłowów dla wielowyrazowych zadań)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Uruchom w trybie testowym (bez rzeczywistego wykonywania)"
    )
    parser.add_argument(
        "--no-confirm",
        action="store_true",
        help="Pomiń prośby o potwierdzenie (pełna automatyzacja)"
    )
    parser.add_argument(
        "--interactive",
        "-i",
        action="store_true",
        help="Uruchom w trybie interaktywnym"
    )

    args = parser.parse_args()

    # Zastosuj nadpisania z linii komend
    if args.dry_run:
        Config.DRY_RUN_MODE = True
    if args.no_confirm:
        Config.REQUIRE_CONFIRMATION = False

    try:
        if args.interactive:
            interactive_mode()
        elif args.task:
            agent = CodingAgent()
            agent.run(args.task)
        else:
            parser.print_help()
            console.print("\n[yellow]Użyj --task aby podać zadanie lub --interactive dla trybu interaktywnego.[/yellow]")

    except ValueError as e:
        console.print(f"[red]Błąd konfiguracji: {str(e)}[/red]")
        console.print("[yellow]Upewnij się, że ustawiłeś GEMINI_API_KEY w pliku .env.[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Błąd krytyczny: {str(e)}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()