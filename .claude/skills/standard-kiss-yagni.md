# Standard: KISS / YAGNI / MVP

## Context

- **When:** EVERY code creation/modification
- **Role:** Guardrails against over-engineering
- **Trigger:** Automatically for ANY task involving code

**CRITICAL:**
These principles are MANDATORY, not optional!
Violation = technical debt + wasted time.

---

## Requirements

### KISS -- Keep It Simple, Stupid

1. **Simplicity beats complexity** -- simple solution is ALWAYS preferred
2. **Less code = fewer bugs** -- minimal code to solve the task
3. **No premature optimization** -- optimize ONLY when problem is proven

### YAGNI -- You Aren't Gonna Need It

1. **No code "for later"** -- do NOT write code "for the future"
2. **Current requirements ONLY** -- implement ONLY current requirements
3. **Remove unused code** -- delete unused code IMMEDIATELY

### MVP Mindset

1. **Start simple** -- begin with the minimal working solution
2. **Add complexity when proven needed** -- add complexity ONLY when necessity is proven
3. **Refactor over rewrite** -- refactoring is preferred over rewriting
4. **Clear initialization** -- simple and clear startup sequence

### One Way Principle

1. **Single way to do X** -- one way for logging, config, error handling
2. **Unified patterns** -- same patterns for same tasks
3. **Project context** -- see project-specific context in relevant config files

---

## Complexity Checklist (MANDATORY before adding complexity)

**BEFORE adding an abstraction/layer/pattern -- answer 5 questions:**

1. Is this feature needed NOW? --> No = DON'T do it
2. Is there a REAL problem this solves? --> No = DON'T do it
3. Does it simplify code for OTHER developers? --> No = DON'T do it
4. Can it be done SIMPLER? --> Yes = do it simpler
5. Does it add a NEW dependency? --> Yes = think twice

If any answer points to excess --> DO NOT add complexity!

---

## Over-Engineering Red Flags (STOP signals)

When detected -- STOP and simplify:

1. **> 3 abstraction layers** for a single operation
2. **Factories creating factories** (Factory of Factories)
3. **Complex configuration** instead of environment variables
4. **Multiple ways** to do the same thing (logging, config, errors)
5. **Single-method interfaces** without a clear reason
6. **Abstraction for code** used only once
7. **"Universal solution"** for a single use case
8. **Implicit initialization** -- complex/magical startup sequence

---

## Examples

**GOOD:** KISS in action
```typescript
// Task: get user name

// KISS -- simple solution
function getUserName(user: User): string {
  return user.name || 'Anonymous';
}

// No extra abstractions, interfaces, factories
// Solves the task in 1 line
```

**GOOD:** YAGNI -- only current requirements
```typescript
// Request: "need an endpoint for user list"

// YAGNI -- only what was asked
app.get('/users', async (req, res) => {
  const users = await db.query('SELECT * FROM users');
  res.json(users);
});

// Do NOT add: pagination, filters, sorting
// until they are REQUESTED
```

**BAD:** Over-engineering
```typescript
// Task: get user name

// Over-engineering -- 5 abstractions for 1 line
interface INameProvider { getName(): string; }
interface IUserNameStrategy { execute(user: User): string; }
class UserNameStrategyFactory { create(type: string): IUserNameStrategy }
class DefaultUserNameStrategy implements IUserNameStrategy { ... }
class UserNameService { constructor(private factory: UserNameStrategyFactory) ... }

// Result: 50 lines instead of 1, maintenance complexity x10
```
Problem: Abstractions "for the future" that never comes. Wasted time on creation and maintenance.

**BAD:** Code "for the future"
```typescript
// Request: "need an endpoint for user list"

// YAGNI violation -- added things NOT requested
app.get('/users', async (req, res) => {
  const { page, limit, sort, filter, search, include } = req.query;
  // ... 100 lines of logic for features nobody asked for
});

// Result: time wasted, features unused, code overcomplicated
```
Problem: "What if we need it" -- in 90% of cases you WON'T.

---

## Critical Points

### MANDATORY:
- Start with the SIMPLEST solution
- Add complexity ONLY when necessity is proven
- Delete unused code IMMEDIATELY
- Pass the Complexity Checklist before adding abstractions

### NEVER:
- Do NOT write code "for the future"
- Do NOT create abstractions "for flexibility"
- Do NOT add layers without a concrete problem
- Do NOT optimize without measurements

### On violation:
STOP --> Remove the excess --> Continue with the simple solution

---

**Version:** 1.1
**Principle:** "Simplicity is the ultimate sophistication" -- Leonardo da Vinci
