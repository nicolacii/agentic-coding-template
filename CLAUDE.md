# CLAUDE.md — Project Instructions

> Этот файл загружается автоматически в каждый разговор с Claude Code.
> Скопируйте в корень проекта и добавьте проектную специфику.

---

## Response Protocol

### Каждый ответ ОБЯЗАН содержать:

**1. Сложность** (первая строка):
```
**Сложность: 🟢 SIMPLE** — [причина]
```

| Уровень | Когда | Flow |
|---------|-------|------|
| 🟢 SIMPLE | 1-2 файла | Execute → Verify → DONE |
| 🟡 STANDARD | Фича, баг, несколько файлов | Prompt Prep → Plan → Execute → Verify → DONE |
| 🔴 COMPLEX | Архитектура, миграция | Prompt Prep → Plan → Execute → Verify + Review → DONE |

**2. Prompt Preparation** (STANDARD/COMPLEX):
```
Goal: [результат]
Constraints: [ДОСЛОВНЫЕ цитаты из запроса]
Protocol: [какой протокол применить]
```

**3. DONE блок** (в конце КАЖДОГО ответа):
```
---
## DONE
Сложность: 🟢/🟡/🔴
Что сделано: [список]
Проверки: Cross-check ✅ | Challenge ✅
Уверенность: [X]%
---
```

---

## Routing Table

| Задача | Протокол |
|--------|----------|
| Новая фича | `.claude/skills/protocol-development.md` → TDD |
| Баг / ошибка | `.claude/skills/protocol-bugfix.md` → 5 Whys |
| Рефакторинг | `.claude/skills/protocol-refactoring.md` → Tests first |
| Данные / анализ | `.claude/skills/protocol-research.md` → Data first |

---

## Verification Rules

### Cross-check (каждый ответ)
Каждый созданный/изменённый файл: ОТКРЫТЬ и проверить ДРУГИМ методом.

### Challenge (4 вопроса)
1. Как опровергнуть? 2. Все файлы открыл? 3. Edge cases? 4. Job решён?

### Visual Diff (для CSS/UI работы)
```bash
python3 scripts/visual-diff.py {page}
```
Итерировать пока diff < 1%. **ЗАПРЕЩЕНО** говорить "визуально совпадает" без diff < 1%.

---

## Рефлексии → Правила (обязательный цикл)

После КАЖДОЙ рефлексии (этап 6 pipeline):
```
Lesson о поведении агента?   → memory/feedback_*.md
Lesson о процессе?           → core-rules.md или WORKFLOW.md
Предложение по продукту/UX?  → tasks/improvements.md
Факт о проекте?              → RESEARCH.md
```

**ЗАПРЕЩЕНО** записывать рефлексию без обновления хотя бы одного из этих файлов.

---

## Code Standards

- **KISS/YAGNI:** Перед абстракцией: нужно сейчас? Решает реальную проблему? Можно проще?
- **File Size:** Components < 200 строк (hard: 400). Services < 400 (hard: 800).
- **Tests:** TDD. Coverage ≥ 80% для нового кода.
- **Commits:** `type(scope): description` — feat, fix, refactor, test.

---

## Forbidden Actions

- ❌ Файлы с `_fixed`, `_final`, `_v2`
- ❌ "Готово" без открытия файлов
- ❌ "Работает" без запуска
- ❌ "Совпадает" без visual diff < 1%
- ❌ Код ДО test cases
- ❌ Пропускать pipeline этапы
- ❌ git push без тестов

---

## Проектная специфика (ЗАПОЛНИТЬ)

```
## Контекст
- Стек: [ваш стек]
- Архитектура: [описание]

## Ключевые файлы
- [путь]: [описание]

## Правила проекта
- [ваши правила]
```
