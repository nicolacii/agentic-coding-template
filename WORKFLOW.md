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

**Выход:** `tasks/{section}/analysis-{section}.md`

**Анализ архитектуры:**
- Data flow, dependencies, API endpoints
- State shape, risks, recommendations

**Анализ кода:**
- Component assessment, code smells, decomposition

**Если задача архитектурная** → создать **ADR** в `docs/adr/` (см. ADR template).

---

## Этап 3: IMPLEMENT

**Выход:** код + тесты в feature branch

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

**Выход:** `tasks/{section}/review-{section}.md`

Проверить: архитектура, типы, тесты, accessibility, security.

**Verdict:** APPROVED / CHANGES REQUESTED

---

## Этап 5: TESTING

**Выход:** `tasks/{section}/testing-{section}.md`

```
[ ] TypeScript: 0 errors
[ ] Tests: all pass
[ ] Coverage: > 70% для новых файлов
[ ] Build: success
[ ] Visual diff: < 1% (если CSS)
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
