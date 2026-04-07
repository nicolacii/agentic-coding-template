# Protocol: Development

## Context

- **Когда:** Новая функциональность, фичи, доработки
- **Ключевые слова:** добавить, создать, новая фича, разработать
- **Базовые модули:** `base-verification.md`
- **Стандарты:** `.claude/rules/` (file size limits, QA)

**CRITICAL:**
- ПРАВИЛО #1: Прочитай ВСЮ инструкцию ПЕРЕД ответом
- ПРАВИЛО #2: Каждый ответ ДОЛЖЕН содержать RESPONSE FORMAT
- ПРАВИЛО #3: НЕ ПРОПУСКАЙ шаги — если пропустил, СТОП и вернись
- ПРАВИЛО #4: После выполнения каждого шага напиши коротко какой output сформировал от этого шага как самопроверка, что ты его не пропустил
- ПРАВИЛО #5: Убедись что нужные сервисы Backend и Frontend перезапущены после выполнения плана доработки.
- ПРАВИЛО #6: Проектируя логику и изменения в архитектуре изучи и соблюдай стандарт размера файлов (см. CLAUDE.md — File Size Limits)

---

## Requirements

### Step 1: PRE-ACTION

**REQUIRED:**
1. **Duplicate Check** — искать существующее перед созданием
2. **JTBD Analysis** — определить Job пользователя
3. **Find Working Example** — для UI найти паттерн в проекте
4. **Control File Size** — формирование логики исходя из правила, что всю логику не складывать в один файл

#### Duplicate Check Template

```markdown
## DUPLICATE CHECK
**Target:** [что создаю]
**Search:** semantic/grep/file → [found/not found]
**Decision:** CREATE NEW / EXTEND EXISTING / ASK USER
```

#### JTBD Analysis Template

```markdown
## JTBD ANALYSIS
**Job Story:** Когда пользователь делает [контекст_задачи], пользователь хочет [действие], чтобы получить [результат] и [выгода]
**3 вопроса:**
1. Какую задачу он решает? → [ответ]
2. Что мешает? → [ответ]
3. Какая доработка поможет получить ему результат? → [ответ]
```

### Step 2: PLAN

```markdown
## DEVELOPMENT PLAN
**Task:** [что сделать]
**Expected Output:** [артефакты]
**Test Cases:** [input → expected output]
```

### Step 3: EXECUTE (TDD)

**REQUIRED:**
1. Написать тест-кейсы (должны ПАДАТЬ)
2. Написать минимальный код для прохождения
3. Запустить тесты (должны пройти)
4. Рефакторинг при необходимости
5. Перезапустить сервисы в которые вносились изменения и проверить работоспособность

### Step 4: VERIFY

```markdown
## VERIFICATION
- [ ] 0 linter errors
- [ ] Tests pass
- [ ] JTBD: Job реализована, UI про выгоды
- [ ] Each file opened and verified
```

---

## Common Pitfalls (универсальные)

### UI Components

**CRITICAL:**
- НАЙДИ работающий пример в проекте → скопируй паттерн
- НЕ используй CSS-классы без проверки что они работают в текущем стеке
- WHY: Responsive классы могут не работать в разных версиях CSS-фреймворков

### Type Consistency (API Integration)

**CRITICAL:**
- Database types могут отличаться от JSON types (bigint → string)
- Map/Set требуют EXACT type match
- WHY: Баги из-за type mismatch (id: string vs number)

### Backend Module Creation (общий паттерн)

```
1. types → 2. repository/data-access → 3. service/business-logic → 4. routes/controllers
```

### External API Integration

**CRITICAL:**
- Поля типа "Список"/"Enum" могут содержать ID, не текст
- Нужен маппинг ID → текст
- WHY: Поле содержало ID вместо читаемого значения

### Entry Point Flow

**CRITICAL:**
- Используй ВЫСОКОУРОВНЕВЫЙ сервис (orchestrator)
- НЕ низкоуровневые методы напрямую
- WHY: Scheduled task может синхронизировать данные, но пропустить агрегацию

---

## Examples

GOOD: Полный flow с JTBD
```markdown
## DUPLICATE CHECK
Target: DateFilter компонент
Search: grep → not found
Decision: CREATE NEW

## JTBD ANALYSIS
Job Story: Когда пользователь ищет сделки за период, пользователь хочет выбрать даты в интерфейсе, чтобы увидеть релевантные данные и сделать нужные выводы
1. Какую задачу он решает? → Найти и проанализировать записи за период
2. Что мешает? → Нет фильтра
3. Какая доработка поможет получить ему результат? → Реализовать и проверить функционал, который позволит получить нужные записи за период за 3 клика

[Реализация...]
```

BAD: Без проверок
```
Создаю компонент DateFilter...
```
Проблема: Может уже существовать, не понятен Job.

---

## Critical Points

**CRITICAL:**
- DUPLICATE CHECK перед ЛЮБЫМ созданием
- JTBD ANALYSIS для user-facing фич
- FIND WORKING EXAMPLE для UI
- Production deployment = проверить что изменения видны
- Check Service Restart = проверить что нужные сервисы, в которые вносились изменения перезапущены и работают без ошибок

---

# TDD — Test-Driven Development

## TDD Context

- **Когда:** Development новых фич, Refactoring существующего кода, Bugfix
- **Принцип:** Red → Green → Refactor (СТРОГО по порядку!)
- **Связь:** Этот стандарт является частью протокола разработки

**CRITICAL:**
СТОП! Этот стандарт ОБЯЗАТЕЛЕН когда активирован.
НЕ ПРОПУСКАТЬ шаги! НЕ писать код без failing tests!
Каждый шаг имеет CHECKPOINT — выполнить ВСЕ до перехода к следующему.

---

## TDD Requirements

### PHASE 0: TEST PLANNING (ОБЯЗАТЕЛЬНО ПЕРВЫЙ ШАГ)

**REQUIRED:**
**CHECKPOINT 0.1** — Перед ЛЮБЫМ кодом заполнить таблицу тест-кейсов:

```markdown
## TEST CASES (заполнить ПЕРЕД реализацией!)

| # | Сценарий | Input | Expected Output | Тип | Status |
|---|----------|-------|-----------------|-----|--------|
| 1 | Happy path | <input> | <expected> | Unit | ⏳ |
| 2 | Edge case: empty | [] | <expected> | Unit | ⏳ |
| 3 | Edge case: null | null | Error | Unit | ⏳ |
| 4 | Integration | <context> | <expected> | Integration | ⏳ |
```

**CHECKPOINT 0.2** — Убедиться что покрыты ВСЕ категории:
- [ ] Happy path (основной сценарий)
- [ ] Edge cases (пустые данные, границы, null/undefined)
- [ ] Error cases (невалидный input, exceptions)
- [ ] Integration points (если есть зависимости)

СТОП: НЕ переходить к Phase 1 пока таблица не заполнена!

---

### PHASE 1: RED — Написать Failing Tests

**REQUIRED:**
**CHECKPOINT 1.1** — Создать тестовый файл:
```typescript
// <feature>.test.ts или <feature>.spec.ts
describe('<Feature>', () => {
  // Тесты для КАЖДОГО кейса из таблицы
});
```

**CHECKPOINT 1.2** — Написать тесты для ВСЕХ кейсов из таблицы Phase 0

**CHECKPOINT 1.3** — Запустить тесты и УБЕДИТЬСЯ что они ПАДАЮТ:
```bash
npm test -- --grep "<feature>"
# Ожидаемый результат: FAIL (тесты должны падать!)
```

**CHECKPOINT 1.4** — Обновить таблицу статусами:
| Status | Значение |
|--------|----------|
| ⏳ | Ожидает написания |
| 🔴 | Test written, FAILING (правильно!) |
| 🟢 | Test PASSING |
| ⏭️ | Skipped (обосновать!) |

СТОП: НЕ писать implementation code пока тесты не написаны И не падают!

---

### PHASE 2: GREEN — Минимальный код для прохождения

**REQUIRED:**
**CHECKPOINT 2.1** — Написать МИНИМАЛЬНЫЙ код чтобы тест прошёл
- НЕ оптимизировать
- НЕ добавлять "на будущее"
- ТОЛЬКО то что нужно для прохождения теста

**CHECKPOINT 2.2** — Запустить тест:
```bash
npm test -- --grep "<feature>"
# Ожидаемый результат: PASS
```

**CHECKPOINT 2.3** — Обновить статус в таблице: 🔴 → 🟢

**CHECKPOINT 2.4** — Повторить для КАЖДОГО теста из таблицы

СТОП: НЕ рефакторить пока ВСЕ тесты не зелёные!

---

### PHASE 3: REFACTOR — Улучшение кода

**REQUIRED:**
**CHECKPOINT 3.1** — ВСЕ тесты зелёные?
- [ ] Да → можно рефакторить
- [ ] Нет → вернуться к Phase 2

**CHECKPOINT 3.2** — Рефакторинг:
- Убрать дублирование
- Улучшить читаемость
- Оптимизировать (если нужно)

**CHECKPOINT 3.3** — После КАЖДОГО изменения:
```bash
npm test
# Все тесты должны оставаться зелёными
```

**CHECKPOINT 3.4** — Финальная проверка:
- [ ] Все тесты проходят
- [ ] Код чистый
- [ ] Нет TODO/FIXME без причины

---

### PHASE 4: VERIFY — Финальная верификация

**REQUIRED:**
Заполнить финальный отчёт:

```markdown
## TDD VERIFICATION

### Test Coverage Summary
| Категория | Написано | Passing | Skipped |
|-----------|----------|---------|---------|
| Happy path | X | X | 0 |
| Edge cases | X | X | 0 |
| Error cases | X | X | 0 |
| Integration | X | X | 0 |
| **TOTAL** | X | X | 0 |

### Test Commands
```bash
npm test -- --coverage
```

### Результат
- [ ] Все тесты проходят
- [ ] Coverage > 80% для нового кода
- [ ] Нет skipped тестов без обоснования
```

---

## TDD Examples

GOOD: Полный TDD цикл с чекпоинтами

```markdown
## TEST CASES для calculateDiscount()

| # | Сценарий | Input | Expected | Тип | Status |
|---|----------|-------|----------|-----|--------|
| 1 | 10% скидка | (100, 10) | 90 | Unit | 🟢 |
| 2 | Нет скидки | (100, 0) | 100 | Unit | 🟢 |
| 3 | 100% скидка | (100, 100) | 0 | Unit | 🟢 |
| 4 | Отрицательная цена | (-50, 10) | Error | Unit | 🟢 |
| 5 | Скидка > 100% | (100, 150) | Error | Unit | 🟢 |

## Phase 1: RED
// calculateDiscount.test.ts
describe('calculateDiscount', () => {
  it('applies 10% discount correctly', () => {
    expect(calculateDiscount(100, 10)).toBe(90);
  });
  // ... остальные тесты
});
// Результат: FAIL (calculateDiscount is not defined)

## Phase 2: GREEN
function calculateDiscount(price: number, percent: number): number {
  if (price < 0) throw new Error('Price cannot be negative');
  if (percent < 0 || percent > 100) throw new Error('Invalid discount');
  return price * (1 - percent / 100);
}
// Результат: PASS

## Phase 3: REFACTOR
// Код уже чистый, рефакторинг не нужен

## TDD VERIFICATION
- Все 5 тестов проходят
- Coverage: 100%
- Skipped: 0
```

BAD: Код БЕЗ тестов

```typescript
// НЕПРАВИЛЬНО: сразу пишет код
function calculateDiscount(price, percent) {
  return price * (1 - percent / 100);
}
// "Потом напишу тесты"
```
Проблема: Нарушен TDD — код написан БЕЗ failing tests.
Edge cases (negative price, invalid percent) не обработаны.

BAD: Тесты после кода

```
1. Написал функцию calculateDiscount
2. Функция работает
3. Теперь напишу тесты чтобы "покрыть"
```
Проблема: Это не TDD, это "test-after".
Тесты будут подстраиваться под код, а не код под требования.

BAD: Пропуск Phase 0

```
"Понятно что нужно сделать, сразу напишу тест"
test('it works', () => {
  expect(myFunction()).toBeTruthy();
});
```
Проблема: Нет таблицы тест-кейсов → пропущены edge cases → баги в production.

---

## TDD Critical Points

**CRITICAL:**
### ОБЯЗАТЕЛЬНЫЙ ПОРЯДОК (НЕ МЕНЯТЬ!):
1. **PHASE 0**: Таблица тест-кейсов → CHECKPOINT
2. **PHASE 1**: Failing tests → CHECKPOINT (тесты ДОЛЖНЫ падать!)
3. **PHASE 2**: Minimal code → CHECKPOINT (тесты проходят)
4. **PHASE 3**: Refactor → CHECKPOINT (тесты всё ещё проходят)
5. **PHASE 4**: Verify → финальный отчёт

### ЗАПРЕЩЕНО:
- Писать код ДО таблицы тест-кейсов
- Писать код ДО failing tests
- Рефакторить с красными тестами
- Пропускать checkpoints
- "Потом допишу тесты"

### ЕСЛИ НАРУШИЛ:
СТОП → Удалить код → Вернуться к Phase 0 → Начать правильно

---

## TDD Integration

**Инструменты тестирования:**
- Jest / Vitest — unit tests
- Supertest — API tests
- Playwright / Cypress — E2E tests
- Testing Library — React components

---

**Версия:** 2.3 (development) + 2.0 (TDD)
**Связанные модули:** `base-verification.md`, `.claude/rules/`
