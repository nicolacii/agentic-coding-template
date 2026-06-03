# RESEARCH.md — {Project Name} Encyclopedia

> **Hard rule** (`.claude/rules/core-rules.md`): читать этот файл перед первой задачей в сессии.
>
> **Цель:** persistent deep-dive в проект, который не выводится из `git log` или быстрого `grep`. Всё, что стоит знать ДО того как трогать код.
>
> **Обновление:** каждый этап 2 (Analysis) pipeline-а дописывает новую секцию `Phase N`. Исключение: trivial S-tasks без architectural impact.

---

## Лог исследований

| Дата | Секция | Повод | Кто записал |
|------|--------|-------|-------------|
| YYYY-MM-DD | Phase 0 (инициализация) | /init-project step 7 | {author} |

---

## Phase 0: Project Overview

### 0.1 Что это

**{Project Name}** — одно-два предложения о том, что делает проект и для кого.

### 0.2 Deployment

- **Prod:** где развёрнут, через что деплоится
- **Dev:** как запустить локально
- **Секреты:** какие файлы гитигноред, где лежат в prod

### 0.3 Sizes (current state {YYYY-MM-DD})

| Файл / модуль | LOC | Назначение |
|--------------|-----|------------|
| ... | ... | ... |

**Тех-долг:** отметить файлы, превышающие soft/hard limits (см. `.claude/skills/standard-file-size-limits.md`).

---

## Phase 1: Architecture

### 1.1 Высокоуровневая схема

```
[ASCII-диаграмма или ссылка на изображение]
```

### 1.2 Модули и ответственности

| Файл / директория | Слой | Импорты снаружи | Импорты внутри |
|-------------------|------|-----------------|----------------|
| ... | ... | ... | ... |

**Циклы импортов:** есть / нет. Если есть — где и почему accepted.

### 1.3 Data flow для типичного запроса

Пример: типичный пользовательский сценарий, шаг за шагом через все слои. Ссылки на конкретные файлы:строки.

---

## Phase 2: {Domain-specific section}

> Добавляй phases по мере необходимости. Примеры разделов:
>
> - **Phase 2: API Endpoints** — полная таблица HTTP endpoints с request/response contracts
> - **Phase 3: Persistence** — схема БД, модели, миграции, invariants
> - **Phase 4: Authentication** — auth model, session, token lifecycle
> - **Phase 5: Frontend** — ключевые компоненты, state management, routing
> - **Phase 6: Security Model** — все security properties в одном месте
> - **Phase 7: External Integrations** — третьи сервисы, API keys, rate limits

---

## Phase N-1: Environment Variables

| Variable | Default | Used in | Purpose |
|----------|---------|---------|---------|
| ... | ... | ... | ... |

---

## Phase N: Quirks / Gotchas / Technical Debt

Всё, на что легко наступить. Самая важная секция — это то, что НЕ видно из кода напрямую.

### N.1 {Quirk name}

Описание — что происходит, почему, где читать код, как не сломать.

### N.2 Known accepted risks

| Risk | Likelihood | Impact | Why accepted |
|------|-----------|--------|--------------|
| ... | ... | ... | ... |

---

## How to update this file

- **Регулярно:** каждый раз, когда открываешь новый аспект проекта, которого здесь нет — добавляй.
- **После крупной задачи (> 5 files changed):** обязательно секция "Phase N" с изменениями (см. WORKFLOW.md Stage 2 Hard Rule для структуры).
- **Размер:** держи < 2000 строк. Если растёт — разбивай на `RESEARCH-{submodule}.md` и оставляй в главном файле только оглавление.
- **Не дублируй CHANGELOG.md** — CHANGELOG = user-facing, RESEARCH = developer-facing. RESEARCH отвечает на "как оно устроено" и "почему так", CHANGELOG на "что изменилось".
- **Не дублируй AGENTS.md** — AGENTS.md = quick start navigation, RESEARCH.md = deep-dive content.
