# Core Rules v5.1

> Always-loaded. Каждый ответ Claude Code следует этой структуре.
> Skills из `.claude/skills/` загружаются on-demand в точках, указанных ниже.

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

## Рефлексия → Правила (КЛЮЧЕВОЙ ЦИКЛ)

После `/reflection` (этап 6 pipeline) ОБЯЗАТЕЛЬНО обновить:
```
Lesson о поведении агента  → memory/feedback_*.md
Lesson о процессе          → core-rules.md или WORKFLOW.md
Предложение по продукту    → tasks/improvements.md
Факт о проекте             → RESEARCH.md
Новый чеклист-пункт        → tasks/checklists/implementation-checklist.md
```
Без обновления хотя бы одного файла — рефлексия НЕ завершена, DONE ЗАБЛОКИРОВАН.

Когда накопилось 5+ items в improvements.md → `/backlog-to-rules` (внедрить в правила).

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
