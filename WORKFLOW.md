# WORKFLOW.md — Development Pipeline

> Каждая задача с кодом проходит 6 обязательных этапов.
> Без исключений по размеру, типу или "простоте".

---

## Pipeline

```
┌────────┐   ┌──────────┐   ┌───────────┐   ┌────────┐   ┌────────┐   ┌───────────┐
│ 1.TASK │ → │2.ANALYSIS│ → │3.IMPLEMENT│ → │4.REVIEW│ → │5.TEST  │ → │6.REFLECT  │
└────────┘   └──────────┘   └───────────┘   └────────┘   └────────┘   └───────────┘
```

---

## Этап 1: TASK

**Выход:** `tasks/{section}/tasks-{section}.md`

1. Определить scope: страницы, компоненты, API
2. Сгенерировать parent tasks (5-8 высокоуровневых)
3. Сгенерировать sub-tasks с тестами в каждом блоке
4. Указать Relevant Files

---

## Этап 2: ANALYSIS

**Выход:** `tasks/{section}/analysis-{section}.md`

**Анализ архитектуры:**
- Data flow: откуда данные, как трансформируются
- Зависимости: store, API, утилиты, компоненты
- API endpoints с request/response shapes
- Risks и recommendations

**Анализ кода:**
- Компоненты с оценкой (good / needs-refactor / rewrite)
- Code smells
- Декомпозиция god-компонентов
- Component API (props interface)

---

## Этап 3: IMPLEMENT

**Выход:** Рабочий код + тесты

**Hard Stop:** перед кодом выполнить:
```
[ ] Прочитал analysis-{section}.md
[ ] Выполнил PRE-ACTION из protocol-development.md
[ ] Таблица тест-кейсов создана (TDD Phase 0)
```

**Порядок:** types → api → hooks → components → pages (последовательно, не параллельно)

**После каждого parent task:**
- `npx tsc --noEmit` — 0 ошибок
- Тесты зелёные
- Task file обновлён `[x]`

---

## Этап 4: REVIEW

**Выход:** `tasks/{section}/review-{section}.md`

**Проверить:**
- Архитектура соответствует analysis
- API типы корректны
- Каждый source file имеет .test file
- Качество тестов (не только "renders")
- Accessibility (aria-labels, keyboard nav)
- Нет security issues (XSS, injection)

**Verdict:** APPROVED / CHANGES REQUESTED

---

## Этап 5: TESTING

**Выход:** `tasks/{section}/testing-{section}.md`

```
[ ] TypeScript: 0 errors
[ ] Tests: all pass
[ ] Coverage: > 70% для новых файлов
[ ] Build: success
[ ] Visual diff: < 1% для каждой затронутой страницы
```

---

## Этап 6: REFLECTION (ключевой этап)

**Выход:** `tasks/{section}/reflection.md` + обновление правил

### 7 вопросов:
1. Что сделано хорошо?
2. Что пошло не так?
3. Что бы сделал по-другому?
4. Какие паттерны повторять?
5. Какие паттерны избегать?
6. Что нужно доработать?
7. Какие правила добавить?

### Обязательные обновления после рефлексии:

```
[ ] reflection.md записана
[ ] tasks/reflection-history.md обновлён
[ ] Lesson о поведении → memory/feedback_*.md
[ ] Lesson о процессе → core-rules.md или WORKFLOW.md
[ ] Предложение по продукту → tasks/improvements.md
[ ] Факт о проекте → RESEARCH.md (если есть)
[ ] Subtasks отмечены [x]
```

**ЗАПРЕЩЕНО** закрывать задачу без обновления хотя бы одного правила/файла из списка выше.

---

## Hard Stop Rules

1. **Нельзя кодить** без `analysis-{section}.md`
2. **Нельзя говорить "готово"** без `review-{section}.md`
3. **Нельзя закрывать задачу** без `reflection.md`
4. **Нельзя говорить "визуально совпадает"** без visual diff < 1%
5. **"Давай дальше" НЕ отменяет pipeline** — предупредить пользователя

---

## Checkpoints между этапами

```
[ ] Этап N завершён? (артефакт создан)
[ ] tsc --noEmit: 0 ошибок?
[ ] Тесты зелёные?
[ ] Task file обновлён?
[ ] Можно переходить? → Да / Нет
```

---

## Lessons Learned (обновляется после каждой рефлексии)

> Сюда записывать конкретные ошибки и исправления.
> Формат: Дата | Раздел | Ошибка | Исправление

| Дата | Ошибка | Исправление |
|------|--------|-------------|
| _пример_ | Pipeline этапы пропущены "для скорости" | Все 6 этапов обязательны, без исключений |
| _пример_ | Visual match оценивался "на глаз" | Automated pixel diff обязателен (< 1%) |
