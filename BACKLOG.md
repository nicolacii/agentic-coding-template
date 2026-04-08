# Backlog

> Единый источник правды для всех задач проекта.
> Обновляется на этапах 1 (TASK) и 7 (MERGE) каждой задачи.

---

## Active Sprint / Current Focus

> Что делается прямо сейчас. Максимум 3-5 задач IN_PROGRESS одновременно.

| ID | Title | Status | Priority | Owner | Started |
|----|-------|--------|----------|-------|---------|
| _пример_ | _G-001 Groups CRUD_ | _IN_PROGRESS_ | _High_ | _claude_ | _2026-04-08_ |

---

## Backlog (TODO)

> Приоритезированный список задач. Сортировка: P0 → P1 → P2.

### P0 — Critical (блокирует release)

| ID | Title | Description | Effort | ADR? |
|----|-------|-------------|--------|------|
| | | | S/M/L/XL | yes/no |

### P1 — High (важно для следующего release)

| ID | Title | Description | Effort | ADR? |
|----|-------|-------------|--------|------|
| | | | | |

### P2 — Medium (nice to have)

| ID | Title | Description | Effort | ADR? |
|----|-------|-------------|--------|------|
| | | | | |

### P3 — Low (когда будет время)

| ID | Title | Description | Effort | ADR? |
|----|-------|-------------|--------|------|
| | | | | |

---

## Recent History (последние 10 завершённых)

> Краткое описание последних завершённых задач со ссылками на артефакты.
> Старше 10 — переезжает в `tasks/archive/`.

| ID | Title | Done | PR | Artifacts | ADR |
|----|-------|------|----|-----------| ----|
| _пример_ | _G-001 Groups CRUD_ | _2026-04-07_ | _#42_ | _tasks/g-001/_ | _ADR-005_ |

---

## Task Groups

> Группировка задач по эпикам. Каждая группа имеет общую цель.

### Group: {Name}

**Goal:** что хотим достичь

**Tasks:**
- [x] G-001: ...
- [x] G-002: ...
- [ ] G-003: ...
- [ ] G-004: ...

**Status:** 2/4 done

---

## Status Legend

| Status | Meaning |
|--------|---------|
| `BACKLOG` | В очереди, не начата |
| `IN_PROGRESS` | В работе сейчас |
| `BLOCKED` | Заблокирована (указать чем) |
| `IN_REVIEW` | На code review |
| `IN_TESTING` | На тестировании |
| `DONE` | Завершена и смержена |
| `CANCELLED` | Отменена (указать причину) |
