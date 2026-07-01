---
name: protocol-bugfix
user-invocable: true
description: Protocol for bug fixing. Triggers on keywords ошибка, баг, не работает, падает, error, broken, fix, bug, crash. Use when investigating any error or unexpected behavior. Enforces Fix Root Cause not Symptom via 5 Whys analysis.
---

# Protocol: Bugfix

## Context

- **Когда:** Ошибки, баги, exceptions, неожиданное поведение
- **Ключевые слова:** ошибка, баг, не работает, падает, error
- **Принцип:** FIX ROOT CAUSE, NOT SYMPTOM

---

## Requirements

### Workflow

**REQUIRED:**
1. STOP → Остановись при ошибке
2. CAPTURE → Зафиксируй всю информацию
3. ANALYZE → 5 Whys до root cause
4. FIX → Минимальный патч для root cause
5. VERIFY → Убедись что исправлено
6. PREVENT → Добавь защиту от повторения
7. LEARN → Вызвать `/error-learning` (gap analysis + запись в experience.md)

### Error Capture Template

```markdown
## ERROR CAPTURED

**Command:** [что вызвало ошибку]
**Error Output:**
```
[ПОЛНЫЙ вывод, не сокращать]
```
**Context:** File: [файл], Action: [что делал]
```

### Root Cause Analysis (5 Whys)

```markdown
### Problem: [symptom]

**Why 1:** [ответ]
↓
**Why 5:** [ROOT CAUSE]

### Root Cause: [формулировка]
### Fix: [минимальное исправление]
```

### Common Error Patterns

| Error Type | Root Cause | Fix |
|------------|------------|-----|
| `ModuleNotFoundError` | Не в .venv / missing package | `pip install` + requirements |
| `TypeError` | Wrong data type assumption | Check actual types |
| `500 Error` | Unhandled exception | Add error handling |
| `Connection refused` | Service not running | Start service |

---

## Examples

GOOD: 5 Whys до root cause
```markdown
### Problem: API 500 error

**Why 1:** Exception в endpoint
↓
**Why 2:** Query не выполняется
↓
**Why 3:** Connection pool исчерпан
↓
**Why 4:** Connections не закрываются
↓
**Why 5:** Нет finally блока

### Root Cause: Отсутствует cleanup
### Fix: finally { connection.close() }
```

BAD: Fix симптома
```
Добавлю try/except чтобы не падало.
```
Проблема: Скрывает ошибку, не исправляет причину.

---

## Critical Points

**CRITICAL:**
- MINIMAL FIX — только то что устраняет root cause
- ONE CHANGE AT A TIME — не несколько исправлений сразу
- TEST AFTER FIX — запусти ту же команду
- NO WORKAROUNDS — если необходим, документируй

### Anti-patterns

- try/except чтобы скрыть ошибку
- Workaround без документации
- Несколько fix-ов одновременно
- Игнорирование recurring errors

---

# Systematic Debugging (усиление RCA)

> Дополняет 5 Whys техниками из Superpowers `systematic-debugging`.
> **Iron Law:** `NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST`. Не прошёл Phase 1 — не имеешь права предлагать фиксы.

## Evidence gathering в multi-component системах

Когда система из нескольких компонентов (CI → build → sign, API → service → DB) — ПЕРЕД фиксами добавь
диагностику на КАЖДОЙ границе компонентов, чтобы увидеть, ГДЕ ломается, а не гадать:
```
Для каждой границы: залогируй что входит / что выходит / propagation env/config / состояние слоя.
Прогони один раз → покажет, какой слой падает (secrets→workflow ✓, workflow→build ✗) → копай туда.
```

## Root-cause tracing (backward)
Ошибка глубоко в стеке? Трассируй НАЗАД: где зародилось плохое значение? Кто вызвал с плохим значением?
Веди вверх до источника. **Фикси в источнике, не в симптоме.**

## 🔴 3+ фикса провалились → question the architecture (эскалация)

Если фикс не сработал: посчитай попытки. **< 3** — вернись к Phase 1, переанализируй с новой информацией.
**≥ 3 — СТОП, НЕ пробуй фикс #4.** Паттерн (каждый фикс вскрывает новую связанность в другом месте /
требует «массивного рефакторинга» / плодит симптомы) = **это не провал гипотезы, это неверная
архитектура.** Вынести пользователю: паттерн фундаментально верен? Не держимся ли по инерции?
Рефакторить архитектуру vs дальше чинить симптомы? (Согласуется с Escalation Rules: «ошибка 3+ раз → STOP».)

## Rationalization table (debugging)
| Отмазка | Реальность |
|--------|-----------|
| «Простая проблема, процесс не нужен» | У простых багов тоже есть root cause. Процесс быстр для простых. |
| «Аврал, нет времени на процесс» | Систематика БЫСТРЕЕ, чем метод тыка. |
| «Сначала попробую вот это, потом разберусь» | Первый фикс задаёт паттерн. Делай правильно сразу. |
| «Несколько фиксов сразу — сэкономлю» | Нельзя изолировать что сработало. Плодит новые баги. |
| «Вижу проблему, сейчас исправлю» | Видеть симптом ≠ понимать root cause. |
| «Ещё одна попытка» (после 2+) | 3+ провала = архитектурная проблема, не фикси снова. |

## Red Flags — STOP, вернись к Phase 1
«Быстрый фикс сейчас, разберусь потом» · «просто поменяю X и посмотрю» · «пропущу тест, проверю руками» ·
«наверное это X, сейчас поправлю» · предлагаю решения до трассировки данных · «ещё одна попытка» (уже 2+) ·
каждый фикс вскрывает новую проблему в другом месте.

**Сигналы пользователя, что делаешь не так:** «Stop guessing» · «это вообще происходит?» · «мы застряли?»
(раздражённо) · «ultra-think это». → STOP, вернись к Phase 1.

---

# Error Learning

## Error Learning Context

- **Когда:** После RCA, bugfix, freeze recovery, неожиданного поведения
- **Цель:** Learn from mistakes, предотвратить повторения
- **Output:** Запись в error-log + improvements-backlog

---

## When to Apply

| Событие | Применять? |
|---------|-----------|
| После RCA | ОБЯЗАТЕЛЬНО |
| После bugfix | ОБЯЗАТЕЛЬНО |
| После freeze recovery | ОБЯЗАТЕЛЬНО |
| После 2+ неудачных попыток | ДА |

### Error Recording Template

**REQUIRED:**
Записать в error-log:

```markdown
## ERROR #N: [дата]

### Symptom:
[что произошло]

### Root Cause:
[почему произошло]

### Fix:
[как исправили]

### Prevention:
[как предотвратить]

### Design Injection:
[что добавить в инструкции]
```

### Gap Analysis

```markdown
## GAP ANALYSIS

### Какая инструкция должна была предотвратить?
[файл правил]

### Почему не предотвратила?
- [ ] Инструкция отсутствует
- [ ] Инструкция неполная
- [ ] Инструкция проигнорирована

### Что добавить?
[конкретное правило или шаг]
```

### Improvement Format

```markdown
## IMPROVEMENT #N: [дата] — [название]

**Источник:** [из какой ошибки]
**Проблема:** [что пошло не так]
**Root Cause:** [почему]
**Предложение:** [что добавить]
**Файл:** [какой файл правил изменить]
**Приоритет:** HIGH/MEDIUM/LOW
**Статус:** Backlog
```

---

## Error Learning Examples

GOOD: Полный error learning
```markdown
## ERROR #5: 2026-01-10

### Symptom:
UI не обновился после build

### Root Cause:
Production сервис не перезапущен

### Fix:
systemctl restart frontend

### Design Injection:
Добавить в protocol-development.md:
"Production Deployment = проверить что изменения видны"
```

---

## Error Learning Critical Points

**CRITICAL:**
- КАЖДАЯ ошибка = запись в error-log
- Найти GAP в инструкциях
- Добавить Improvement в backlog
- Периодически внедрять improvements в правила

---

**Версия:** 1.1 (bugfix) + 1.1 (error-learning)
**Связанные модули:** `base-verification.md`, `protocol-development.md`
