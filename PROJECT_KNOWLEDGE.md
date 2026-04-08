# Project Knowledge — Single Entry Point

> Главный файл памяти проекта. Агент читает это в начале каждой сессии.
> Все знания о проекте — здесь или по ссылкам отсюда.

---

## Project Overview

**Name:** {Project Name}
**Type:** {Web app / Mobile / Library / etc.}
**Status:** {Active / Maintenance / Pilot / etc.}
**Started:** {YYYY-MM-DD}

**One-line description:** что делает проект в одном предложении

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | |
| Backend | |
| Database | |
| Infrastructure | |
| Testing | |

---

## Architecture

**Pattern:** {feature-based / DDD / hexagonal / monolith / microservices}

**Key decisions:** см. `docs/adr/` — все архитектурные решения с обоснованием.

**High-level diagram:**
```
[схема архитектуры или ссылка на изображение]
```

---

## Key Files & Directories

| Path | Purpose |
|------|---------|
| `src/` | Source code |
| `tasks/` | Active tasks (pipeline artifacts) |
| `tasks/archive/` | Archived tasks (per quarter) |
| `docs/adr/` | Architecture Decision Records |
| `BACKLOG.md` | Task backlog with priorities |
| `CHANGELOG.md` | Release history |
| `RESEARCH.md` | Domain knowledge (если есть) |

---

## Active Work

**Current focus:** {что делается сейчас, ссылка на BACKLOG.md секцию}

**Recent decisions:** {последние 3 ADR с одной строкой описания}

---

## Where to Find What

| Need | Look in |
|------|---------|
| Что делать дальше? | `BACKLOG.md` (Active Sprint) |
| Почему так решили? | `docs/adr/` |
| Что было сделано? | `CHANGELOG.md` + `BACKLOG.md` (Recent History) |
| Как устроен старый проект? | `RESEARCH.md` (если миграция) |
| Правила работы агента? | `.claude/rules/` + `CLAUDE.md` |
| Какие skills доступны? | `.claude/skills/` |
| Как работает pipeline? | `WORKFLOW.md` |
| Что улучшить? | `tasks/improvements.md` |
| История ошибок и lessons? | `tasks/reflection-history.md` |

---

## Conventions

### Git
- Branches: `feat/`, `fix/`, `refactor/`, `docs/`
- Commits: conventional commits (`type(scope): description`)
- PR per task

### Code
- File size limits: см. `.claude/skills/standard-file-size-limits.md`
- Test coverage: ≥ 80% for new code
- TypeScript strict, no `any`

### Process
- Pipeline: см. `WORKFLOW.md` (7 этапов)
- Reflection обязательна → должна обновлять правила/ADR/skills

---

## Project-Specific Rules

> Здесь — что специфично для этого проекта (не входит в core-rules)

- _пример: Все API endpoints должны проходить через api/client.ts_
- _пример: Никаких inline styles — только SCSS modules или BEM_
- _пример: Партнёрские интеграции — через config object, не switch_

---

## Glossary

> Domain terms специфичные для проекта

| Term | Meaning |
|------|---------|
| _пример: Bundle_ | _Автоматизация (связка trigger + actions)_ |
| _пример: Step_ | _Один шаг автоматизации (trigger или action)_ |
