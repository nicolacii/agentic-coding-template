---
name: standard-agent-quality
description: Agent and QA quality metrics — success criteria for AI agent work, QA checklists, definition of done. Use to evaluate if a task is truly complete or if quality is acceptable.
---

# Standard: Agent & QA Quality

---

## Agent Quality

### Context

- **When:** VERIFY phase of all tasks
- **Goal:** Measurable quality criteria for AI agent work
- **Impact:** Reduce repeated errors, improve first-time quality

### Success Metrics

**Task-Level:**
- Linter errors = 0 (100%)
- Compilation on first attempt (>90%)
- Cross-check successful (100%)
- Challenge passed (100%)

**Session-Level:**
- Tasks without rework (>80%)
- Repeated errors (<10%)

### Guardrails

| Allowed | Forbidden |
|---------|-----------|
| Edit project code | Delete files without 100% certainty |
| Create files on request | Files with `_fixed`, `_final` |
| Suggest improvements | Change architecture without approval |
| Fix errors | Hide errors via try/catch |

### Escalation Rules

| Situation | Action |
|-----------|--------|
| Confidence < 50% | Ask the user |
| Change >5 files | Show plan, get OK |
| Architectural decision | Propose options |
| Unclear requirements | Ask questions |

### Feedback Loop

```
Task completed --> Quick Learning --> Was there an error?
├── No --> Continue
└── Yes --> Record in improvements-backlog.md
```

**CRITICAL:**
Error repeated 3+ times --> STOP --> Update the instruction immediately

### Agent Quality Quick Check

```markdown
## Quality Check

- [ ] Linter = 0
- [ ] Artifacts opened
- [ ] Cross-check completed
- [ ] Confidence calibrated
- [ ] No guardrail violations
```

---

## QA Standards

### Context

- **When:** Code Review, Development verification
- **Goal:** Code acceptance criteria

### Code Quality Checklist

- [ ] 0 linter errors
- [ ] 0 TypeScript errors
- [ ] No console.log (except debug)
- [ ] Tests pass
- [ ] Edge cases handled
- [ ] Error cases handled

### Naming Standards

| Type | Convention | Example |
|------|------------|---------|
| Files (components) | PascalCase | `<ComponentName>.tsx` |
| Files (utils) | camelCase | `<utilName>.ts` |
| Functions | camelCase | `<functionName>()` |
| Components | PascalCase | `<ComponentName>` |
| Constants | UPPER_SNAKE | `<CONSTANT_NAME>` |

### JTBD Verification (user-facing)

```markdown
## JTBD Verification
- [ ] Job Story implemented
- [ ] UI texts about benefits, not about features
- [ ] Minimum steps to result
- [ ] No unclear terminology
```

### QA Examples

**GOOD:** Full QA check
```markdown
## QA CHECKLIST

### Code:
- [x] 0 linter errors
- [x] 0 TypeScript errors
- [x] Tests pass

### JTBD:
- [x] Job Story: "When searching for deals, I want a date filter"
- [x] UI: "Show for period" -- about the result
```

### QA Critical Points

- Linter = 0 ALWAYS
- For user-facing features: JTBD verification
- Edge cases documented and handled

---

**Version:** 1.1
