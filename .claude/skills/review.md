# Skill: Interactive Code Review

> Структурированный code review с options и рекомендациями. Для standalone использования вне pipeline.
> Запуск: `/review` или "сделай code review", "проверь код"

---

## Когда вызывать

- После завершения фичи/бага (вне pipeline)
- Перед мержем в main
- Для ревью чужого кода / PR
- Для самопроверки перед отправкой

---

## Процесс

### 1. Определить режим

Спросить пользователя:
```
Режим ревью:
1/ BIG — полный (4 секции, до 4 issues в каждой)
2/ SMALL — быстрый (1 вопрос на секцию)
```

### 2. Четыре секции ревью

#### Секция 1: Architecture
- Design: правильно ли выбран подход?
- Coupling: нет ли лишних зависимостей?
- Data flow: данные идут правильным путём?
- Security: нет ли XSS, injection, CSRF проблем?

#### Секция 2: Code Quality
- Organization: файлы на своих местах? Naming ok?
- DRY: нет ли дублирования?
- Error handling: ошибки обработаны?
- Tech debt: не создаём ли новый долг?

#### Секция 3: Tests
- Coverage: все ли пути покрыты?
- Assertions: тесты проверяют реальное поведение, не trivial?
- Edge cases: граничные случаи покрыты?
- Failure modes: что если API упал, данные пустые, timeout?

#### Секция 4: Performance
- N+1: нет ли лишних запросов в цикле?
- Memory: нет ли утечек (неочищенные listeners, refs)?
- Caching: можно ли кэшировать?
- Complexity: O(n) vs O(n²)?

#### Секция 5: CTO Review (для COMPLEX задач)
- Scope: масштаб изменений адекватен задаче?
- Risk assessment: что может сломаться? Rollback plan?
- Alternatives: рассмотрены ли другие подходы?
- Dependencies: не создаём ли coupling между модулями?
- Scalability: выдержит ли 10x нагрузку?
- Security: OWASP top 10, auth/authz, input validation?

### 3. Формат для каждого issue

```markdown
### Issue {N}: {название}

**Файл:** `{path}:{line}`
**Severity:** 🔴 Critical / 🟡 Warning / 🟢 Info

**Проблема:** {описание}

**Options:**
A) {рекомендуемый вариант}
   - Effort: {low/medium/high}
   - Risk: {low/medium/high}
   - Impact: {описание}

B) {альтернатива}
   - Effort: {low/medium/high}
   - Risk: {low/medium/high}
   - Impact: {описание}

C) Do nothing
   - Risk: {описание}

**Рекомендация:** Option A — {почему}
```

### 4. Итог

```markdown
## Review Summary

| Секция | Issues | Critical | Warning | Info |
|--------|--------|----------|---------|------|
| Architecture | {N} | {N} | {N} | {N} |
| Code Quality | {N} | {N} | {N} | {N} |
| Tests | {N} | {N} | {N} | {N} |
| Performance | {N} | {N} | {N} | {N} |

**Verdict:** APPROVE / REQUEST CHANGES / BLOCK

### Blocking issues:
{list if any}

### Recommended improvements:
{list if any}
```

---

## Engineering Preferences

- DRY — флаговать дублирование агрессивно
- Тесты — обязательны, не опционально
- "Engineered enough" — не хрупко, не over-abstracted
- Больше edge cases, не меньше
- Explicit лучше clever
- Каждый issue = file:line + конкретные options
