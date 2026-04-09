# WORKFLOW.md — Development Pipeline v2

> Каждая задача с кодом проходит 7 обязательных этапов.
> Git workflow интегрирован: feature branch на старте, PR на завершении.

---

## Pipeline

```
┌──────┐  ┌────────┐  ┌──────────┐  ┌───────────┐  ┌────────┐  ┌──────┐  ┌─────────┐  ┌────────┐
│0.GIT │→ │1.TASK  │→ │2.ANALYSIS│→ │3.IMPLEMENT│→ │4.REVIEW│→ │5.TEST│→ │6.REFLECT│→ │7.MERGE │
└──────┘  └────────┘  └──────────┘  └───────────┘  └────────┘  └──────┘  └─────────┘  └────────┘
```

---

## Этап 0: GIT — Создание ветки

**Выход:** новая feature ветка

```bash
# Префикс по типу задачи:
git checkout -b feat/{section}      # новая фича
git checkout -b fix/{section}       # багфикс
git checkout -b refactor/{section}  # рефакторинг
git checkout -b docs/{section}      # документация

# Пример:
git checkout -b feat/error-pages
```

**Правила:**
- Одна задача = одна ветка
- Имя ветки = имя секции (slugified)
- Базовая ветка = `main` (или `develop` если используете gitflow)

---

## Этап 1: TASK

**Выход:** `tasks/{section}/tasks-{section}.md`

1. Прочитать `BACKLOG.md` — найти задачу
2. Определить scope: страницы, компоненты, API
3. Sub-tasks (5-8 высокоуровневых) с тестами в каждом
4. Указать Relevant Files
5. Обновить `BACKLOG.md` — статус задачи `IN_PROGRESS`

---

## Этап 2: ANALYSIS

**Выход:**
- Manual: `tasks/{section}/analysis-{section}.md`
- Orchestrated: `tasks/{section}/analyst-architect.md` + `analyst-*.md` файлы
- **MANDATORY для migration projects:** дописать новую секцию в `RESEARCH.md`

### 🔴 HARD RULE для migration projects: дописывать в RESEARCH.md

**Если проект — migration** (`reference.legacy.path` set in `.claude/project-config.yml`):

Каждый analyst Stage 2 ОБЯЗАН написать находки про legacy НЕ ТОЛЬКО в свой output файл (`analyst-*.md`), но и **дописать секцию в `RESEARCH.md`** на корне проекта. Структура секции:

```
## Phase N: {Section Name} (YYYY-MM-DD)

### N.1 Architecture
- Файлы: список с LOC
- Cross-module dependencies (что модуль читает извне)
- Routes (URLs из legacy paths.ts)

### N.2 API Endpoints
- Полная таблица: # | endpoint | method | request | response | notes
- TypeScript contracts (interface/type definitions)

### N.3 State Shape
- Legacy Redux slice (если есть)
- Selectors / hooks
- User profile fields consumed

### N.4 Data Flows
- Каждая бизнес-операция: trigger → API → store/cache → component

### N.5 Risks / Quirks
- Race conditions, security, performance, edge cases
- Legacy hacks, технический долг, что НЕ воспроизводить
```

И обновить **Лог исследований** таблицу в начале RESEARCH.md.

**Зачем:** RESEARCH.md — это persistent encyclopedia старого проекта, переиспользуется во всех итерациях миграции (в т.ч. если эта итерация будет признана неудачной и переписана). Без записи в RESEARCH.md ценные данные остаются только в `tasks/{section}/analyst-*.md` который привязан к конкретной попытке миграции и теряется при rewrite.

**Lesson task 10.0 Billing 2026-04-08:** analyst-architect собрал ~700 строк деталей про legacy billing, но они остались только в `tasks/billing/analyst-architect.md`. Пользователь явно просил единый файл-энциклопедию для случая если проект придётся переписать → теперь hard rule.

**Verification:** перед закрытием Stage 2 orchestrator ОБЯЗАН проверить:
```
[ ] RESEARCH.md содержит новую "Phase N" секцию по этой задаче
[ ] Лог исследований обновлён
[ ] Минимум: API endpoints + state shape + data flows + routes
```

### Auto-orchestration (для COMPLEX с `multi_agent.enabled: true`)

Orchestrator АВТОМАТИЧЕСКИ spawn analysts параллельно через Task tool:
```
Task("analyst-architect") + Task("analyst-fe-senior")  # parallel
```

После завершения:
1. Orchestrator читает output файлы
2. **MANDATORY:** orchestrator (или analyst-architect) дописывает Phase N в RESEARCH.md
3. Aggregates → `tasks/{section}/implementation-plan.md`

### Manual mode

**Анализ архитектуры:** data flow, dependencies, API endpoints, state shape, risks
**Анализ кода:** component assessment, code smells, decomposition

**Если задача архитектурная** → создать **ADR** в `docs/adr/` (см. ADR template).
**Если migration project** → ОБЯЗАТЕЛЬНО дописать Phase N в `RESEARCH.md` (см. Hard Rule выше).

---

## Этап 3: IMPLEMENT

**Выход:** код + тесты в feature branch

### Auto-orchestration (для COMPLEX)

Orchestrator АВТОМАТИЧЕСКИ spawn developers SEQUENTIALLY:
```
Task("developer-types")     # 1st
→ wait → read output
Task("developer-api")       # 2nd, reads developer-types output
→ wait → read output
Task("developer-ui")        # 3rd, reads developer-api output
→ wait → read output
```

Sequential потому что слои зависят друг от друга. Orchestrator контекст не растёт — sub-agents работают изолированно.

### Manual mode

**Hard Stop:** перед кодом
```
[ ] Прочитал analysis-{section}.md
[ ] Выполнил PRE-ACTION (Duplicate Check + JTBD)
[ ] Таблица тест-кейсов создана (TDD Phase 0)
[ ] Я в feature branch (не в main)
```

**Порядок:** types → api → hooks → components → pages

**После каждого parent task:**
- `tsc --noEmit` — 0 errors
- Tests green
- `git commit` с conventional commit message
- Task file `[x]`

---

## Этап 4: REVIEW

**Выход:** `tasks/{section}/review-{section}.md` ИЛИ `reviewer-*.md` файлы

### Auto-orchestration (для COMPLEX)

Orchestrator АВТОМАТИЧЕСКИ spawn reviewers PARALLEL:
```
Task("reviewer-architect") + Task("reviewer-fe-senior")  # parallel
+ Task("reviewer-security")   # if backend project
+ Task("reviewer-backend")    # if backend project
```

Если verdict = CHANGES REQUESTED → orchestrator spawn нужного developer для fix → re-review.

### Manual mode

Проверить: архитектура, типы, тесты, accessibility, security.

**Verdict:** APPROVED / CHANGES REQUESTED

---

## Этап 5: TESTING

**Выход:** `tasks/{section}/testing-{section}.md` ИЛИ `qa-results.md`

### Что Stage 5 проверяет (regression scope)

Stage 5 — это **полный regression**, не только новые тесты:

```bash
npx tsc --noEmit          # вся кодовая база (а не только новые файлы)
npx vitest run            # ВСЕ тесты, не только новые — это и есть regression suite
npx vite build            # production билд всей сборки
python3 scripts/visual-diff.py {page}  # для CSS/UI работы
```

Если новый код сломал существующие фичи — `vitest run` это поймает. Это автоматическая регрессия.

### Visual-diff — MANDATORY для migration projects (HARD RULE с 2026-04-08)

**Если проект — migration с легаси reference (см. `.claude/project-config.yml` → `reference.legacy.path`):**

Visual-diff ОБЯЗАТЕЛЕН для каждой новой страницы перед мержем. Это HARD acceptance gate, не optional.

```
[ ] Каждая новая страница миграции прошла visual-diff < 1% против legacy production
[ ] Если diff > 1% → итерировать SCSS пока не пройдёт, ЛИБО explicitly defer в visual debt с записью в BACKLOG.md
[ ] "Skipped because no reference" — НЕ валидное основание. Reference = legacy production URL.
```

**Lesson (task 10.0 Billing 2026-04-08):** visual-diff был skipped в QA stage (sub-agent не имел Bash, orchestrator забыл re-run), 5 страниц замержились с diff 2.82-27.12% от legacy. Premature merge пойман только пост-фактум по жалобе пользователя. Это структурный fail enforcement → теперь hard rule.

### Auto-orchestration (для COMPLEX)

Orchestrator АВТОМАТИЧЕСКИ spawn qa:
```
Task("qa") → runs tsc, vitest, build, visual-diff
```

QA sub-agent итерирует visual-diff пока < 1%.
**Если QA sub-agent не имеет Bash доступа** → orchestrator ОБЯЗАН re-run static checks И visual-diff сам перед commit. См. `/orchestrate` Circuit Breaker → QA Bash requirement.

### Manual mode

```
[ ] TypeScript: 0 errors
[ ] Tests: all pass (full suite — это regression)
[ ] Coverage: > 70% для новых файлов
[ ] Build: success
[ ] Visual diff: < 1% (если CSS И ЕСТЬ legacy reference) — MANDATORY для migration
```

---

## Этап 6: REFLECTION (ключевой этап)

**Выход:** `tasks/{section}/reflection.md` + **обязательное** обновление одного из:

```
Lesson о поведении агента?  → memory/feedback_*.md
Lesson о процессе?          → core-rules.md или WORKFLOW.md
Архитектурное решение?      → docs/adr/ADR-XXX-{title}.md (НОВЫЙ)
Повторяющийся паттерн (3+)? → .claude/skills/{new-skill}.md (НОВЫЙ)
Предложение по продукту?    → tasks/improvements.md
Факт о проекте?             → RESEARCH.md (если есть)
Изменение в продукте?       → CHANGELOG.md
```

**Self-improvement enforcement:** если рефлексия НЕ создала минимум 1 артефакт из списка — она НЕ завершена. DONE заблокирован.

### 7 вопросов
1. Что сделано хорошо?
2. Что пошло не так?
3. Что бы сделал по-другому?
4. Какие паттерны повторять?
5. Какие паттерны избегать?
6. Что нужно доработать?
7. Какие правила/скиллы добавить? **← обязан указать конкретный файл**

---

## Этап 7: MERGE

**Выход:** PR смержен в main, ветка удалена

```bash
# 1. Push feature branch
git push -u origin feat/{section}

# 2. Создать PR
gh pr create --title "{type}({scope}): {description}" --body "..."

# 3. После approval — merge
gh pr merge --squash --delete-branch

# 4. Обновить BACKLOG.md → статус DONE + ссылка на PR
# 5. Обновить CHANGELOG.md → запись о выпуске
# 6. Локально:
git checkout main && git pull
```

---

## Hard Stop Rules

1. **Нельзя кодить** без feature branch (этап 0)
2. **Нельзя кодить** без `analysis-{section}.md` (этап 2)
3. **Нельзя говорить "готово"** без `review-{section}.md` (этап 4)
4. **Нельзя закрывать задачу** без `reflection.md` + минимум 1 артефакта self-improvement (этап 6)
5. **Нельзя мержить** без passed testing (этап 5)
6. **Нельзя говорить "визуально совпадает"** без visual diff < 1%
7. **"Давай дальше" НЕ отменяет pipeline**

---

## Архивация

Когда `tasks/` накопит 30+ папок:

```bash
# Перенести завершённые задачи в архив
mkdir -p tasks/archive/2026-Q1
mv tasks/{old-section-1,old-section-2,...} tasks/archive/2026-Q1/

# Обновить BACKLOG.md — добавить ссылки на архивные задачи
```

Архивация раз в квартал. Активные задачи остаются в `tasks/`.

---

## Lightweight Mode (для S задач)

Для микро-задач (typo, 1 файл, обновление текста) можно использовать lightweight pipeline:

```
0.GIT → 3.IMPLEMENT → 5.TEST → 7.MERGE
```

Пропускаются: 1.TASK, 2.ANALYSIS, 4.REVIEW, 6.REFLECTION.

**Условие:** задача < 30 строк изменений, нет нового функционала, нет архитектурных решений.

**ВНИМАНИЕ:** lightweight mode — это исключение, не правило. Если сомневаешься — используй full pipeline.

---

## Lessons Learned

| Дата | Ошибка | Исправление |
|------|--------|-------------|
| _пример_ | Pipeline пропускался "для скорости" | Все 7 этапов обязательны для full mode |
| _пример_ | Visual match "на глаз" | Automated pixel diff (< 1%) |
| _пример_ | Reflection без обновления правил | Self-improvement enforcement добавлен |
