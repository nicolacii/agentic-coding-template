---
name: validate-from-end
user-invocable: true
description: Validate from end skill — define expected output BEFORE starting work, then verify after. MANDATORY for STANDARD/COMPLEX tasks. Prevents agent from working without clear success criteria. Outputs Goal, Expected Artifacts, Acceptance Criteria.
---

# Skill: Validate From End

> Валидация от результата — определить ожидаемый output ПЕРЕД работой, затем проверить.
> Запуск: `/validate-from-end` или "проверь результат", "определи ожидаемый результат"

---

## Когда вызывать

- Перед началом любой STANDARD/COMPLEX задачи
- Когда нужно убедиться что результат соответствует ожиданиям
- При gap analysis: ожидание vs реальность

---

## Процесс

### 1. ПЕРЕД началом работы

```markdown
## EXPECTED OUTPUT

### Task: [что нужно сделать]

### Expected Output:
- [ ] [конкретный deliverable 1]
- [ ] [конкретный deliverable 2]

### Success Criteria:
1. [измеримый критерий 1]
2. [измеримый критерий 2]

### Test Cases:
| # | Input | Expected Output | Pass/Fail |
|---|-------|-----------------|-----------|
| 1 | [input] | [expected] | [ ] |
| 2 | [negative case] | [expected error] | [ ] |
```

### 2. ПОСЛЕ завершения работы

```markdown
## OUTPUT QUALITY CHECK

### Functional:
- [ ] Output совпадает с expected?
- [ ] Все test cases pass?
- [ ] Edge cases обработаны?

### Technical:
- [ ] Компилируется без ошибок?
- [ ] Тесты проходят?
- [ ] Нет регрессий?

### Cross-Check:
- [ ] Каждый артефакт открыт и проверен?
- [ ] Expected vs Actual сравнены?
```

### 3. GAP ANALYSIS (если есть расхождения)

```markdown
## GAP ANALYSIS: Expected vs Actual

| # | Expected | Actual | Gap | Action |
|---|----------|--------|-----|--------|
| 1 | [ожидание] | [реальность] | [разница] | [fix] |

### Root Cause:
- [почему gap 1]

### Remediation:
1. [действие для fix gap 1]
```

---

## Принцип

```
BEFORE: Какой должен быть результат?
DURING: Двигаюсь ли к этому результату?
AFTER:  Совпадает ли результат с ожиданием?
ALWAYS: Могу ли доказать это?
```

---

## Self-review артефакта (spec / plan) — источник: Superpowers `brainstorming` + `writing-plans`

RAT выше проверяет **вход** (правильно ли понял). Это — проверка **выхода** (сам артефакт),
свежим взглядом, ПЕРЕД тем как отдать его пользователю / в реализацию.

**Spec self-review (для дизайн-документа / постановки):**
- [ ] **Placeholder-скан** — нет «TBD / TODO / уточнить позже / решим потом».
- [ ] **Внутренние противоречия** — секции не конфликтуют; архитектура совпадает с описанием фич.
- [ ] **Scope** — не пора ли декомпозировать на под-проекты?
- [ ] **Ambiguity** — любое требование, читаемое двояко → выбрать одно, написать явно.

**Plan self-review (для implementation-плана):**
- [ ] **Spec-coverage** — каждое требование spec → есть задача? Перечислить gaps.
- [ ] **Placeholder-скан** — нет «add error handling / handle edge cases / similar to Task N / write tests» без кода.
- [ ] **Type-consistency** — сигнатуры/имена в задаче N совпадают с задачей M (функция, которую назвали `foo()` в Task 3 и `fooBar()` в Task 7 — баг).

Нашёл проблему → **исправь inline** и двигайся дальше (без повторного ревью). Нет gap'ов → продолжай.
