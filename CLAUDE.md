# CLAUDE.md — Agentic Coding Template

> Шаблон-болванка для создания нового проекта. Универсальные правила процесса — в `~/.claude/CLAUDE.md`, **здесь дублировать НЕ нужно**.

---

## Что это

Стартовый каркас для проектов с workflow-pipeline (TASK → ANALYSIS → IMPLEMENT → REVIEW → TESTING → REFLECTION). Содержит:

- `.claude/skills/` — on-demand протоколы (копируется в новый проект)
- `.claude/sub-agents/` — роли для multi-agent orchestration
- `.claude/project-config.yml` — конфиг (multi_agent mode, sub-agent roster)
- `templates/` — заготовки (research-template, ADR-template, и т.д.)
- `tasks/` — структура для артефактов pipeline
- `WORKFLOW.md` — 6-этапный pipeline (детали)

---

## Как использовать

При создании нового проекта в `Work-work/`:

```bash
NEW_PROJECT_NAME=my-new-project
cp -r agentic-coding-template "../$NEW_PROJECT_NAME"
cd "../$NEW_PROJECT_NAME"
```

Затем в Claude Code из папки нового проекта:

```
/init-project
```

— это интерактивно настроит: project type, stack, multi_agent mode (none/lightweight/full), conventions. Создаст `AGENTS.md`, `RESEARCH.md`, заполнит конфиг.

После `/init-project` — заменить этот файл (`CLAUDE.md`) на slim-версию с проектной спецификой (см. `Analytics-Agent/CLAUDE.md` или `Localisation-Agent/CLAUDE.md` как пример).

---

## Hard rules для самого шаблона

- **README шаблона vs rules:** если README-инструкции «quick start» противоречат rules в `~/.claude/CLAUDE.md` — **rules авторитетнее**. README — для людей, rules — автоматический контракт для агента.
- Шаблон **не содержит** проектного контента: ни AGENTS.md (хаб), ни RESEARCH.md, ни BACKLOG.md. Эти файлы создаются `/init-project` для конкретного проекта.
- Перед обновлением шаблона — сначала валидировать на реальном проекте (например, обкатать на Analytics-Agent), потом переносить в шаблон.
