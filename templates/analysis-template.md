# Analysis: {Section}

> Дата: YYYY-MM-DD

---

## Architecture Review

### Dependency Map
```
Component
├── depends on X
├── depends on Y
└── uses API endpoint Z
```

### API Endpoints
| Endpoint | Method | Request | Response |
|----------|--------|---------|----------|
| | | | |

### State Shape
- Store: [what state]
- React Query: [what queries]
- Local state: [what local state]

### Risks
1. [risk]

### Recommendations
1. [recommendation]

---

## Code Quality Review

### Component Assessment
| Component | Lines | Rating | Comment |
|-----------|-------|--------|---------|
| | | good/refactor/rewrite | |

### Code Smells
1. [file:line] — [description]

### Decomposition Plan
- [god-component] → [split into what]

---

## Agreed Implementation Plan

### Must Fix
1. [blocking issue]

### Should Fix
1. [quality issue]

### Nice to Have
1. [improvement]

---

## Definition of a Good Plan (правила качества плана — источник: Superpowers `writing-plans`)

Каждый implementation-план ОБЯЗАН:

- **Global Constraints дословно из spec** в шапке — version floors, dependency limits, инварианты (копировать verbatim, не пересказывать).
- **Задачи bite-sized (2–5 мин)**: точный путь файла + **полный код** + точная команда + expected output.
- **Блок `Interfaces: Consumes / Produces`** на каждую задачу — какие сигнатуры задача берёт у соседей и какие отдаёт (чтобы исполнитель не читал соседние задачи).
- **TDD-шаги**: написать падающий тест → убедиться что падает → минимальный код → тест зелёный → commit.

🚫 **No Placeholders** (это провал плана, не писать никогда):
- «TODO / TBD / implement later / fill in details»
- «add appropriate error handling / add validation / handle edge cases»
- «write tests for the above» (без самого кода теста)
- «similar to Task N» (повторить код — задачи читают вне порядка)
- шаги, описывающие ЧТО без КАК (для кода — обязателен code block)
- ссылки на типы/функции, не определённые ни в одной задаче

**Plan self-review перед отдачей** (см. `/validate-from-end`): spec-coverage · placeholder-скан · type-consistency между задачами.
