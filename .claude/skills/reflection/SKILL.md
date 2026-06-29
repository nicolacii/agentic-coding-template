---
name: reflection
user-invocable: true
description: Pipeline reflection skill — runs after each completed task pipeline. Triggers automatically at stage 6 of WORKFLOW.md. Use after finishing a task with code to capture lessons, update rules, create ADRs, or generate new skills. Self-improvement enforcement: must produce at least 1 artifact (rule update, ADR, new skill, or backlog item).
---

# Skill: Pipeline Reflection

> Этап 6 pipeline. Self-improvement enforcement: рефлексия ОБЯЗАНА создать минимум 1 артефакт.

---

## Когда вызывать

После завершения этапов 1-5 pipeline (Task → Analysis → Implement → Review → Testing).

---

## Процесс

### Шаг 1: Собрать метрики

Прочитать артефакты из `tasks/{section}/`:
- `tasks-{section}.md` — sub-tasks done/total
- `analysis-{section}.md` — что нашли
- `review-{section}.md` — issues, verdict
- `testing-{section}.md` — coverage, visual diff %

```
Раздел: {section}
Файлов создано: N
Тестов: N
Coverage: N%
Review issues: N blocking + N should-fix
Visual diff: N%
Iterations: N
Pipeline violations: N
```

### Шаг 2: 7 вопросов

1. Что сработало хорошо?
2. Что пошло не так?
3. Были ли пропущены этапы? Почему?
4. Качество анализа — нашёл ли реальные проблемы?
5. Качество ревью — нашёл ли реальные баги?
6. Качество тестов — покрыли реальные сценарии?
7. **Что нужно изменить в процессе?** ← обязан указать конкретный артефакт

### Шаг 3: Записать reflection.md

```markdown
# Reflection: {Section}
> Дата: YYYY-MM-DD

## Метрики
{таблица}

## 7 вопросов
{ответы конкретно}

## Action Items (обязательно ≥1)
- [ ] {action} → {target file}

## Self-improvement artifacts created
- [ ] memory/feedback_*.md
- [ ] CLAUDE.md update
- [ ] WORKFLOW.md update
- [ ] docs/adr/ADR-XXX.md (NEW)
- [ ] .claude/skills/{new-skill}.md (NEW)
- [ ] tasks/improvements.md
- [ ] CHANGELOG.md
```

### Шаг 4: ENFORCEMENT — создать минимум 1 артефакт

**Правило:** рефлексия НЕ завершена пока не создан хотя бы один из:

| Артефакт | Когда создавать |
|----------|----------------|
| `memory/feedback_*.md` | Lesson о поведении агента (повторяющаяся ошибка) |
| `CLAUDE.md` update | Lesson о процессе (новое правило) |
| `WORKFLOW.md` update | Изменение pipeline |
| `docs/adr/ADR-XXX.md` | Архитектурное решение принято |
| `.claude/skills/{new}.md` | Паттерн повторился 3+ раз → новый skill |
| `tasks/improvements.md` | Идея для backlog |
| `CHANGELOG.md` | Изменение для пользователя |

**Если задача прошла идеально и нечего улучшать** — добавить запись в `tasks/reflection-history.md` с пометкой `No improvements needed` и обоснованием. Это тоже артефакт.

### Шаг 5: Обновить reflection-history.md

```markdown
| Дата | Раздел | Issues | Iterations | Key lesson | Artifacts created |
|------|--------|--------|------------|-----------| -------------------|
| YYYY-MM-DD | {section} | N | N | {one line} | ADR-XXX, skill-XXX |
```

### Шаг 6: Если паттерн повторился 3+ раз → создать новый skill

Если в reflection-history.md одна и та же ошибка появляется 3+ раз:
1. Создать новый skill в `.claude/skills/{name}.md`
2. Добавить frontmatter с triggers
3. Обновить `CLAUDE.md` — добавить точку вызова
4. Записать в reflection.md что создан новый skill

---

## Правила

- **Честность важнее позитива** — если этап был бесполезен, так и пиши
- **Конкретика важнее абстракций** — "file.tsx:42 не покрыт" > "нужно больше тестов"
- **Каждый вывод → действие** — без действия вывод бесполезен
- **Не дублировать** — если проблема уже зафиксирована, не повторять
- **Self-improvement enforcement** — без минимум 1 артефакта рефлексия НЕ завершена
