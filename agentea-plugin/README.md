# agentEA Plugin

**Advanced Trading Strategy Automation with RL Optimization, Code Review, and Development Workflow**

🎯 Complete Claude Code plugin for the agentEA ecosystem featuring multi-strategy portfolio management, reinforcement learning optimization, intelligent code review, and automated testing.

## Features

### 🤖 4 Agent Skills
- **Code Reviewer** - Professional code review, security analysis, best practices
- **RL Expert** - Reinforcement learning optimization for trading strategies
- **Architecture Advisor** - System design, scalability, technical decisions
- **Test Generator** - Comprehensive test generation and coverage analysis

### ⚡ 8 Slash Commands
- `/analyze-strategy` - Quick strategy performance analysis
- `/test-backtest` - Run backtests on historical data
- `/check-code` - Quick code quality check
- `/generate-tests` - Generate test templates
- `/optimize-model` - RL model optimization guidance
- `/full-review` - Comprehensive code review workflow
- `/experiment` - Safe experimental sessions with checkpointing
- `/setup-hooks` - Hook installation and configuration

### 🔧 3 Automation Hooks
- **Pre-commit validation** - Tests, coverage, secrets detection before commit
- **Post-write formatting** - Auto-formatting with black/isort
- **Session setup** - Environment initialization and database checks

## Installation

### Via Claude Code

```bash
claude plugin install https://github.com/wasiek91/agentEA/agentea-plugin
```

### Manual

1. Clone the repository:
```bash
git clone https://github.com/wasiek91/agentEA.git
cd agentEA/agentea-plugin
```

2. Install the plugin:
```bash
claude plugin install ./
```

3. Verify installation:
```bash
claude /analyze-strategy
```

## Usage

### Quick Start

**Analyze a trading strategy:**
```bash
/analyze-strategy portfolio-manager-pro/strategies/my_strategy.py
```

**Run a backtest:**
```bash
/test-backtest my_strategy 1y 2024-01-01
```

**Check code quality:**
```bash
/check-code portfolio-manager-pro/main.py
```

### Full Code Review Workflow

```bash
/full-review src/new_feature.py
```

This orchestrates:
1. Quick code check (linting, formatting)
2. Deep code review (security, best practices)
3. Architecture assessment
4. Test generation and coverage
5. Final summary with recommendations

### RL Model Optimization

**Get quick optimization suggestions:**
```bash
/optimize-model sharpe 0.8
```

**For deep consulting:**
Use the RL Expert skill to discuss hyperparameter tuning, convergence issues, reward shaping.

### Safe Experimentation

```bash
/experiment rl_tuning_v2
```

Create experimental sessions with automatic checkpointing. Safely test changes with `/rewind` to undo.

## Agent Skills in Detail

### Code Reviewer Skill
Automatically invoked when you ask Claude to review code, verify security, or improve design.

**Analyzes:**
- Security (OWASP Top 10)
- Code quality and readability
- Performance bottlenecks
- Design patterns
- Test coverage

**Output:** Detailed report with severity levels and actionable recommendations.

### RL Expert Skill
Automatically invoked for reinforcement learning optimization, hyperparameter tuning, model convergence issues.

**Covers:**
- Algorithms (PPO, DQN, A3C, DDPG, SAC)
- Hyperparameter tuning strategies
- Reward function design
- Trading metrics (Sharpe, Drawdown, Win Rate)
- Convergence troubleshooting

**For agentEA:** Specialized in trading strategy optimization with risk management focus.

### Architecture Advisor Skill
Automatically invoked for system design, scalability planning, technical decisions.

**Addresses:**
- Monolith vs microservices trade-offs
- Design patterns and best practices
- Database schema optimization
- API design and versioning
- Deployment strategies
- Technical debt management

**For agentEA:** Expert in integrating Portfolio Manager Pro, Janosik EA, and Coding Agent.

### Test Generator Skill
Automatically invoked for test generation, edge case identification, coverage analysis.

**Generates:**
- Unit test templates with fixtures
- Integration test strategies
- Edge case and error handling tests
- Performance test ideas
- Test organization recommendations

**Target:** 80%+ code coverage.

## Hooks Configuration

Hooks are automatically activated when the plugin is installed.

### Pre-Commit Hook
**Triggers:** Before `git commit` commands

**Validates:**
- ✅ All tests pass (`pytest`)
- ✅ Coverage > 80% (`pytest --cov`)
- ✅ No hardcoded secrets (passwords, API keys, tokens)

**Action:** Blocks commit if checks fail

### Post-Write Hook
**Triggers:** After every file write/edit

**Auto-formats Python files:**
- Black (code formatting)
- isort (import organization)
- mypy (type checking - optional)

**Note:** Runs silently, no action required

### Session Setup Hook
**Triggers:** At Claude Code session start

**Performs:**
- Loads environment variables from `.env`
- Checks PostgreSQL database connection
- Lists recent git branches

## Commands Reference

### `/analyze-strategy [file]`
Quick performance analysis of a trading strategy.

**Output:** Performance score, risk metrics, recommendations

**Time:** ~2 min

---

### `/test-backtest [strategy] [period] [start-date]`
Run historical backtest of a strategy.

**Arguments:**
- `strategy`: Strategy name (required)
- `period`: 3m, 6m, 1y, 2y (default: 1y)
- `start-date`: YYYY-MM-DD (optional)

**Output:** Return, Sharpe, Drawdown, Win Rate, verdict

**Time:** ~5 min

---

### `/check-code [file-or-directory]`
Quick quality check - linting, security, formatting.

**Output:** Issues found, score, status (PASS/REVIEW/FAIL)

**Time:** ~2 min

---

### `/generate-tests [function] [file]`
Generate test templates for a function or module.

**Output:** Test structure, cases identified, coverage estimate

**Time:** ~2 min

---

### `/optimize-model [metric] [value]`
Quick RL optimization guidance for specific metrics.

**Metrics:** sharpe, drawdown, win_rate, loss, convergence

**Output:** Quick fixes, recommended order, expected improvement

**Time:** ~1 min

---

### `/full-review [file-or-feature]`
Comprehensive review orchestrating all tools.

**Includes:**
1. Quick code check
2. Deep code review
3. Architecture assessment
4. Test coverage analysis
5. Final summary

**Output:** Detailed report with recommendations

**Time:** ~40-60 min

---

### `/experiment [experiment-name]`
Start safe experimental session with automatic checkpointing.

**Workflow:**
```
1. Checkpoint (automatic)
2. Experiment
3. Test changes
4. Verdict: Commit ✅ or Rewind ❌
```

**Use cases:**
- RL hyperparameter tuning
- Strategy refactoring
- Architecture exploration
- A/B testing

**Time:** Variable (30 min - 2 hours)

---

### `/setup-hooks`
Installation and configuration guide for automation hooks.

## For agentEA Project

This plugin is specifically designed for the agentEA ecosystem:

### Portfolio Manager Pro
- Multi-strategy orchestration (10-100+ strategies)
- RL optimization with ensemble voting
- REST API on port 8000
- PostgreSQL backend for persistence

### Janosik EA
- Specialized single strategy (XAUUSD focus)
- Deep RL optimization
- Tight risk management (4%-8%-12% drawdown tiers)
- 5% daily loss limit

### Coding Agent
- Autonomous development automation
- CLI-based tool orchestration
- Git integration and batch operations

## Performance Targets (For agentEA Trading)

```
Sharpe Ratio:       > 1.0
Maximum Drawdown:   < 15%
Win Rate:           > 45%
Profit Factor:      > 2.0
Monthly Return:     1-3% (realistic)
```

## Troubleshooting

### Hooks not activating
1. Verify plugin installed: `claude plugin list`
2. Check settings: `claude settings show`
3. Restart Claude Code

### Skills not being invoked
- Skills activate automatically based on context
- Explicitly mention the type of help needed (e.g., "review this for security")
- Use `/full-review` for explicit invocation

### Test generation failing
- Ensure pytest is installed
- Provide clear function signatures
- Include docstrings for context

## Support

For issues, questions, or contributions:
- GitHub Issues: https://github.com/wasiek91/agentEA/issues
- Documentation: https://github.com/wasiek91/agentEA/blob/master/CLAUDE.md

## License

MIT - See LICENSE file

## Credits

Built with Claude Code by Anthropic

---

**Ready to revolutionize your trading strategy development!** 🚀
