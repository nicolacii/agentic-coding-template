# ADR-{NNN}: {Title}

**Status:** Proposed | Accepted | Rejected | Superseded by ADR-XXX
**Date:** YYYY-MM-DD
**Decided by:** {Author}
**Tags:** architecture, frontend, backend, infrastructure

---

## Context

Что побудило принять решение? Какая проблема решается? Какие constraints?

Пример:
> Старый проект использует Redux Thunks для всех API вызовов. Это приводит к
> дублированию кода (loading/error/data state в каждом slice) и ручному
> управлению cache invalidation.

---

## Decision

Что решено? Конкретно, без воды.

Пример:
> Перевести все серверные запросы на React Query. Redux Toolkit оставить
> только для клиентского state (auth, UI preferences).

---

## Alternatives Considered

Какие варианты рассматривались и почему отвергнуты?

### Alternative 1: {Name}
- **Pros:** ...
- **Cons:** ...
- **Why rejected:** ...

### Alternative 2: {Name}
- **Pros:** ...
- **Cons:** ...
- **Why rejected:** ...

---

## Consequences

### Positive
- ...
- ...

### Negative
- ...
- ...

### Neutral / Risks
- ...

---

## Implementation Notes

Как реализовать решение? Есть ли migration path?

```
Step 1: ...
Step 2: ...
Step 3: ...
```

---

## References

- Related ADRs: ADR-XXX, ADR-YYY
- External docs: [link](url)
- Discussion: [link to issue/PR]
