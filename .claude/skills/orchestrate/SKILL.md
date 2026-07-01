---
name: orchestrate
user-invocable: true
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

---

## Circuit Breaker (валидировано task 10.0 Billing, 2026-04-08)

После ЛЮБОГО отказа sub-agent (529, error, timeout, partial output):

1. **Проверить артефакты.** Если ≥ 50% ожидаемых файлов созданы → orchestrator доделывает остаток в-context (fallback mode). СТОП retry.
2. Если < 50% создано → ОДИН retry с тем же brief.
3. Если retry тоже падает → переключить model на Sonnet → ОДИН ещё retry.
4. Если опять падает → orchestrator делает работу в-context. Документировать в output файле как "Completed via fallback after N sub-agent failures".

**ЗАПРЕЩЕНО:**
- Retry слепо больше 2 раз
- Переключать model на первой ошибке (может быть transient)
- Молча скипать — всегда документировать fallback в output файле этапа

**Эмпирика task 10.0:** Opus developer-api упал 3 раза подряд с 529 (41 сек / 152 сек / partial 40%). Третья попытка дала 40% артефактов — orchestrator доделал остаток за 3 минуты в context, результат неотличим от sub-agent output по стилю. Ретроспективно правильный путь был "1 retry → fallback после 2-х падений", сэкономили бы ~5 минут.

---

## Health Checks during background sub-agent runs

Для любого sub-agent с ожидаемым временем > 3 минут:

1. **После spawn:** запомнить agent ID и путь к expected output файлу
2. **Каждые 2-3 минуты** проверять прогресс через:
   - `ls -la <expected-artifact>` (proxy для "что-то происходит?")
   - `tail -c 4000 <agent-stream-file> | grep -oE '"name":"[^"]+"|"command":"...'` (последние tool calls)
3. **Reporting в чат** одной строкой: "Stage X / 7 — agent created Y files, last action: Z, elapsed: T min"
4. **Если 3+ минуты zero progress** → likely hung. Сообщить пользователю. Предложить kill+retry vs continue waiting.

**ЗАПРЕЩЕНО:** fire-and-forget на длинном sub-agent без report'а прогресса. Молчание = плохой UX, пользователь не понимает идёт ли работа или зависло.

**Эмпирика:** на task 10.0 пользователь явно жаловался на silence. Внедрено мid-run, применено к последующим sub-agents. Сэкономило раздражение.

---

## Model Selection для sub-agents

| Sub-agent role | Model | Когда |
|----------------|-------|-------|
| analyst-* | **Opus** | Глубокий анализ, ambiguous decisions |
| developer-types | **Sonnet** | Mechanical type porting |
| developer-api (типовые) | **Sonnet** | Established patterns |
| developer-ui (large) | **Sonnet** | Эмпирически 2-4× быстрее, 0 vs 4 errors |
| developer-* (novel arch) | **Opus** | State design, новые паттерны |
| reviewer-* | **Sonnet** | Rule checking |
| qa | **Sonnet** | Running checks |

**Эмпирика task 10.0 Billing:**
- Opus: 9 мин analyst, 3 ЧАСА developer-ui, 4× API 529 errors
- Sonnet: 4-5 мин reviewer, 2.7 мин qa, 0× API 529 errors

Default — Sonnet. Opus только когда нужна глубина рассуждений.

---

## QA sub-agent — Bash requirement

QA role фундаментально требует shell access (`tsc --noEmit`, `vitest run`, `vite build`, `python3 visual-diff.py`). Если sub-agent sandbox блокирует Bash:
1. QA должен явно declare этот failure в output
2. Orchestrator обязан re-run static checks сам (быстро, ~30 сек)
3. Update qa.md role file: "MUST verify Bash availability in setup, fail loudly if not"

---

## Durable Progress — ledger переживает compaction

> Источник: Superpowers `subagent-driven-development`. Память чата НЕ переживает compaction. В реальных
> сессиях orchestrator, потерявший место, переспавнивал уже готовые задачи — самый дорогой из
> наблюдавшихся провалов.

- В начале orchestration проверь ledger: `cat tasks/{section}/progress-ledger.md`. Задачи, помеченные
  там complete — **ГОТОВЫ, не переспавнивать**; продолжай с первой непомеченной.
- Когда ревью задачи вернулось чистым — допиши строку: `Task N: complete (files X,Y, review clean)`.
- Ledger — карта восстановления: файлы, которые он называет, существуют в git даже когда контекст уже
  не помнит их создания. После compaction доверяй ledger + `ls`/`git log`, а не своей памяти.

## File Handoffs — артефакты файлами, не paste-ом в контекст

Всё, что ты вставляешь в prompt субагента, и всё, что он печатает назад — остаётся в твоём контексте
до конца сессии и перечитывается на каждом ходу. Передавай файлами:
- **Task brief:** каждой задаче — свой brief-файл (её требования, точные значения verbatim), а не весь план.
- **Report file:** субагент пишет полный отчёт в файл, возвращает только статус + коммиты + 1 строку теста + concerns.
- **Reviewer inputs:** ревьюеру — пути (brief + report + diff), плюс global constraints, что связывают задачу.
- ❌ Не вставляй накопленную историю прошлых задач («состояние после Tasks 1-3») в поздние dispatch —
  свежему субагенту нужны его задача, интерфейсы, что он трогает, и constraints. Больше ничего.

## Не pre-judge findings ревьюеру

- ❌ Никогда не инструктируй ревьюера «не флагай X», «трактуй как Minor максимум», «план так решил».
  Если считаешь, что finding = ложное срабатывание — дай ревьюеру его поднять, разбери в review-цикле.
  Формулировки «do not flag / at most Minor / план выбрал» в твоём prompt = ты pre-judge, обычно чтобы
  сэкономить себе цикл ревью. Пример-код из плана — стартовая точка, не доказательство, что его слабости выбраны.
- Finding, помеченный plan-mandated (или конфликтующий с тем, что требует текст плана) = **решение
  пользователя**, как любое противоречие плана: покажи finding + текст плана, спроси что главнее.
- Critical/Important findings → fix-субагент. Minor → в ledger, финальный whole-branch review триажит.

## Model selection по сложности задачи (дополнение к таблице ролей)

Явно указывай model при dispatch (пропуск наследует твою — часто самую дорогую). Сигналы:
1-2 файла + полная спека → дешёвая; несколько файлов + интеграция → стандартная; дизайн-суждение /
широкое понимание кодовой базы → самая мощная. Финальный whole-branch review — на самой мощной.

## Parallel fan-out для независимых проблем (ad-hoc)

> Источник: Superpowers `dispatching-parallel-agents`. Отдельно от pipeline-оркестрации: когда есть
> N **независимых** провалов (разные тест-файлы, подсистемы, баги без общего состояния) — один
> агент на проблемный домен, все dispatch в ОДНОМ message (= параллельно).

Хороший prompt субагента: **focused** (один домен) · **self-contained** (весь контекст: имена тестов,
тексты ошибок) · **constraints** («не меняй production-код» / «только тесты») · **specific output**
(«верни summary: root cause + что изменил»). НЕ использовать когда провалы связаны (фикс одного чинит
другие), нужен полный контекст системы, или агенты будут править одни файлы (shared state). После
возврата: прочитать summaries → проверить на конфликты правок → прогнать полный suite.

## Cross-ref
- План для субагентов пиши по `/writing-plans` (Global Constraints + Consumes/Produces + No Placeholders).
- Ревьюер и реакция на его findings — `/review` + `/receiving-review`.
- Финальное завершение ветки — Stage 7 в WORKFLOW.md (4 опции + typed-confirm на discard).
