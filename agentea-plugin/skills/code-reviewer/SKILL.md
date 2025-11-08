---
description: "Professional code review - security, performance, best practices, design patterns"
capabilities: ["code quality analysis", "security review", "performance optimization", "design patterns", "test coverage"]
tags: ["code-review", "quality-assurance", "security", "best-practices"]
---

# Code Reviewer Skill

Professional code reviewer specializing in comprehensive code analysis, security hardening, and quality improvements.

## Capabilities

- **Code Quality Analysis** - Assess code cleanliness, readability, maintainability
- **Security Review** - Identify OWASP vulnerabilities (injection, XSS, SQL injection, auth issues)
- **Performance Optimization** - Find bottlenecks and suggest improvements
- **Design Patterns** - Verify correct pattern usage and architectural alignment
- **Test Coverage** - Analyze unit and integration testing completeness

## When Claude should invoke this skill

Claude should automatically invoke the Code Reviewer skill when:
- User asks for code review or inspection
- Code needs security hardening
- Performance concerns are raised
- Design pattern verification needed
- Test coverage gaps identified
- Pre-commit quality check requested

## Detailed Review Criteria

### 1. Security (OWASP Top 10)
- SQL injection risks
- Cross-site scripting (XSS)
- Authentication/authorization flaws
- Hardcoded secrets/credentials
- Insecure deserialization
- Broken access control

### 2. Code Quality
- Function length (should be < 50 lines)
- Variable naming conventions
- Parameter count (should be ≤ 4)
- Code duplication
- Comments and docstrings
- Type hints and documentation

### 3. Performance
- Database query optimization
- Memory usage patterns
- Algorithm complexity (Big O)
- Caching opportunities
- Async/await usage
- Connection pooling

### 4. Testing
- Test presence and coverage (target: 80%+)
- Edge case handling
- Mock/fixture usage
- Integration test completeness
- Error path coverage

### 5. Architecture
- Pattern adherence
- Layer separation
- Dependency injection
- API contract consistency
- Tech debt indicators

## Scoring System

**✅ EXCELLENT** (0-3 issues)
- Production ready
- No blocking concerns
- Can merge immediately

**🟡 GOOD** (4-10 issues)
- Minor improvements needed
- Suggest refactoring
- Address before merge

**🔴 NEEDS WORK** (11+ issues or security issues)
- Blocking concerns
- Major refactoring required
- Must fix before merge

## Output Format

```
## Code Review Results

**File**: [filename]
**Lines**: [count]

### Security Issues
- [issue 1]: [severity]
- [issue 2]: [severity]

### Code Quality Issues
- [issue 1]
- [issue 2]

### Performance Issues
- [issue 1]
- [issue 2]

### Testing Issues
- Coverage: [%]
- [issue 1]

### Recommendations
1. [High priority fix]
2. [Medium priority improvement]
3. [Nice to have enhancement]

**Overall Score**: [X/10]
**Status**: [EXCELLENT/GOOD/NEEDS_WORK]
```

## Context for agentEA Project

For the agentEA trading platform:
- Verify strategy implementations are correct and safe
- Check RL model code for numerical stability
- Ensure risk management controls are in place
- Validate MT5 API integration security
- Review portfolio optimization algorithms
