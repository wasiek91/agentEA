# Code Reviewer Skill - Documentation

**Claude's Professional Code Review Expert**

Automatically invoked when you ask Claude to review code, identify security issues, improve design, or analyze best practices.

---

## When Does This Skill Activate?

Claude automatically uses the Code Reviewer skill when you ask questions like:

- "Przejrzyj ten kod pod względem bezpieczeństwa"
- "Czy ta funkcja jest bezpieczna?"
- "Jakie są problemy z wydajnością w tym pliku?"
- "Sprawdź czy kod follows best practices"
- "Jest tutaj jakieś zagrożenie OWASP?"

---

## What It Analyzes

### 🔒 Security (OWASP Top 10)
- Injection attacks (SQL, Command, etc.)
- Authentication & authorization flaws
- Sensitive data exposure
- XML external entities (XXE)
- Broken access control
- Security misconfiguration
- Cross-Site Scripting (XSS)
- Insecure deserialization
- Using components with known vulnerabilities
- Insufficient logging & monitoring

### 📊 Code Quality
- Code readability and maintainability
- Function complexity
- Naming conventions
- Documentation quality
- Dead code

### ⚡ Performance
- Algorithmic inefficiencies
- Memory leaks
- N+1 query problems
- Unnecessary loops or calculations

### 🏗️ Design Patterns
- Proper use of design patterns
- Anti-patterns detection
- SOLID principles violations
- DRY (Don't Repeat Yourself)

### 🧪 Testing
- Test coverage gaps
- Missing edge case handling
- Testability issues

---

## Real-World Example

### Input
```python
def process_user_data(user_input):
    # Extract email from user input
    email = user_input['email']

    # Execute SQL query
    query = f"SELECT * FROM users WHERE email = '{email}'"
    result = db.execute(query)

    return result
```

### Code Reviewer Response
```
🔴 CRITICAL VULNERABILITY: SQL Injection (A03:2021)
Location: Line 7
Problem: Direct concatenation of user input into SQL query
Risk: Attacker can bypass authentication or steal entire database

Exploit Example:
email = "' OR '1'='1' --"
→ Query becomes: SELECT * FROM users WHERE email = '' OR '1'='1' --'
→ Returns ALL users regardless of email

✅ Fix: Use parameterized queries
db.execute("SELECT * FROM users WHERE email = ?", [email])
```

---

## Common Use Cases

### Before Production Deployment
```
"Przejrzyj całą api_server.py przed wdrożeniem do produkcji"

→ Checks: Security, performance, design
→ Output: Prioritized list of issues & fixes
```

### Code Security Audit
```
"Czy są jakieś problemy bezpieczeństwa w tym kodzie?"

→ Focuses on OWASP Top 10
→ Output: Severity levels, exploit examples, mitigations
```

### Performance Optimization
```
"Jak mogę zoptymalizować wydajność tej funkcji?"

→ Analyzes: Algorithms, database queries, memory usage
→ Output: Specific optimizations with expected impact
```

### Refactoring Assistance
```
"Czy ten kod jest dobrze sformułowany? Jak mogę go ulepszyć?"

→ Analyzes: Design patterns, readability, maintainability
→ Output: Refactoring suggestions with code examples
```

---

## Output Format

### Typical Report Includes:

1. **Executive Summary** - Overall code health score
2. **Critical Issues** - Must-fix security/performance problems
3. **Medium Issues** - Should-fix design/quality improvements
4. **Low Issues** - Nice-to-have optimization suggestions
5. **Recommendations** - Actionable next steps

---

## Tips for Best Results

### ✅ Do's
- Provide full function/class context (not just snippets)
- Include docstrings for better understanding
- Mention the purpose/goal of the code
- Ask specific questions ("review for security" vs just "review")

### ❌ Don'ts
- Don't ask for fixes for intentionally vulnerable code (it will refuse)
- Don't provide code fragments without context
- Don't expect refactoring for encrypted/binary data

---

## Integration with Other Skills

### Works Great With:

1. **Test Generator Skill**
   - Review finds issues → Test Generator writes tests for edge cases
   - Example: "Review for edge cases, then generate tests"

2. **Architecture Advisor Skill**
   - Review identifies design issues → Architecture suggests restructuring
   - Example: "Is this architecture secure and scalable?"

3. **Slash Commands**
   - Use `/check-code` for quick review
   - Use `/full-review` for comprehensive analysis

---

## FAQ

**Q: Why isn't it finding all security issues?**
A: Code Reviewer focuses on most common OWASP risks. For advanced security audits, use external tools (SAST, DAST).

**Q: Can it fix the code automatically?**
A: No, it refuses to improve intentionally vulnerable code. It provides recommendations instead.

**Q: How detailed are the reports?**
A: Very detailed - includes line numbers, exploit examples, and specific mitigations.

**Q: Does it understand my codebase context?**
A: Yes, if you provide file imports and dependencies. Better context = better analysis.

---

## Example Output

```
═══════════════════════════════════════════════════════════════
📋 CODE REVIEW REPORT: core_mt5.py
═══════════════════════════════════════════════════════════════

Overall Score: 6.2/10 ⚠️

🔴 CRITICAL (1)
  ├─ A07: Hardcoded MT5 credentials (line 45)
  └─ Impact: Complete account compromise

🟡 MEDIUM (3)
  ├─ A04: No input validation on account numbers (line 78)
  ├─ A05: Missing error handling in network calls (line 120)
  └─ A02: Race condition in trade execution (line 156)

🟢 LOW (2)
  ├─ Code readability: Long function (230 lines) (line 30)
  └─ Performance: Inefficient data parsing (line 95)

Recommendations:
1. Move credentials to environment variables (CRITICAL)
2. Add input validation (MEDIUM)
3. Refactor long functions (LOW)

Time to Fix: ~2-3 hours
═══════════════════════════════════════════════════════════════
```

---

## Support

- **Report Issues**: github.com/wasiek91/agentEA/issues
- **See Full Plugin Docs**: README.md
