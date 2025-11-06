"""Narzędzie operacji na systemie plików do czytania i listowania plików."""
import os
from typing import Dict, Any
from langchain_core.tools import BaseTool
from rich.console import Console

console = Console()


class ReadFileTool(BaseTool):
    """Narzędzie do czytania zawartości plików."""

    name: str = "read_file"
    description: str = """Czytaj zawartość pliku.
    Input powinien być ścieżką do pliku (względną lub bezwzględną).
    Przykład: 'app.py' lub './src/main.py'"""

    def _run(self, file_path: str) -> str:
        """Czytaj zawartość pliku."""
        try:
            if not file_path.strip():
                return "BŁĄD: Nie podano ścieżki do pliku."

            file_path = file_path.strip()

            if not os.path.exists(file_path):
                return f"BŁĄD: Plik nie znaleziony: {file_path}"

            if not os.path.isfile(file_path):
                return f"BŁĄD: Ścieżka nie jest plikiem: {file_path}"

            # Sprawdź rozmiar pliku (limit 1MB)
            file_size = os.path.getsize(file_path)
            if file_size > 1024 * 1024:
                return f"BŁĄD: Plik zbyt duży ({file_size} bajtów). Maksymalny rozmiar to 1MB."

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            return f"Zawartość {file_path}:\n\n{content}"

        except UnicodeDecodeError:
            return f"BŁĄD: Nie można odczytać pliku (nie jest plikiem tekstowym): {file_path}"
        except PermissionError:
            return f"BŁĄD: Brak uprawnień do czytania pliku: {file_path}"
        except Exception as e:
            return f"BŁĄD czytania pliku: {str(e)}"

    async def _arun(self, file_path: str) -> str:
        """Wersja async (nie zaimplementowana)."""
        raise NotImplementedError("ReadFileTool nie wspiera wykonywania asynchronicznego.")


class ListDirectoryTool(BaseTool):
    """Narzędzie do listowania zawartości katalogów."""

    name: str = "list_directory"
    description: str = """Listuj pliki i katalogi w podanej ścieżce.
    Input powinien być ścieżką do katalogu (względną lub bezwzględną).
    Użyj pustego stringu lub '.' dla aktualnego katalogu.
    Przykład: '.' lub './src' lub 'C:/projekty/mojaaplikacja'"""

    def _run(self, dir_path: str = ".") -> str:
        """Listuj zawartość katalogu."""
        try:
            if not dir_path.strip():
                dir_path = "."

            dir_path = dir_path.strip()

            if not os.path.exists(dir_path):
                return f"BŁĄD: Katalog nie znaleziony: {dir_path}"

            if not os.path.isdir(dir_path):
                return f"BŁĄD: Ścieżka nie jest katalogiem: {dir_path}"

            items = os.listdir(dir_path)

            if not items:
                return f"Katalog jest pusty: {dir_path}"

            # Rozdziel pliki i katalogi
            files = []
            directories = []

            for item in sorted(items):
                item_path = os.path.join(dir_path, item)
                if os.path.isdir(item_path):
                    directories.append(f"[KATALOG]  {item}")
                else:
                    size = os.path.getsize(item_path)
                    files.append(f"[PLIK] {item} ({size} bajtów)")

            result = f"Zawartość {dir_path}:\n\n"

            if directories:
                result += "Katalogi:\n"
                result += "\n".join(directories)
                result += "\n\n"

            if files:
                result += "Pliki:\n"
                result += "\n".join(files)

            return result

        except PermissionError:
            return f"BŁĄD: Brak uprawnień do dostępu do katalogu: {dir_path}"
        except Exception as e:
            return f"BŁĄD listowania katalogu: {str(e)}"

    async def _arun(self, dir_path: str = ".") -> str:
        """Wersja async (nie zaimplementowana)."""
        raise NotImplementedError("ListDirectoryTool nie wspiera wykonywania asynchronicznego.")


class FileExistsTool(BaseTool):
    """Narzędzie do sprawdzania czy plik lub katalog istnieje."""

    name: str = "file_exists"
    description: str = """Sprawdź czy plik lub katalog istnieje.
    Input powinien być ścieżką do sprawdzenia.
    Zwraca czy ścieżka istnieje i jakiego jest typu.
    Przykład: 'app.py' lub './src'"""

    def _run(self, path: str) -> str:
        """Sprawdź czy ścieżka istnieje."""
        try:
            if not path.strip():
                return "BŁĄD: Nie podano ścieżki."

            path = path.strip()

            if not os.path.exists(path):
                return f"Ścieżka nie istnieje: {path}"

            if os.path.isfile(path):
                size = os.path.getsize(path)
                return f"Ścieżka istnieje i jest PLIKIEM: {path} ({size} bajtów)"
            elif os.path.isdir(path):
                item_count = len(os.listdir(path))
                return f"Ścieżka istnieje i jest KATALOGIEM: {path} ({item_count} elementów)"
            else:
                return f"Ścieżka istnieje ale typ jest nieznany: {path}"

        except PermissionError:
            return f"Ścieżka istnieje ale brak uprawnień: {path}"
        except Exception as e:
            return f"BŁĄD sprawdzania ścieżki: {str(e)}"

    async def _arun(self, path: str) -> str:
        """Wersja async (nie zaimplementowana)."""
        raise NotImplementedError("FileExistsTool nie wspiera wykonywania asynchronicznego.")
