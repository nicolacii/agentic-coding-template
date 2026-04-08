---
name: protocol-refactoring
description: Protocol for code refactoring and optimization. Triggers on keywords рефакторинг, улучшить код, оптимизировать, refactor, clean up, extract, split component. Enforces Change Structure Not Behavior — tests MUST exist before refactoring, run after each change.
---

# Protocol: Refactoring

## Context

- **Когда:** Улучшение структуры кода без изменения поведения
- **Ключевые слова:** рефакторинг, улучшить, оптимизировать, упростить
- **Принцип:** CHANGE STRUCTURE, NOT BEHAVIOR

**CRITICAL:**
Если поведение меняется → это НЕ refactoring, это feature/bugfix!

---

## Requirements

### When to Refactor

| Refactor When | Do NOT When |
|---------------|-------------|
| Код работает, но трудно понять | Код ещё не работает |
| Дублированный код | Нет тестов |
| Длинные методы (> 50 строк) | Под давлением времени |
| Глубокая вложенность (> 3 levels) | "Just because" |

### Safety Protocol

**REQUIRED:**
1. Тесты ДОЛЖНЫ существовать перед рефакторингом
2. Тесты ДОЛЖНЫ проходить перед каждым изменением
3. Только маленькие шаги (одно изменение за раз)
4. Запуск тестов ПОСЛЕ каждого изменения
5. Commit ПОСЛЕ каждого успешного шага

### Workflow

```
1. VERIFY   → Все тесты проходят
2. IDENTIFY → Что рефакторить
3. PREPLAN  → Как рефакторить согласно стандарту размера файлов (см. CLAUDE.md — File Size Limits)
3. PLAN     → Маленькие шаги
4. EXECUTE  → Один шаг
5. TEST     → Тесты после шага
6. COMMIT   → Commit если зелёный
7. REPEAT   → Следующий шаг
```

### Common Patterns

| Smell | Refactoring |
|-------|-------------|
| Long Method (> 50 lines) | Extract Method |
| Duplicate Code | Extract Method/Class |
| Long Parameter List (> 4) | Parameter Object |
| Deep Nesting (> 3 levels) | Guard Clauses |
| Magic Numbers | Extract Constant |

---

## Examples

GOOD: Маленькие шаги с тестами
```markdown
### Step 1: Extract validateOrder()
- [ ] Run tests → PASS
- [ ] Commit

### Step 2: Extract calculateTotal()
- [ ] Run tests → PASS
- [ ] Commit

### Step 3: Rename variables
- [ ] Run tests → PASS
- [ ] Commit
```

BAD: Big Bang рефакторинг
```
Переписываю весь модуль заново...
```
Проблема: Нет промежуточных тестов, высокий риск сломать.

BAD: Рефакторинг без тестов
```
Быстренько почищу этот код...
```
Проблема: Без тестов нет гарантии что поведение не изменилось.

---

## Critical Points

**CRITICAL:**
### Golden Rules:
1. TESTS FIRST — нет тестов, нет рефакторинга
2. RULES FIRST — критичное соблюдение правил инструкции по размеру файла (см. CLAUDE.md — File Size Limits)
3. SMALL STEPS — одно изменение за раз
4. TEST OFTEN — после каждого изменения
5. COMMIT OFTEN — после каждого зелёного теста
6. BEHAVIOR UNCHANGED — same inputs → same outputs

### Anti-patterns

- Big Bang: переписать весь модуль за раз
- No Tests: рефакторинг без покрытия тестами
- Mixed Changes: "пока я тут, исправлю ещё баг"
- Premature Abstraction: абстракция для кода используемого 1 раз

---

**Версия:** 1.2
**Связанные модули:** `base-verification.md`, `protocol-development.md` (TDD section)
