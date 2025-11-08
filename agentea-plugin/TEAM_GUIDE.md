# Team Guide - agentea-plugin

**Installation, Setup, and Workflow Guide for Teams**

---

## 📥 Installation for Team Members

### Quick Setup (5 minutes)

**Step 1: Clone Repository**
```bash
git clone https://github.com/wasiek91/agentEA.git
cd agentEA
```

**Step 2: Load Plugin in Claude Code**
```bash
# When starting a Claude Code session, use:
npx claude --plugin-dir ./agentea-plugin

# Or add to permanent settings:
# See "Permanent Installation" below
```

**Step 3: Verify Installation**
```bash
# In Claude Code, try:
/check-code agentea-plugin/README.md

# Should see output confirming plugin is active
```

---

## 🔧 Permanent Installation (Optional)

If you want the plugin always available without `--plugin-dir`:

### Windows
```powershell
# Edit: C:\Users\<username>\.claude\settings.local.json

# Add to enabledPlugins:
"enabledPlugins": {
  "agentea-plugin": {
    "source": "directory",
    "path": "C:/path/to/agentEA/agentea-plugin"
  }
}
```

### macOS/Linux
```bash
# Edit: ~/.claude/settings.json

# Add to enabledPlugins:
"enabledPlugins": {
  "agentea-plugin": {
    "source": "directory",
    "path": "/path/to/agentEA/agentea-plugin"
  }
}
```

---

## 🎯 Team Workflow Examples

### Workflow 1: Code Review Before Pull Request

**Step 1: Prepare Code**
```bash
# Make changes to portfolio-manager-pro/new_feature.py
```

**Step 2: Start Claude Code with Plugin**
```bash
npx claude --plugin-dir ./agentea-plugin
```

**Step 3: Request Review**
```
You: "Przejrzyj portfolio-manager-pro/new_feature.py
      pod względem bezpieczeństwa i wydajności"

→ Code Reviewer Skill automatically invokes
→ Returns detailed report with fixes
```

**Step 4: Address Issues & Commit**
```bash
git add portfolio-manager-pro/new_feature.py
git commit -m "fix: Address security issues from review"

# Pre-commit hook validates tests pass
```

---

### Workflow 2: RL Model Optimization Sprint

**Day 1: Problem Identification**
```
You: "Jak mogę zwiększyć Sharpe ratio modelu z 0.6 do 1.0?"

→ RL Expert Skill returns optimization strategy
```

**Day 2: Implementation**
```bash
# RL Expert recommended specific changes:
1. Update reward function
2. Adjust hyperparameters
3. Increase network size
4. Add risk metrics to state

# Implement + run backtesting
```

**Day 3: Testing & Validation**
```
You: "/full-review rl_engine.py"

→ Complete review: code quality + architecture + tests
```

---

### Workflow 3: Architecture Planning Meeting

**Before Meeting:**
```
You: "Jak zmienia się architektura gdy skalujemy
      z 10 na 100+ strategii w Portfolio Manager?"

→ Architecture Advisor provides detailed analysis
→ Monolith vs Microservices comparison
→ Hybrid recommendation with diagrams
```

**During Meeting:**
- Share Architecture Advisor's output
- Discuss trade-offs (use their analysis)
- Make decisions based on expert recommendations

---

## 📚 Documentation Files

| File | Purpose | Audience |
|------|---------|----------|
| **README.md** | Overview, quick start, test results | Everyone |
| **SKILL_CODE_REVIEWER.md** | How to use Code Reviewer Skill | QA, Senior Devs |
| **SKILL_RL_EXPERT.md** | RL optimization strategies | ML Engineers, Traders |
| **SKILL_ARCHITECTURE_ADVISOR.md** | System design decisions | Architects, Tech Leads |
| **SKILL_TEST_GENERATOR.md** | Testing strategies | QA, All Developers |
| **TEAM_GUIDE.md** | This file - setup & workflows | Everyone |

---

## 🔑 Key Features by Role

### For Developers
- `/check-code` - Quick code quality check
- `/generate-tests` - Generate test templates
- Code Reviewer - Security & quality review

### For QA
- Test Generator Skill - Comprehensive test generation
- `/test-backtest` - Validate trading strategies
- Coverage analysis and edge case detection

### For Team Leads
- Architecture Advisor - Design decisions
- `/full-review` - Complete code assessment
- Performance metrics & bottleneck identification

### For ML Engineers
- RL Expert Skill - Model optimization
- `/optimize-model` - Quick tuning guidance
- Hyperparameter recommendations

---

## 💡 Best Practices

### ✅ Do's
1. **Use slash commands for quick checks**
   ```
   /check-code [file] → 2 min
   ```

2. **Use Skills for in-depth analysis**
   ```
   "Przejrzyj ten kod" → Code Reviewer Skill (5 min)
   ```

3. **Run `/full-review` before major PRs**
   ```
   Complete review: code + architecture + tests
   ```

4. **Ask specific questions for better results**
   ```
   "Optimize for Sharpe ratio specifically" (better)
   vs "Optimize the model" (generic)
   ```

5. **Provide context to Claude**
   ```
   Include: imports, dependencies, docstrings, requirements
   ```

### ❌ Don'ts
1. **Don't ask for fixes to vulnerable code**
   - Claude will refuse (intentional policy)
   - Ask for recommendations instead

2. **Don't overwhelm with huge codebases at once**
   - Break into modules: "Review just mt5_connector.py"
   - Use file references

3. **Don't skip the documentation**
   - Read SKILL_*.md files for your use case
   - Saves time in long run

4. **Don't use hooks if they're problematic**
   - They're optional
   - Can be disabled in settings if needed

---

## 🚨 Troubleshooting

### Problem: Plugin not loading

**Solution:**
```bash
# Check plugin directory
ls agentea-plugin/

# Should see:
# - .claude-plugin/plugin.json
# - skills/
# - commands/
# - hooks/
# - README.md

# If missing, reinstall from git
git pull origin master
```

---

### Problem: Skills not invoking automatically

**Solution:**
```
# Claude invokes skills based on context
# Be specific with your questions:

❌ "Przejrzyj ten kod"
✅ "Przejrzyj ten kod pod względem bezpieczeństwa OWASP"

❌ "Zoptymalizuj model"
✅ "Jak mogę zwiększyć Sharpe ratio z 0.6 do 1.0?"
```

---

### Problem: Hook validation failing on commit

**Solution:**
```bash
# Hook validates:
# 1. Tests pass (pytest)
# 2. Coverage > 80%
# 3. No secrets in code

# Fix:
1. Run tests: pytest tests/
2. Check coverage: pytest --cov
3. Check for secrets: grep -r "password\|api_key\|token"
```

---

## 📊 Performance Expectations

| Operation | Time | Notes |
|-----------|------|-------|
| `/check-code` | ~2 min | Quick lint & format check |
| `/analyze-strategy` | ~2 min | Performance analysis |
| Code Reviewer | ~5 min | Deep security review |
| RL Expert | ~10 min | Optimization strategy |
| Architecture Advisor | ~15 min | Design analysis |
| `/full-review` | ~40 min | Complete assessment |

---

## 🤝 Team Collaboration

### Sharing Results
```bash
# Copy Claude response → paste into pull request
# Documents design decisions for team

Example PR comment:
"""
## Architecture Review by agentea-plugin

Per Architecture Advisor recommendation:
- Use Hybrid architecture (Monolith + Microservices)
- Keep trading core as single process
- Scale support services independently

[Full recommendation in claude-review.md]
"""
```

### Code Review Checklist
Use plugin results to create standardized reviews:

```markdown
- [ ] Security review (Code Reviewer Skill)
- [ ] Architecture assessment (Architecture Advisor)
- [ ] Test coverage (Test Generator)
- [ ] Performance check (Code Reviewer)
- [ ] Best practices (Code Reviewer)
```

---

## 📞 Support & Feedback

### Questions?
1. Check the relevant SKILL_*.md file
2. See README.md "Troubleshooting" section
3. Open GitHub issue: github.com/wasiek91/agentEA/issues

### Want to improve the plugin?
- Suggest new Skills or Commands
- Report bugs via GitHub issues
- Share workflow examples that worked well

---

## 🎓 Learning Path

**Week 1: Basics**
- [ ] Try `/check-code` on a file
- [ ] Use Code Reviewer Skill (ask: "review for security")
- [ ] Read SKILL_CODE_REVIEWER.md

**Week 2: Testing & QA**
- [ ] Use Test Generator Skill
- [ ] Try `/generate-tests`
- [ ] Read SKILL_TEST_GENERATOR.md

**Week 3: Performance & ML**
- [ ] Use RL Expert Skill
- [ ] Try `/optimize-model`
- [ ] Read SKILL_RL_EXPERT.md

**Week 4: Architecture**
- [ ] Use Architecture Advisor Skill
- [ ] Try `/full-review`
- [ ] Read SKILL_ARCHITECTURE_ADVISOR.md

---

## ✅ Ready to Get Started!

```bash
# Next steps:

1. Clone repo
git clone https://github.com/wasiek91/agentEA.git

2. Load plugin
npx claude --plugin-dir ./agentea-plugin

3. Try your first command
/check-code agentea-plugin/README.md

4. Share with team!
"We now have AI-powered code reviews, testing, and architecture advice"
```

**Happy coding! 🚀**
