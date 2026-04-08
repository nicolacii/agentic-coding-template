---
name: orchestrate
description: Multi-agent orchestration skill — delegates work to specialized sub-agents via Task tool. Use for COMPLEX (XL) tasks where context preservation is critical. Orchestrator stays minimal, sub-agents do heavy reading/writing in isolated contexts. Required when task involves 10+ legacy files or 5+ implementation layers.
---

# Skill: Multi-Agent Orchestration

> Делегирует работу specialized sub-agents через Task tool.
> Orchestrator никогда не читает большие объёмы кода — только output sub-agents.

---

## Когда использовать

| Задача | Orchestration |
|--------|---------------|
| 🟢 SIMPLE | НЕ использовать (overhead > польза) |
| 🟡 STANDARD | Опционально (если есть глубокий анализ) |
| 🔴 COMPLEX | **Обязательно** (без неё orchestrator забудет начало) |

**Триггеры:**
- Задача требует чтения 10+ файлов legacy кода
- Имплементация в 5+ слоях (types, api, hooks, components, pages)
- Большой scope аудита/анализа
- Параллельные независимые потоки работы

---

## Принципы

1. **Orchestrator не читает legacy код** — только outputs sub-agents
2. **Коммуникация через файлы** — sub-agents не видят чат
3. **Каждый sub-agent — изолированный контекст** — не влияет на orchestrator memory
4. **Brief должен быть точным** — sub-agent не угадает intent
5. **Параллельность где возможно** — analysts, reviewers могут работать параллельно

---

## Workflow

### Шаг 1: Прочитать project-config.yml

```bash
cat .claude/project-config.yml
```

Получить:
- `multi_agent.mode` — none / lightweight / full
- `multi_agent.roles` — список доступных ролей
- `stack.languages` — какие технологии в проекте

Если `multi_agent.enabled: false` → НЕ использовать orchestration, делать всё самостоятельно.

### Шаг 2: Создать orchestrator-brief

```bash
mkdir -p tasks/{section}
```

Создать `tasks/{section}/orchestrator-brief.md` из шаблона:

```markdown
# Orchestrator Brief: {section}

## Goal
{что нужно сделать в одном предложении}

## Context
- Project type: {из project-config.yml}
- Stack: {релевантные языки}
- Reference: {legacy path / figma / production URL}

## Sub-Agents Plan

### Stage 2: Analysis (parallel)
- analyst-architect → analyse architecture
- analyst-fe-senior → analyse code quality
{другие analysts если есть}

### Stage 3: Implementation (sequential)
- developer-types → src/types/{section}.ts
- developer-api → src/api/{section}.ts
- developer-ui → src/features/{section}/

### Stage 4: Review (parallel)
- reviewer-architect
- reviewer-fe-senior

### Stage 5: Testing
- qa → tsc, tests, visual-diff

## Constraints
- {константы из CLAUDE.md проекта}
- {ограничения из задачи}

## Expected Output
- {какие файлы должны появиться}
- {acceptance criteria}
```

### Шаг 3: Spawn analysts (parallel)

Использовать Task tool с несколькими параллельными вызовами:

```
Task(subagent_type="general-purpose", description="Analyze architecture",
     prompt="Read .claude/sub-agents/analyst-architect.md.
             Read tasks/{section}/orchestrator-brief.md.
             Execute the role. Write output to tasks/{section}/analyst-architect.md.
             Return summary in <200 words.")

Task(subagent_type="general-purpose", description="Analyze UI quality",
     prompt="Read .claude/sub-agents/analyst-fe-senior.md.
             Read tasks/{section}/orchestrator-brief.md.
             Execute the role. Write output to tasks/{section}/analyst-fe-senior.md.
             Return summary in <200 words.")
```

Важно: оба Task вызова в **одном message** для параллельности.

### Шаг 4: Aggregate analysis

После завершения обоих analysts:
1. Прочитать `tasks/{section}/analyst-architect.md`
2. Прочитать `tasks/{section}/analyst-fe-senior.md`
3. Создать `tasks/{section}/implementation-plan.md` с агрегированным планом

### Шаг 5: Spawn developers (sequential)

Sequential потому что слои зависят друг от друга: types → api → hooks → ui.

```
Task(subagent_type="general-purpose", description="Implement types",
     prompt="Read .claude/sub-agents/developer-types.md.
             Read tasks/{section}/implementation-plan.md.
             Execute. Write output to tasks/{section}/developer-types-output.md.")
```

После завершения — spawn developer-api, передав output predecessor:

```
Task(prompt="...
            Previous step output: tasks/{section}/developer-types-output.md
            Read it before starting.")
```

### Шаг 6: Spawn reviewers (parallel)

Аналогично analysts — два reviewer в параллель.

### Шаг 7: Spawn QA

QA запускает тесты, visual-diff, build:

```
Task(subagent_type="general-purpose", description="Run QA",
     prompt="Read .claude/sub-agents/qa.md.
             Run tsc --noEmit, vitest run, vite build.
             If CSS changed: run python3 scripts/visual-diff.py {page}.
             Write results to tasks/{section}/qa-results.md.")
```

### Шаг 8: Reflection (orchestrator делает САМ)

Reflection требует памяти всех этапов — не делегируется. Orchestrator читает все outputs и пишет `tasks/{section}/reflection.md`.

---

## Анти-паттерны

❌ Делегировать reflection — orchestrator должен помнить весь цикл
❌ Sub-agent читает чат — он его не видит
❌ Длинный prompt без brief файла — sub-agent не запомнит детали
❌ Параллельный запуск зависимых developers (types → api нельзя параллельно)
❌ Orchestrator читает 50+ файлов legacy — для этого есть analyst sub-agent

---

## Оптимизация контекста

**Orchestrator должен оставаться "тонким":**
- Читает только: project-config, brief templates, sub-agent outputs (summaries), reflection
- НЕ читает: legacy код, исходники компонентов, тесты, документацию (это работа sub-agents)

**Если orchestrator контекст превышает 50K токенов** → задача слишком сложная, нужно разбить на несколько pipeline циклов.

---

## Lightweight Mode

Если `multi_agent.mode: lightweight` — использовать только 3 sub-agents:
- `analyst` (один универсальный анализ)
- `developer` (один универсальный разработчик)
- `qa` (тестирование)

Для маленьких задач этого достаточно.

---

## Fallback

Если sub-agent не справился (ошибка, неполный output) → orchestrator может:
1. Перезапустить sub-agent с уточнённым brief
2. Сделать работу самостоятельно (если контекст позволяет)
3. Запросить помощь у пользователя
