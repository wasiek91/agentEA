# AI Coding Agent

An intelligent AI coding assistant powered by Claude Sonnet 4.5, LangChain, and LangGraph that automates coding tasks through CLI tool integration.

## Features

- **LangGraph Workflow**: Structured planning-execution-verification cycle
- **CLI Tool Integration**: Safe execution of npm, git, python, node, and aider commands
- **Aider Integration**: Leverage Aider for AI-powered code generation and editing
- **Git Automation**: Automatic version control and change tracking
- **File System Operations**: Read files, list directories, check file existence
- **Safety First**: Command whitelist/blacklist, confirmation prompts, dry-run mode
- **Interactive & CLI Modes**: Use as one-shot command or interactive session

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Coding Agent                       │
│                                                      │
│  ┌──────────┐    ┌───────────┐    ┌─────────────┐ │
│  │ Planning │───▶│ Execution │───▶│Verification │ │
│  └──────────┘    └───────────┘    └─────────────┘ │
│       │               │                    │        │
│       └───────────────┴────────────────────┘        │
│                       │                             │
└───────────────────────┼─────────────────────────────┘
                        │
        ┌───────────────┴───────────────┐
        │                               │
   ┌────▼────┐                    ┌────▼────┐
   │  Tools  │                    │   LLM   │
   └─────────┘                    └─────────┘
        │                              │
   ┌────┴────┬────────┬─────────┐    │
   │         │        │         │     │
 Shell    Aider    Git    FileSystem  │
   │         │        │         │     │
   └─────────┴────────┴─────────┘     │
                                       │
                              Claude Sonnet 4.5
```

### Workflow Nodes

1. **Planning Node**: Analyzes the task and creates a step-by-step execution plan
2. **Execution Node**: Uses available tools to execute the plan
3. **Verification Node**: Checks results and decides whether to continue or complete

### Available Tools

#### Shell Tool (`shell_executor`)
- Execute safe CLI commands
- **Whitelist**: npm, git, python, node, aider, ls, dir, pwd, cd, cat, mkdir, touch
- **Blacklist**: rm, del, format, dd, mkfs, and other destructive commands
- Automatic safety filtering and user confirmation

#### Aider Tools
- `aider_executor`: Run Aider to create/modify code with AI
- `aider_status`: Check Aider installation status

#### Git Tools
- `git_status`: View repository status
- `git_commit`: Commit changes with automatic staging
- `git_diff`: View file differences

#### File System Tools
- `read_file`: Read file contents (max 1MB)
- `list_directory`: List directory contents
- `file_exists`: Check file/directory existence

## Installation

### Prerequisites

- Python 3.8 or higher
- Git
- Node.js and npm (optional, for JS projects)
- Aider (optional but recommended)

### Setup

1. **Clone or create the project directory**:
```bash
mkdir coding-agent
cd coding-agent
```

2. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

3. **Install Aider** (recommended):
```bash
pip install aider-chat
```

4. **Configure environment variables**:
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Anthropic API key
# ANTHROPIC_API_KEY=your_api_key_here
```

5. **Get your Anthropic API key**:
   - Visit https://console.anthropic.com/
   - Create an account or sign in
   - Generate an API key
   - Add it to your `.env` file

## Usage

### One-Shot Command Mode

Execute a single task:

```bash
python agent.py --task "Create a simple Flask todo app"
```

```bash
python agent.py --task "Add unit tests for all functions in app.py"
```

```bash
python agent.py --task "Fix linting errors and commit changes"
```

### Interactive Mode

Start an interactive session:

```bash
python agent.py --interactive
```

Then enter tasks one at a time:
```
Enter task: Create a FastAPI hello world app
Enter task: Add error handling
Enter task: Write tests
Enter task: exit
```

### Command Line Options

- `--task "description"`: Execute a specific task
- `--interactive` or `-i`: Start interactive mode
- `--dry-run`: Preview what would be executed without running commands
- `--no-confirm`: Skip confirmation prompts (use with caution)

### Configuration

Edit `config.py` or set environment variables in `.env`:

```env
# API Configuration
ANTHROPIC_API_KEY=your_key_here
MODEL_NAME=claude-sonnet-4-5-20250929

# Safety Settings
DRY_RUN_MODE=false           # Set to true to preview without executing
REQUIRE_CONFIRMATION=true     # Set to false to skip confirmations

# Agent Settings
VERBOSE=true                  # Show detailed execution logs
```

## Example Workflows

### Example 1: Create a Todo App with Tests

```bash
python agent.py --task "Create a todo app with Flask including add, list, and delete functions, then write pytest tests for all endpoints"
```

**What happens**:
1. **Planning**: Agent breaks down into steps (create Flask app, implement endpoints, write tests)
2. **Execution**:
   - Uses Aider to generate Flask application code
   - Creates test file with pytest
   - Runs tests to verify functionality
3. **Verification**: Checks test results and confirms success
4. **Git Commit**: Automatically commits changes with descriptive message

### Example 2: Fix and Refactor Code

```bash
python agent.py --task "Review app.py for code quality issues, fix any bugs, add docstrings, and ensure PEP8 compliance"
```

**What happens**:
1. Reads `app.py` using `read_file` tool
2. Uses Aider to refactor and improve code
3. Runs linting to verify PEP8 compliance
4. Commits improvements

### Example 3: Interactive Development

```bash
python agent.py --interactive

# Session:
Enter task: Create a React component for a login form
Enter task: Add form validation
Enter task: Write unit tests with Jest
Enter task: Build the project and fix any errors
Enter task: exit
```

## Safety Features

### 1. Command Whitelist/Blacklist
- Only approved commands can be executed
- Destructive commands are blocked automatically

### 2. User Confirmation
- Every shell command requires user approval (unless disabled)
- Clear display of what will be executed

### 3. Dry Run Mode
```bash
python agent.py --task "your task" --dry-run
```
- Preview all operations without executing
- Perfect for testing and understanding agent behavior

### 4. Timeouts
- Shell commands: 5 minute timeout
- Aider commands: 10 minute timeout
- Prevents hanging processes

### 5. File Size Limits
- Maximum file read size: 1MB
- Prevents memory issues with large files

## Troubleshooting

### "ANTHROPIC_API_KEY not found"
- Ensure `.env` file exists in the project root
- Verify `ANTHROPIC_API_KEY` is set correctly
- Check that `python-dotenv` is installed

### "Aider not found"
```bash
pip install aider-chat
```

### "Command blocked by safety filter"
- Review the whitelist in `config.py`
- Ensure command is safe and necessary
- Add to whitelist if appropriate

### Tool execution errors
- Run with `--dry-run` first to preview
- Check that you're in correct directory
- Verify all prerequisites are installed

## Project Structure

```
coding-agent/
├── agent.py              # Main agent with LangGraph workflow
├── config.py             # Configuration management
├── requirements.txt      # Python dependencies
├── .env.example         # Environment template
├── .env                 # Your environment (create this)
├── README.md            # This file
└── tools/               # Tool implementations
    ├── __init__.py
    ├── shell_tool.py    # Shell command execution
    ├── aider_tool.py    # Aider integration
    ├── git_tool.py      # Git operations
    └── filesystem_tool.py # File system operations
```

## Advanced Usage

### Custom Tool Development

Add new tools by extending `BaseTool` from LangChain:

```python
from langchain.tools import BaseTool

class MyCustomTool(BaseTool):
    name = "my_tool"
    description = "What this tool does"

    def _run(self, query: str) -> str:
        # Tool implementation
        return "result"
```

Then add to `agent.py`:
```python
from tools.my_tool import MyCustomTool

self.tools = [
    # ... existing tools
    MyCustomTool(),
]
```

### Adjusting Workflow

Modify the LangGraph workflow in `agent.py`:

```python
def _build_workflow(self) -> StateGraph:
    workflow = StateGraph(AgentState)

    # Add custom nodes
    workflow.add_node("custom_phase", self._custom_node)

    # Modify edges
    workflow.add_edge("execution", "custom_phase")
    workflow.add_edge("custom_phase", "verification")

    return workflow.compile()
```

## Contributing

Contributions are welcome! Areas for improvement:

- Additional tools (database, API, testing frameworks)
- Better error recovery strategies
- Multi-step task decomposition
- Result caching and checkpointing
- Integration with more AI coding tools

## License

MIT License - feel free to use and modify as needed.

## Credits

Built with:
- [Claude](https://www.anthropic.com/claude) by Anthropic
- [LangChain](https://www.langchain.com/) - LLM application framework
- [LangGraph](https://github.com/langchain-ai/langgraph) - Workflow orchestration
- [Aider](https://aider.chat/) - AI pair programming tool
- [Rich](https://rich.readthedocs.io/) - Terminal formatting

## Support

For issues and questions:
- Check the Troubleshooting section
- Review tool documentation in source files
- Ensure all dependencies are correctly installed
- Try running with `--dry-run` and `--verbose` flags

Happy coding with AI!
