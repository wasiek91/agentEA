#!/bin/bash
# Post-write formatting hook - Auto format Python files
# Runs after every file write/edit

if [ -z "$CLAUDE_PROJECT_DIR" ]; then
  exit 0
fi

# Get tool input
tool_input=$(cat)
file_path=$(echo "$tool_input" | grep -o '"file_path":"[^"]*"' | cut -d'"' -f4)

# Check if file is Python
if [[ ! "$file_path" =~ \.py$ ]]; then
  exit 0
fi

echo "🎨 Auto-formatting $file_path..." >&2

# Run formatters
if command -v black &> /dev/null; then
  black "$file_path" --quiet 2>/dev/null
fi

if command -v isort &> /dev/null; then
  isort "$file_path" --quiet 2>/dev/null
fi

# Optional: type checking
if command -v mypy &> /dev/null; then
  mypy "$file_path" --ignore-missing-imports 2>/dev/null || true
fi

echo "✅ Formatting done" >&2
exit 0
