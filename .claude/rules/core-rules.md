# Core Rules v5.3

> Always-loaded. Каждый ответ Claude Code следует этой структуре.
> Skills из `.claude/skills/` загружаются on-demand в точках, указанных ниже.

## Project Initialization

При первом запуске в новом проекте → запустить `/init-project` для интерактивной настройки:
- Project type, languages, stack
- Multi-agent mode (none / lightweight / full)
- Sub-agent roles
- Conventions, visual reference URLs

Создаёт: `.claude/project-config.yml`, `PROJECT_KNOWLEDGE.md`, `.claude/sub-agents/*.md`

## Memory entrypoints (читать при необходимости)

| Файл | Назначение | Когда читать |
|------|-----------|-------------|
| `PROJECT_KNOWLEDGE.md` | Главная точка входа памяти | Начало сессии (`/start`) |
| `.claude/project-config.yml` | Stack, multi-agent config | Перед `/orchestrate` |
| `BACKLOG.md` | Реестр задач + приоритеты + история | Перед взятием новой задачи |
| `CHANGELOG.md` | История изменений | Перед merge или release |
| `docs/adr/` | Архитектурные решения | При архитектурных вопросах |
| `tasks/improvements.md` | Backlog улучшений | Перед `/backlog-to-rules` |
| `tasks/reflection-history.md` | История рефлексий + lessons | Для поиска повторяющихся проблем |

## Multi-Agent Orchestration

Для COMPLEX задач (XL, 10+ файлов legacy, миграции) → использовать `/orchestrate`:
- Orchestrator делегирует работу sub-agents через Task tool
- Sub-agents работают в isolated contexts (analysts, developers, reviewers, qa)
- Коммуникация через файлы в `tasks/{section}/`
- Orchestrator не читает большие объёмы кода — только summaries

Условие: `multi_agent.enabled: true` в `.claude/project-config.yml`. Если выключено — делать всё самостоятельно.

---

## ШАГ 0: Сложность (ПЕРВАЯ строка)

```
**Сложность: 🟢 SIMPLE** — [причина]
```

| Уровень | Когда | Flow |
|---------|-------|------|
| 🟢 SIMPLE | 1-2 файла | Execute → Verify → DONE |
| 🟡 STANDARD | Фича, баг, несколько файлов | Prompt Prep → Plan → Execute → Verify → DONE |
| 🔴 COMPLEX | Архитектура, миграция | Prompt Prep → Plan → Execute → Verify + Review → DONE |

## ШАГ 1: Routing (STANDARD/COMPLEX)

**1a. Определить тип задачи → загрузить протокол:**

| Задача | Протокол (ПРОЧИТАТЬ перед работой) |
|--------|----------|
| Новая фича | `/protocol-development` → PRE-ACTION (→ `/check-duplicates`) + TDD |
| Баг | `/protocol-bugfix` → 5 Whys (→ `/error-learning` после фикса) |
| Рефакторинг | `/protocol-refactoring` → Tests first (→ `/techdebt-scan` перед) |
| Данные | `/protocol-research` → Data first |
| Зависание | `/protocol-freeze-recovery` |

**Hard Stop:** без прочтения протокола кодинг ЗАПРЕЩЁН.

**1b. Prompt Prep** (→ `/protocol-prepare-prompt`):
```
Goal: [результат]  Constraints: [ЦИТАТЫ из запроса]  Protocol: [какой]
```

**1c. RAT** — `/validate-from-end` для STANDARD/COMPLEX:
Определить expected output ПЕРЕД началом работы. Category 0: "Я правильно понял запрос?"

## ШАГ 2: Выполнение

- Один файл за раз
- Создал файл → `/check-duplicates` перед созданием
- Изменил → ОТКРОЙ и проверь
- Sequential: types → api → hooks → components → pages
- Перед созданием нового файла → `/check-duplicates`

## ШАГ 3: Проверка → `/verify`

**Полная верификация через `/verify`.** Краткая версия:

**Cross-check** — каждый файл открыть и проверить:
```
| Файл | Открыт | Проверен |
|------|--------|----------|
```

**Challenge** — 4 вопроса:
1. Как опровергнуть? 2. Все файлы открыл? 3. Edge cases? 4. Job решён?

**Confidence** = 100% минус: не тестировал (−50%), не открывал (−40%), нет cross-check (−30%)

**Visual Diff** → `/visual-diff` (для CSS/SCSS):
1. `python3 scripts/visual-diff.py {page}` → diff %
2. Прочитать diff image → красные зоны
3. Исправить → повторить пока diff < 1%
ЗАПРЕЩЕНО говорить "визуально совпадает" без diff < 1%.

## ШАГ 4: DONE (конец КАЖДОГО ответа)

```
---
## DONE
Сложность: 🟢/🟡/🔴
Что сделано: [список]
Проверки: Cross-check ✅ | Challenge ✅
Уверенность: [X]%
---
```

## ШАГ 5: Post-Task

1. Subtasks → отметить [x]
2. Документация → обновить
3. Memory → обновить прогресс
4. Если задача из pipeline → перейти к следующему этапу (см. WORKFLOW.md)

---

## Pipeline Skills (точки вызова в WORKFLOW.md)

| Этап pipeline | Skill | Обязательность |
|---------------|-------|---------------|
| 2. Analysis | — (ручной анализ) | Обязателен |
| 3. Implement | `/protocol-development` или `/protocol-bugfix` | Обязателен |
| 4. Review | `/review` | Обязателен |
| 5. Testing | `/visual-diff` (если CSS) | Обязателен |
| 6. Reflection | `/reflection` → обновить правила | **БЛОКИРУЕТ DONE** |

## Session Skills

| Момент | Skill |
|--------|-------|
| Начало сессии | `/start` — read context, status, pending |
| Конец сессии | `/session-end` — update memory, log errors |
| После багфикса | `/error-learning` — Symptom → Root Cause → Fix |
| 5+ improvements | `/backlog-to-rules` — внедрить в правила |
| Анализ UI/UX | `/evaluate-jobs` — JTBD анализ |
| Ошибка в "done" | `/fix-last-task` — исправление |

## Self-Improvement Loop (КРИТИЧЕСКИЙ ЦИКЛ)

**Принцип:** рефлексия БЕЗ изменения системы — это просто журнал. Каждая рефлексия ОБЯЗАНА produce минимум 1 артефакт self-improvement.

После `/reflection` (этап 6 pipeline) ОБЯЗАТЕЛЬНО создать минимум 1 артефакт:

| Тип lesson | Артефакт |
|-----------|----------|
| Lesson о поведении агента (повторяющаяся ошибка) | `memory/feedback_*.md` |
| Lesson о процессе (новое правило) | `core-rules.md` или `WORKFLOW.md` update |
| **Архитектурное решение** | `docs/adr/ADR-XXX-{title}.md` (НОВЫЙ файл) |
| **Паттерн повторился 3+ раз** | `.claude/skills/{new-skill}.md` (НОВЫЙ файл) |
| Идея для backlog | `tasks/improvements.md` |
| Изменение для пользователя | `CHANGELOG.md` |
| Факт о проекте | `RESEARCH.md` или `PROJECT_KNOWLEDGE.md` |

**Если задача прошла идеально и нечего улучшать** — записать это явно в `tasks/reflection-history.md` с пометкой `No improvements needed` и обоснованием. Это тоже считается артефактом.

**Без артефакта** — рефлексия НЕ завершена, DONE ЗАБЛОКИРОВАН, задача НЕ закрыта.

Когда накопилось 5+ items в `improvements.md` → запустить `/backlog-to-rules` (внедрить в правила).

Когда одна и та же ошибка появляется в `reflection-history.md` 3+ раз → создать новый skill в `.claude/skills/`.

---

## Forbidden

- ❌ `_fixed`, `_final`, `_v2` — edit original
- ❌ "Готово" без открытия файлов
- ❌ "Работает" без запуска
- ❌ "Совпадает" без diff < 1%
- ❌ Код ДО test cases
- ❌ Пропуск pipeline этапов
- ❌ git push без тестов
- ❌ Создание файла без `/check-duplicates`
- ❌ Рефлексия без обновления правил

## Code Standards

**KISS:** Нужно? Решает проблему? Проще? → Нет = НЕ делай. Подробнее: `/standard-kiss-yagni`
**Files:** Components < 200 (400). Services < 400 (800). Подробнее: `/standard-file-size-limits`
**Tests:** TDD. Coverage ≥ 80%. Подробнее: `/standard-code-quality`
**Quality:** Подробнее: `/standard-agent-quality`

## Escalation

| Ситуация | Действие |
|----------|----------|
| Уверенность < 50% | Спросить пользователя |
| > 5 файлов | Показать план, ждать OK |
| Ошибка 3+ раз | СТОП → обновить правила |
