#!/bin/bash
# Session setup hook - Auto setup on session start

echo "🚀 Setting up agentEA session..." >&2

# Load .env if exists
if [ -f "$CLAUDE_PROJECT_DIR/.env" ]; then
  echo "📦 Loading .env..." >&2
  if [ -n "$CLAUDE_ENV_FILE" ]; then
    # Persist to CLAUDE_ENV_FILE for subsequent bash commands
    while IFS='=' read -r key value; do
      [[ "$key" != "#"* ]] && [ -n "$key" ] && echo "export $key='$value'" >> "$CLAUDE_ENV_FILE"
    done < "$CLAUDE_PROJECT_DIR/.env"
  fi
fi

# Check PostgreSQL connection
if command -v psql &> /dev/null; then
  if [ -n "$DATABASE_URL" ]; then
    echo "🗄️  Checking database..." >&2
    if psql "$DATABASE_URL" -c "SELECT 1" > /dev/null 2>&1; then
      echo "✅ Database connected" >&2
    else
      echo "⚠️  Database connection failed" >&2
    fi
  fi
fi

# List recent branches
if command -v git &> /dev/null; then
  echo "📚 Recent branches:" >&2
  git branch -v --sort=-committerdate | head -5 >&2
fi

echo "✅ Session ready!" >&2
exit 0
