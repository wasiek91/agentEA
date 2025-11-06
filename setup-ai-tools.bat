@echo off
title AI Tools Setup (Offline Version)
color 0A
echo.
echo ==========================================
echo   USTAWIENIE PANELI AI W VS CODE
echo ==========================================
echo.

REM === Ścieżka do ustawień użytkownika VS Code ===
set settingsPath=%APPDATA%\Code\User\settings.json

REM === Tworzenie katalogu jeśli nie istnieje ===
if not exist "%APPDATA%\Code\User" (
    mkdir "%APPDATA%\Code\User"
)

echo 💾 Tworzenie / aktualizacja ustawien VS Code...

(
echo {
echo   "workbench.sideBar.location": "left",
echo   "workbench.activityBar.visible": true,
echo   "workbench.layoutControl.enabled": true,
echo   "workbench.editor.showTabs": true,
echo   "window.newWindowDimensions": "inherit",
echo   "workbench.colorTheme": "Dark Modern",
echo   "locale": "pl",
echo   "security.workspace.trust.enabled": false,
echo   "telemetry.telemetryLevel": "off"
echo }
) > "%settingsPath%"

echo.
echo ⚙️ Teraz musisz tylko zainstalowac rozszerzenia recznie:
echo ------------------------------------------
echo 1. Otworz VS Code
echo 2. Wcisnij Ctrl+Shift+X (Extensions)
echo 3. Wpisz i zainstaluj po kolei:
echo     - openai.openai-chat
echo     - gencay.vscode-chatgpt
echo     - formulahendry.code-runner
echo     - ms-vscode.vscode-ai
echo     - cloude.vscode-cloude
echo     - kilocode.kilocode-ai
echo     - codex-ai.codex
echo ------------------------------------------
echo.
echo ✅ Po instalacji zamknij i uruchom ponownie VS Code.
echo Po lewej pojawia sie panele: Chat, Kilo Code, Codex, OpenAI, Cloude.
echo.
pause
exit
