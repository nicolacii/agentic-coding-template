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
