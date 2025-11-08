---
allowed-tools: Bash(chmod:*), Bash(ls:*)
description: Zainstaluj i skonfiguruj hooks dla agentEA
---

# Setup Hooks

Zainstaluj hook scripts i skonfiguruj Claude Code

## Co robi:

1. ✅ Sprawdza hook skrypty
2. ✅ Ustawia uprawnienia wykonania
3. ✅ Waliduje konfigurację
4. ✅ Pokazuje status wszystkich hooks

## Kroki instalacji:

```bash
# 1. Sprawdź czy folder istnieje
ls -la ./hooks/

# 2. Ustaw uprawnienia
chmod +x ./hooks/*.sh
chmod +x ./hooks/*.py

# 3. Test hooks
python ./hooks/pre-commit-validation.py < /dev/null
bash ./hooks/post-write-format.sh < /dev/null
```

## Dostępne hooks:

1. **pre-commit-validation.py**
   - Sprawdza testy, coverage, secrets
   - Blokuje commit jeśli problemy

2. **post-write-format.sh**
   - Auto-format Python (black, isort)
   - Runs po każdym write/edit

3. **session-setup.sh**
   - Auto-setup na start
   - Load .env, check database

## Veryfikacja:

```bash
# Check configuration
cat settings.local.json | grep -A 10 '"hooks"'

# Test hook execution
python ./hooks/pre-commit-validation.py << EOF
{"tool_name": "Bash", "tool_input": {"command": "echo test"}}
EOF
```

## Troubleshooting:

❌ **Hooks not running?**
- Verify settings.json syntax
- Test: chmod +x on scripts

❌ **Permission errors?**
- Ensure: Python 3 installed
- Ensure: Bash available
- Ensure: Black, isort installed

## Next steps:

```
/experiment your_feature
→ Hooks automatically run
→ If OK → git commit
→ If blocked → fix & retry
```

**All set! 🚀**
