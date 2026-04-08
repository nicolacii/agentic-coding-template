---
name: techdebt-scan
description: Scan codebase for technical debt — duplicates, large files, code smells, god components. Use BEFORE refactoring to identify what needs cleanup. Outputs prioritized list of debt items with effort estimates.
---

# Skill: TechDebt Scan

> Поиск и документирование технического долга в кодовой базе.
> Запуск: `/techdebt-scan` или "найди техдолг", "проверь качество кода"

---

## Когда вызывать

- В конце сессии или после крупных изменений
- По запросу: "найди дубли", "проверь размеры файлов", "techdebt scan"
- Перед началом рефакторинга — чтобы знать scope

**ВАЖНО: Это READ-ONLY анализ. НЕ исправлять код — только выявлять и документировать!**

---

## Процесс

### Phase 1: SCAN — Сканирование

1. **Размеры файлов** (по лимитам из CLAUDE.md → Code Standards → File Size Limits):
   - Найти все файлы > 300 строк
   - Routes/Components > 200 строк — warning
   ```bash
   find src apps -name "*.ts" -o -name "*.tsx" | xargs wc -l | sort -rn | head -20
   ```

2. **Дублирующийся код:**
   - Semantic search: повторяющиеся паттерны
   - Grep: одинаковые блоки > 10 строк
   - Утилиты в разных местах

3. **Code smells:**
   - Функции > 50 строк
   - Глубокая вложенность > 3 уровней
   - Файлы с > 10 exports
   - Magic numbers/strings
   - `any`, `@ts-ignore`, `console.log`

### Phase 2: ANALYZE — Классификация

Заполнить таблицы для каждой категории:

```markdown
## TECHDEBT SCAN RESULTS — {date}

### 1. Oversized Files
| Файл | Строк | Лимит | Severity | Рекомендация |
|------|-------|-------|----------|--------------|

### 2. Duplicate Code
| Паттерн | Файл 1 | Файл 2 | Строк | Severity | Рекомендация |
|---------|--------|--------|-------|----------|--------------|

### 3. Code Smells
| Тип | Локация | Описание | Severity | Рекомендация |
|-----|---------|----------|----------|--------------|
```

### Phase 3: PRIORITIZE

| Severity | Impact | Effort | Priority |
|----------|--------|--------|----------|
| 🔴 High | Блокирует разработку | Low | P0 — ASAP |
| 🔴 High | Блокирует разработку | High | P1 — планировать |
| 🟡 Medium | Снижает качество | Low | P2 — quick win |
| 🟡 Medium | Снижает качество | High | P3 — backlog |
| 🟢 Low | Косметика | Any | P4 — optional |

### Phase 4: REPORT

```markdown
## TECHDEBT REPORT — {date}

### Summary
| Категория | Найдено | 🔴 | 🟡 | 🟢 |
|-----------|---------|----|----|-----|
| Oversized files | | | | |
| Duplicate code | | | | |
| Code smells | | | | |
| **TOTAL** | | | | |

### Top 5 Issues
1. **[P0]** {path} — {описание} — {рекомендация}
2. ...

### Quick Wins (Low effort, High impact)
- [ ] ...

### Требует планирования
- [ ] ...
```

---

## Запреты

- НЕ исправлять код автоматически (только анализ)
- НЕ пропускать категории сканирования
- НЕ давать абстрактные рекомендации без конкретных файлов
- Для исправления найденного — использовать Refactoring Protocol из CLAUDE.md
