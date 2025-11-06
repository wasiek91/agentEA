# Quick Start Guide

Get up and running with the AI Coding Agent in 5 minutes!

## Step 1: Install Dependencies

```bash
pip install langchain langchain-anthropic langgraph python-dotenv rich
```

Or use the requirements file:
```bash
pip install -r requirements.txt
```

## Step 2: Configure API Key

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Get your Anthropic API key from: https://console.anthropic.com/

3. Edit `.env` and add your key:
```
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
```

## Step 3: Run Setup (Optional)

Check that everything is configured correctly:
```bash
python setup.py
```

## Step 4: Try Your First Task!

### Example 1: Simple Task
```bash
python agent.py --task "List all Python files in the current directory"
```

### Example 2: Interactive Mode
```bash
python agent.py --interactive
```

Then type a task:
```
Enter task: Check git status
Enter task: List files in tools directory
Enter task: exit
```

### Example 3: Safe Dry Run
```bash
python agent.py --task "Install express with npm" --dry-run
```

This will show you what would happen without actually running it!

## Common First Tasks

### 1. Project Setup
```bash
python agent.py --task "Create a Python project structure with src, tests, and docs folders"
```

### 2. Git Operations
```bash
python agent.py --task "Check git status and show what files have changed"
```

### 3. Code Reading
```bash
python agent.py --task "Read the config.py file and summarize what configuration options are available"
```

### 4. Development (with Aider)
First install Aider:
```bash
pip install aider-chat
```

Then:
```bash
python agent.py --task "Create a simple Flask hello world app in app.py"
```

## Tips for Success

1. **Be Specific**: Instead of "make an app", say "create a Flask app with a /hello endpoint that returns JSON"

2. **Break Down Complex Tasks**: For large projects, run multiple smaller tasks in interactive mode

3. **Use Dry Run**: Test complex tasks with `--dry-run` first

4. **Check Confirmations**: The agent will ask before running potentially dangerous commands

5. **Start Simple**: Begin with file listing and reading tasks to get comfortable

## Troubleshooting

### "API key not found"
- Make sure `.env` exists in the `coding-agent` directory
- Check that `ANTHROPIC_API_KEY` is set correctly (starts with `sk-ant-`)

### "Command not in whitelist"
- The agent only runs safe commands by default
- Check `config.py` to see the whitelist
- This is a safety feature!

### "Aider not found"
```bash
pip install aider-chat
```

## What's Next?

- Read the full [README.md](README.md) for detailed documentation
- Explore the tools in the `tools/` directory
- Customize `config.py` for your needs
- Try the example workflows in README.md

## Getting Help

- Check the main README.md for full documentation
- Review tool source code in `tools/` for details
- Use `--dry-run` to preview actions safely

Happy coding!
