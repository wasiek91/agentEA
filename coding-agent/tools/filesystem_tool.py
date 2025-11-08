"""Narzędzie operacji na systemie plików do czytania i listowania plików."""
import os
from typing import Dict, Any
from langchain_core.tools import BaseTool
from rich.console import Console

console = Console()


class ReadFileTool(BaseTool):
    """Narzędzie do czytania zawartości plików."""

    name: str = "read_file"
    description: str = "Read file contents"

    def _run(self, file_path: str) -> str:
        """Czytaj zawartość pliku."""
        try:
            if not file_path.strip():
                return "Error: No file path"

            file_path = file_path.strip()

            if not os.path.exists(file_path):
                return "Error: File not found"

            if not os.path.isfile(file_path):
                return "Error: Not a file"

            file_size = os.path.getsize(file_path)
            if file_size > 1024 * 1024:
                return "Error: File too large (>1MB)"

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            return content

        except UnicodeDecodeError:
            return "Error: Not a text file"
        except PermissionError:
            return "Error: Permission denied"
        except Exception as e:
            return f"Error: {str(e)}"

    async def _arun(self, file_path: str) -> str:
        """Wersja async (nie zaimplementowana)."""
        raise NotImplementedError("ReadFileTool nie wspiera wykonywania asynchronicznego.")


class ListDirectoryTool(BaseTool):
    """Narzędzie do listowania zawartości katalogów."""

    name: str = "list_directory"
    description: str = "List directory contents"

    def _run(self, dir_path: str = ".") -> str:
        """Listuj zawartość katalogu."""
        try:
            if not dir_path.strip():
                dir_path = "."

            dir_path = dir_path.strip()

            if not os.path.exists(dir_path):
                return "Error: Directory not found"

            if not os.path.isdir(dir_path):
                return "Error: Not a directory"

            items = os.listdir(dir_path)

            if not items:
                return "Empty directory"

            # Rozdziel pliki i katalogi
            files = []
            directories = []

            for item in sorted(items):
                item_path = os.path.join(dir_path, item)
                if os.path.isdir(item_path):
                    directories.append(f"[DIR] {item}")
                else:
                    files.append(f"[FILE] {item}")

            result = ""
            if directories:
                result += "\n".join(directories)
            if files:
                if result:
                    result += "\n"
                result += "\n".join(files)

            return result if result else "Empty"

        except PermissionError:
            return "Error: Permission denied"
        except Exception as e:
            return f"Error: {str(e)}"

    async def _arun(self, dir_path: str = ".") -> str:
        """Wersja async (nie zaimplementowana)."""
        raise NotImplementedError("ListDirectoryTool nie wspiera wykonywania asynchronicznego.")


class FileExistsTool(BaseTool):
    """Narzędzie do sprawdzania czy plik lub katalog istnieje."""

    name: str = "file_exists"
    description: str = "Check if path exists"

    def _run(self, path: str) -> str:
        """Sprawdź czy ścieżka istnieje."""
        try:
            if not path.strip():
                return "Error: No path"

            path = path.strip()

            if not os.path.exists(path):
                return "Not found"

            if os.path.isfile(path):
                return "File"
            elif os.path.isdir(path):
                return "Directory"
            else:
                return "Other"

        except PermissionError:
            return "Permission denied"
        except Exception as e:
            return f"Error: {str(e)}"

    async def _arun(self, path: str) -> str:
        """Wersja async (nie zaimplementowana)."""
        raise NotImplementedError("FileExistsTool nie wspiera wykonywania asynchronicznego.")
