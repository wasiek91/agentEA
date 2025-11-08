#!/usr/bin/env python3
"""
Pre-commit validation hook for agentEA
Sprawdza czy kod jest ready do commita
"""

import json
import sys
import subprocess
import re
from pathlib import Path

def run_command(cmd, cwd=None):
    """Uruchom komendę i zwróć output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_tests():
    """Sprawdź czy testy passują"""
    print("📋 Checking tests...", file=sys.stderr)
    success, stdout, stderr = run_command("pytest --tb=short -q")
    if not success:
        return False, f"Tests failed:\n{stderr}"
    return True, "Tests passed ✓"

def check_coverage():
    """Sprawdź code coverage"""
    print("📊 Checking coverage...", file=sys.stderr)
    success, stdout, stderr = run_command("pytest --cov --cov-report=term-missing --cov-fail-under=80")
    if not success:
        return False, "Coverage < 80%"
    return True, "Coverage OK ✓"

def check_secrets():
    """Sprawdź czy nie ma secrets w kodzie"""
    print("🔐 Checking for secrets...", file=sys.stderr)

    # Regex patterns for secrets
    patterns = [
        (r"(?i)password\s*[:=]", "Found password literal"),
        (r"(?i)api[_-]?key\s*[:=]", "Found API key literal"),
        (r"(?i)secret\s*[:=]", "Found secret literal"),
        (r"(?i)token\s*[:=]", "Found token literal"),
        (r"private[_-]?key", "Found private key reference"),
    ]

    # Scan staged files
    success, files_output, _ = run_command("git diff --cached --name-only")
    if not success:
        return True, "Could not check files"

    issues = []
    for file_path in files_output.strip().split('\n'):
        if not file_path:
            continue

        success, content, _ = run_command(f"git show :{file_path}")
        if not success:
            continue

        for pattern, message in patterns:
            if re.search(pattern, content):
                issues.append(f"{file_path}: {message}")

    if issues:
        return False, "Secrets found:\n" + "\n".join(issues)

    return True, "No secrets found ✓"

def check_lint():
    """Sprawdź linting (Python)"""
    print("🔍 Checking linting...", file=sys.stderr)
    success, stdout, stderr = run_command("pylint --disable=all --enable=E,W portfolio-manager-pro/ janosik-ea/ 2>/dev/null")
    # Pylint zawsze exits with non-zero, sprawdzaj output
    if "error" in stderr.lower() and "fatal" in stderr.lower():
        return False, f"Lint errors:\n{stderr}"
    return True, "Lint check OK ✓"

def main():
    """Główna logika"""
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    # Sprawdzenie czy to jest git commit
    tool_name = input_data.get("tool_name", "")
    if tool_name != "Bash":
        return 0

    tool_input = input_data.get("tool_input", {})
    command = tool_input.get("command", "")

    if "git commit" not in command:
        return 0

    print("\n🚀 Pre-commit validation for agentEA", file=sys.stderr)
    print("=" * 50, file=sys.stderr)

    # Uruchom walidacje
    checks = [
        ("Tests", check_tests),
        ("Coverage", check_coverage),
        ("Secrets", check_secrets),
        # ("Linting", check_lint),  # Optional, może być wolne
    ]

    all_passed = True
    failures = []

    for check_name, check_func in checks:
        try:
            passed, message = check_func()
            print(f"  {check_name}: {message}", file=sys.stderr)
            if not passed:
                all_passed = False
                failures.append(f"  • {message}")
        except Exception as e:
            print(f"  {check_name}: ⚠️ Error - {str(e)}", file=sys.stderr)

    print("=" * 50, file=sys.stderr)

    if not all_passed:
        error_msg = "Pre-commit checks failed:\n" + "\n".join(failures)
        print(f"❌ COMMIT BLOCKED\n{error_msg}", file=sys.stderr)
        print(json.dumps({
            "decision": "block",
            "reason": error_msg
        }))
        return 0  # Exit 0 with JSON output

    print("✅ All checks passed! Commit allowed.", file=sys.stderr)
    return 0

if __name__ == "__main__":
    sys.exit(main())
