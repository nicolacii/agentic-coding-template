---
name: protocol-freeze-recovery
user-invocable: true
description: Protocol for recovery when AI agent is stuck, looping, or repeating same failed action. Triggers when same error happens 3+ times, infinite loop detected, or user says застрял, зависание, freeze, stuck, looping. Enforces Understand Before Retry.
---

# Protocol: Freeze Recovery

> Когда AI завис, зациклился, не отвечает. Принцип: UNDERSTAND BEFORE RETRY.
> Запуск: `/protocol-freeze-recovery` или "завис", "зациклился", "freeze"

---

**CRITICAL: НЕ перезапускай код который завис! Сначала найди причину.**

## Workflow

1. **НЕ перезапускай** код который завис
2. **ПРОВЕРЬ** что запускал и как
3. **НАЙДИ** почему завис (RCA — 5 Whys)
4. **ИСПРАВЬ** причину
5. Только потом **повторяй**

## Immediate Actions

```markdown
## FREEZE DETECTED
**Что делал:** [описание]
**Команда:** [exact command]
**Время работы:** [сколько]
**Последний output:** [что видел]
```

## Common Freeze Patterns

| Pattern | Cause | Fix |
|---------|-------|-----|
| Infinite loop | No exit condition | Add limit/break |
| Memory overflow | Large dataset | Process in chunks |
| Network timeout | Slow API | Add timeout |
| Deadlock | Race condition | Review locks |
| npm install hangs | Sandbox/network | Ask user to run from terminal |

## Examples

GOOD: RCA перед retry
```
## FREEZE DETECTED
**Команда:** df.groupby('id').apply(complex_func)
**Время:** > 5 минут

### RCA:
Why 1: Долго выполняется
Why 2: complex_func тяжёлая на каждую строку
Why 3: 1M rows × O(n) = слишком много

### Fix: Vectorize или limit rows
```

BAD: Retry без понимания
```
Завис. Перезапускаю...
Опять завис. Попробую ещё раз...
```
Проблема: Причина не найдена, будет зависать снова.

---

**NEVER** retry без понимания причины. **ALWAYS** RCA (5 Whys) → fix → retry.
