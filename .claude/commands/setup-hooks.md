---
allowed-tools: Bash(chmod:*), Bash(cp:*), Bash(ls:*)
description: Zainstaluj i skonfiguruj hooks dla agentEA
---

# Setup Hooks

Zainstaluj hook scripts i skonfiguruj Claude Code

## Co robi:

1. ✅ Sprawdza hook skrypty (`.claude/hooks/`)
2. ✅ Ustawia uprawnienia wykonania
3. ✅ Waliduje konfigurację w settings.json
4. ✅ Pokazuje status wszystkich hooks

## Kroki instalacji:

```bash
# 1. Sprawdź czy folder istnieje
ls -la .claude/hooks/

# 2. Ustaw uprawnienia
chmod +x .claude/hooks/*.sh
chmod +x .claude/hooks/*.py

# 3. Test hooks
python .claude/hooks/pre-commit-validation.py < /dev/null
bash .claude/hooks/post-write-format.sh < /dev/null
```

## Dostępne hooks:

1. **pre-commit-validation.py**
   - Sprawdza testy, coverage, secrets
   - Blokuj commit jeśli niebieski

2. **post-write-format.sh**
   - Auto-format Python (black, isort)
   - Runs po każdym write/edit

3. **pre-bash-safety.py**
   - Blokuj dangerous commands
   - rm -rf, git push --force, mkfs, dd

4. **session-setup.sh**
   - Auto-setup na start
   - Load .env, check database

## Veryfikacja:

```bash
# Check configuration
cat .claude/settings.local.json | grep -A 10 '"hooks"'

# Test hook execution
python .claude/hooks/pre-commit-validation.py << EOF
{"tool_name": "Bash", "tool_input": {"command": "echo test"}}
EOF
```

## Troubleshooting:

❌ **Hooks not running?**
- Sprawdzenie: `/hooks` menu
- Verify: settings.json syntax
- Test: chmod +x on scripts

❌ **Permission errors?**
- Ensure: Python 3 installed
- Ensure: Bash available
- Ensure: Black, isort installed (`pip install black isort`)

## Next steps:

```
/experiment your_feature
→ Hooks automatically run
→ If OK → git commit
→ If blocked → fix & retry
```

**All set! 🚀**
