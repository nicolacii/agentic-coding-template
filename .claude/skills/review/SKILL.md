---
name: review
user-invocable: true
description: Code review skill — structured review with architecture, code quality, tests, accessibility, security checks. Used at stage 4 of WORKFLOW pipeline OR standalone. Outputs review-{section}.md with verdict APPROVED or CHANGES REQUESTED. Triggers on review request, before merge, or after implementation.
---

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

---

## Rubric + Verdict (усиление, источник: Superpowers `requesting-code-review`)

**Whole-branch review дроби fresh-субагентом** (свой контекст, не история сессии).
Обязателен после крупной фичи и перед мержем. Дробить с git-диапазоном (BASE..HEAD).

**Read-only:** ревьюер НЕ мутирует рабочее дерево/индекс/HEAD. Только `git show/diff/log`;
для чужой ревизии — отдельный `git worktree`, не двигать HEAD.

**5 осей (чек-лист, не «посмотри код»):**
1. **Plan alignment** — реализовано по плану/требованиям? Отклонения — улучшения или проблемы?
2. **Code quality** — separation of concerns, error handling, type safety, DRY без преждевременной абстракции, edge cases.
3. **Architecture** — здравые решения, scalability/perf, security, чистая интеграция.
4. **Testing** — тесты проверяют **реальное поведение, не моки**; edge cases; integration где важно; все зелёные.
5. **Production readiness** — миграции, обратная совместимость, доки, очевидные баги.

**Калибровка severity** (не всё Critical):
- 🔴 **Critical (Must Fix)** — баги, security, потеря данных, сломанная функциональность.
- 🟡 **Important (Should Fix)** — архитектура, missing features, плохой error handling, дыры в тестах.
- 🟢 **Minor (Nice to Have)** — стиль, оптимизация, доки.

Каждый issue = `file:line + что не так + почему важно + как чинить`. **Сначала признать strengths** (точная похвала повышает доверие к остальному фидбеку).

**Обязательный verdict в конце:** `Ready to merge? Yes / No / With fixes` + 1-2 предложения обоснования. Без вердикта review не завершён.

После получения findings → применять через skill `/receiving-review`.
