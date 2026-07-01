---
name: writing-plans
user-invocable: true
description: How to write an implementation plan an isolated agent (or fresh session) can execute task-by-task without your context. Use for M/L/XL tasks after ANALYSIS, before code — especially before orchestration/subagent handoff. Enforces bite-sized TDD steps, Global Constraints, task interfaces (Consumes/Produces), No Placeholders.
---

# Skill: Writing Plans

> Пиши план так, будто исполнитель НИЧЕГО не знает о нашей кодовой базе и имеет сомнительный вкус.
> Задокументируй всё: какие файлы трогать в каждой задаче, код, как тестировать. Разбей на bite-sized
> задачи. DRY. YAGNI. TDD. Частые коммиты.
> Источник: Superpowers `writing-plans`. Место в пайплайне: Stage 2→3 (WORKFLOW.md), особенно перед
> `/orchestrate` (план — это то, что читают developer-субагенты).

**Зачем:** субагент/свежая сессия видят ТОЛЬКО свою задачу, не твой контекст. План — единственный
источник требований. Плохой план = субагент угадывает intent = переделка.

---

## Когда использовать

- M/L/XL задачи после ANALYSIS, до кода.
- Перед handoff субагентам (subagent-driven / orchestrate) — план заменяет твой контекст.
- XS/S inline — можно облегчённо (DEVELOPMENT PLAN из `/protocol-development` достаточно).

---

## Scope Check
Если спека покрывает несколько независимых подсистем — разбей на отдельные планы (по одному на
подсистему). Каждый план должен давать работающий, тестируемый софт сам по себе.

## File Structure (до задач)
Сначала — карта: какие файлы создаются/меняются и за что каждый отвечает. Здесь фиксируются решения о
декомпозиции. Один файл = одна ответственность. Файлы, которые меняются вместе — живут вместе (дели по
ответственности, не по техническому слою). В существующей кодовой базе — следуй установленным паттернам.

## Header плана (обязателен)
```markdown
# [Feature] Implementation Plan
> **For agentic workers:** REQUIRED SUB-SKILL: используй /orchestrate (subagent-driven) или executing-plans.
**Goal:** [одно предложение — что строим]
**Architecture:** [2-3 предложения о подходе]
**Tech Stack:** [ключевые технологии]

## Global Constraints
[Проектные требования — версии, лимиты зависимостей, правила именования/копирайта, платформа — по одной
строке, ДОСЛОВНЫЕ значения из спеки. Требования каждой задачи неявно включают эту секцию.]
```

## Task Right-Sizing
Задача — наименьшая единица, несущая свой тест-цикл и достойная гейта свежего ревьюера. Setup,
конфиг, скаффолд, доки — сворачивай в ту задачу, чьему deliverable они нужны. Дели только там, где
ревьюер мог бы осмысленно отклонить одну задачу, приняв соседнюю. Каждая задача = независимо
тестируемый deliverable.

## Task Structure
```markdown
### Task N: [Component]
**Files:** Create: `path` · Modify: `path:123-145` · Test: `tests/path`
**Interfaces:**
- Consumes: [что берёт из ранних задач — точные сигнатуры]
- Produces: [на что опираются поздние задачи — точные имена функций, типы параметров/возврата.
  Исполнитель видит только свою задачу; этот блок — как он узнаёт имена/типы соседей.]

- [ ] **Step 1: Написать failing тест** ```<код теста>```
- [ ] **Step 2: Запустить — убедиться, что падает** — Run: `...` Expected: FAIL "..."
- [ ] **Step 3: Минимальная реализация** ```<код>```
- [ ] **Step 4: Запустить — проходит** — Run: `...` Expected: PASS
- [ ] **Step 5: Commit** ```git commit -m "feat: ..."```
```
Каждый шаг = одно действие (2-5 мин).

## No Placeholders (это провалы плана — никогда не пиши)
- «TBD», «TODO», «implement later», «fill in details»
- «Add appropriate error handling / validation / handle edge cases» без конкретики
- «Write tests for the above» без кода тестов
- «Similar to Task N» (повтори код — исполнитель может читать задачи не по порядку)
- Шаги, описывающие ЧТО, но не показывающие КАК (для кода — блок кода обязателен)
- Ссылки на типы/функции, не определённые ни в одной задаче

## Self-Review (после написания плана, сам, без субагента)
1. **Spec coverage:** пройди каждое требование спеки → укажи задачу, что его реализует. Пробел → добавь задачу.
2. **Placeholder scan:** ищи паттерны из «No Placeholders». Чини.
3. **Type consistency:** типы/сигнатуры/имена в поздних задачах совпадают с определёнными в ранних? (`clearLayers()` в Task 3 vs `clearFullLayers()` в Task 7 = баг.)
Нашёл — чини инлайн, без ре-ревью.

## Execution Handoff
После сохранения плана предложи выбор исполнения:
1. **Subagent-Driven (рекоменд.)** — свежий субагент на задачу + ревью между задачами (`/orchestrate`).
2. **Inline** — исполнить в этой сессии с чекпоинтами.
