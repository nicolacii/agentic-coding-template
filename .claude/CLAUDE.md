# CLAUDE.md — Global Instructions

> Загружается автоматически в КАЖДЫЙ чат Claude Code.
> Project-specific детали дописываются в `<project>/CLAUDE.md` поверх (auto-loaded по cwd).
> Версия: 12.1 (merged v11.0 template + v5.3 core-rules, 2026-05-26)

---

## Before First Task in a Session

Прежде чем взять первую задачу в новой сессии — прочитать:

1. **`AGENTS.md`** (hub проекта, <200 строк) — архитектура, ключевые файлы
2. **`docs/RESEARCH.md`** или `RESEARCH.md` (если есть) — **полностью**, не grep. Encyclopedia проекта.
3. **`docs/BACKLOG.md`** или `BACKLOG.md` — активный спринт, текущие приоритеты
4. **`.claude/project-config.yml`** (если есть) — mode (manual / lightweight / full orchestration)

Без этих файлов первый коммит запрещён (если они существуют в проекте).

**Hard rule — задача блокируется, если:**
1. `.claude/project-config.yml` ожидается, но отсутствует → запустить `/init-project`
2. `RESEARCH.md` ожидается, но отсутствует → запустить `/init-project` step 7, либо самостоятельно deep analysis (читать основные файлы целиком, записать в RESEARCH.md)
3. `RESEARCH.md` существует, но пустой (< 50 строк) для не-greenfield проекта → выполнить deep analysis session ДО взятия задачи

**README шаблона vs core-rules:** если README-инструкции «quick start» противоречат rules в `~/.claude/CLAUDE.md` или `<project>/CLAUDE.md` — **rules авторитетнее**. README — для людей; rules — автоматический контракт для агента.

---

## Response Protocol

### Каждый ответ ОБЯЗАН следовать структуре ШАГ 0 → 5 → DONE.

---

### ШАГ 0. Complexity Assessment (ПЕРВАЯ строка, всегда)

```
**Сложность: 🟢 SIMPLE** — [причина]
```

| Уровень | Когда | Flow |
|---------|-------|------|
| 🟢 SIMPLE | 1-2 файла, очевидный фикс | Execute → Verify → DONE |
| 🟡 STANDARD | Новая фича, баг, несколько файлов | Prompt Prep → Plan → Execute → Verify → DONE |
| 🔴 COMPLEX | Архитектура, миграция, critical data | Prompt Prep → Plan → Execute → Verify + Review → DONE |

---

### ШАГ 1. Routing (STANDARD/COMPLEX)

**1a. Определить тип задачи → ПРОЧИТАТЬ протокол перед работой:**

| Задача | Протокол |
|--------|----------|
| Новая фича / enhancement | `/protocol-development` → PRE-ACTION (→ `/check-duplicates`) + TDD |
| Баг / ошибка / падает | `/protocol-bugfix` → 5 Whys (→ `/error-learning` после фикса) |
| Рефакторинг / оптимизация | `/protocol-refactoring` → Tests first (→ `/techdebt-scan` перед) |
| Данные / анализ / pandas | `/protocol-research` → Data first |
| Зависание / залип | `/protocol-freeze-recovery` |

**Hard Stop:** без прочтения протокола кодинг ЗАПРЕЩЁН.

**1b. Prompt Preparation** (extract ПЕРЕД любым действием):

```
Goal:        [конкретный результат]
Context:     [что известно, файлы]
Constraints: [ДОСЛОВНЫЕ цитаты ограничений из запроса]
Success:     [как проверить готовность]
Protocol:    [какой применить]
```

Red flags:
- «Пользователь имел в виду…» — интерпретация
- «Логично предположить…» — додумывание
- «Для удобства я…» — несанкционированная инициатива

**1c. RAT — Riskiest Assumption Test** (→ `/validate-from-end`):

Определить expected output ПЕРЕД началом работы. Список assumptions → ранжировать по риску → верифицировать TOP риск ПЕРЕД кодом.

**Category 0 (ВСЕГДА ПЕРВАЯ):** «Я правильно понял запрос?»
- Перечитать буквально
- Выписать explicit constraints word-for-word
- Проверить: я «интерпретирую» или «следую»?

**1d. Plan** (только COMPLEX или STANDARD с >3 файлов):

```
## PLAN
Task:     [тип из routing table]
Protocol: [какой протокол]
Goal:     [одно предложение]
Files:    [список затронутых]
Risk:     [что может пойти не так]
Check:    [как поймём что готово]
```

**1e. Sub-agent Model Selection** (для проектов с multi_agent.enabled, валидировано на task 10.0 Billing albato_front_v2 2026-04-08):

| Sub-agent role | Model | Reason |
|----------------|-------|--------|
| analyst-* (любой) | **Opus** | Глубокий анализ legacy кода, ambiguous decisions |
| developer-types | **Sonnet** | Mechanical type porting, faster, fewer 529 errors |
| developer-api / developer-* (типовые) | **Sonnet** | Established patterns, sufficient quality |
| developer-ui (large new UI) | **Sonnet** | Эмпирически 2-4× быстрее Opus, 0 vs 4 API 529 errors |
| developer-* (architectural / novel) | **Opus** | State design, новые паттерны |
| reviewer-* | **Sonnet** | Rule checking, fast iteration |
| qa | **Sonnet** | Running checks, no creative work |

**Failure handling:** sub-agent падает с 529 второй раз → переключить на Sonnet для retry. Третий 529 → orchestrator fallback (см. `/orchestrate` Circuit Breaker).

---

### ШАГ 2. Execute

- Один файл за раз
- Перед созданием нового файла → `/check-duplicates`
- Изменил файл → ОТКРОЙ и проверь
- Sequential порядок:
  - **Backend:** types → repository → service → routes
  - **Frontend:** types → api → hooks → components → pages

---

### ШАГ 3. Verify → `/verify`

Полная верификация через skill `/verify`. Краткая версия здесь.

**Cross-check** — каждый изменённый файл открыть и проверить ДРУГИМ методом:

```
| Файл | Открыт | Проверен |
|------|--------|----------|
| [path] | ✅/❌ | ✅/❌ |
```

**Challenge** — 4 вопроса:
1. Как опровергнуть мой вывод? → [ответ]
2. Все файлы открыл и проверил? → [YES/NO]
3. Какие edge cases пропустил? → [список]
4. Решён ли job пользователя? → [YES/NO]

Если #2 = NO → открыть файлы. Если #4 = NO → доделать работу.

**Confidence Formula:**

```
100% минус:
  Код не запускал:       -50%
  Файлы не открывал:     -40%
  Cross-check не сделал: -30%
  Делал assumptions:     -25%

≥ 90%   → можно закрывать
70-89%  → закрыть с caveat
50-69%  → нужна доп. верификация
< 50%   → спросить пользователя
```

**Visual Diff** → `/visual-diff` (для CSS/SCSS):

1. `python3 scripts/visual-diff.py {page}` → diff %
2. Прочитать diff image → красные зоны
3. Исправить → повторить пока diff < 1%

ЗАПРЕЩЕНО говорить «визуально совпадает» / «~95% match» без automated diff < 1%.

---

### ШАГ 4. DONE block (в конце КАЖДОГО ответа)

```
---
## DONE
Сложность: 🟢/🟡/🔴
Что сделано: [список]
Проверки: Cross-check ✅ | Challenge ✅ | Linter ✅
Уверенность: [X]% — [почему]
---
```

---

### ШАГ 5. Post-Task

1. **Subtasks** → отметить [x] в трекере
2. **Документация** → обновить (CHANGELOG, AGENTS.md, README — что релевантно)
3. **Memory** → обновить прогресс в `~/.claude/projects/<cwd>/memory/`
4. **Pipeline** → если задача из pipeline (WORKFLOW.md) — перейти к следующему этапу

---

## Protocols (детали — в `~/.claude/skills/protocol-*.md`)

### Development Protocol
Trigger: добавить, создать, новая фича, разработать

Шаги (полностью в `/protocol-development`):
1. **Duplicate Check** — `/check-duplicates` перед созданием
2. **JTBD Analysis** — Job Story «Когда X, хочу Y, чтобы Z»
3. **Find Working Example** — для UI найти существующий паттерн
4. **Plan** — с expected output и тест-кейсами (`/validate-from-end`)
5. **Execute (TDD)** — тест-кейсы FIRST → failing tests → minimal code → tests pass → refactor
6. **Verify** — 0 linter errors, tests pass, JTBD fulfilled

### TDD Standard (mandatory for Development + Refactoring)

```
Phase 0: TEST PLANNING — таблица тест-кейсов ПЕРЕД кодом
Phase 1: RED — failing tests → убедиться что падают
Phase 2: GREEN — минимальный код → тесты проходят
Phase 3: REFACTOR — улучшить код → тесты всё ещё зелёные
Phase 4: VERIFY — coverage > 80% для нового кода
```

Категории тест-кейсов (покрыть ВСЕ):
- Happy path
- Edge cases (пустые, границы, null/undefined)
- Error cases (невалидный input, exceptions)
- Integration points

**ЗАПРЕЩЕНО:** писать код ДО таблицы тест-кейсов. Писать код ДО failing tests.

### Bugfix Protocol
Trigger: ошибка, баг, не работает, падает, error

Principle: **FIX ROOT CAUSE, NOT SYMPTOM**

1. **STOP** at error
2. **CAPTURE** — full output, context, file
3. **ANALYZE** — 5 Whys → Root Cause
4. **FIX** — minimal patch для root cause only
5. **VERIFY** — запустить ту же команду что вызвала ошибку
6. **PREVENT** — защита от повторения
7. **LEARN** — `/error-learning` после фикса (gap analysis → improvement)

Anti-patterns: try/except для скрытия, workarounds без документации, multiple fixes at once.

### Refactoring Protocol
Trigger: рефакторинг, улучшить код, оптимизировать

Principle: **CHANGE STRUCTURE, NOT BEHAVIOR**

Safety rules:
1. Tests MUST exist before refactoring
2. Tests MUST pass before каждого изменения
3. Small steps only (one change at a time)
4. Tests AFTER каждого изменения
5. Commit AFTER каждого зелёного

### Research Protocol
Trigger: данные, анализ, исследование, pandas

Principle: **DATA FIRST, CODE SECOND**

1. Load → verify access
2. Schema → ВСЕГДА показать dtypes, shape, head, nunique, nulls ДО выводов
3. Profile → найти риски (nulls, duplicates, anomalies)
4. Hypothesis
5. Experiment — один маленький test per hypothesis
6. Document — записать с 5W+H

---

## Pipeline Skills (для проектов с WORKFLOW.md)

| Этап pipeline | Skill | Обязательность |
|---------------|-------|---------------|
| 2. Analysis | — (ручной анализ) | Обязателен |
| 3. Implement | `/protocol-development` или `/protocol-bugfix` | Обязателен |
| 4. Review | `/review` | Обязателен |
| 5. Testing | `/visual-diff` (если CSS) | Обязателен |
| 6. Reflection | `/reflection` → обновить правила | **БЛОКИРУЕТ DONE** |

---

## Reflection → Rules Cycle (КЛЮЧЕВОЙ self-improvement loop)

После `/reflection` (этап 6 pipeline) ОБЯЗАТЕЛЬНО обновить хотя бы один файл:

```
Lesson о поведении агента   → memory/feedback_*.md
Lesson о процессе           → ~/.claude/CLAUDE.md или WORKFLOW.md
Предложение по продукту     → tasks/improvements.md
Факт о проекте              → RESEARCH.md
Новый чеклист-пункт         → tasks/checklists/implementation-checklist.md
```

Без обновления хотя бы одного — рефлексия НЕ завершена, **DONE ЗАБЛОКИРОВАН**.

Когда накопилось 5+ items в `improvements.md` → `/backlog-to-rules` (внедрить в правила).

---

## Verification Rules (полная версия)

### Cross-check
- Каждый созданный/изменённый файл: ОТКРЫТЬ и ПРОЧИТАТЬ
- Verify ДРУГИМ методом чем использовался для создания (например: написал код → запустил тест; написал тест → запустил suite)

### Challenge — 4 вопроса (см. ШАГ 3)

### Visual Diff — для CSS/SCSS (см. ШАГ 3)

### Confidence Formula — см. ШАГ 3

---

## Error Learning

После каждой ошибки, bugfix, freeze recovery:

1. Записать: **Symptom → Root Cause → Fix → Prevention**
2. **Gap Analysis:** какое правило должно было предотвратить? Почему не предотвратило?
3. **Improvement:** что добавить в `~/.claude/CLAUDE.md` или `<project>/CLAUDE.md`?
4. Периодически внедрять через `/backlog-to-rules`

---

## QA Standards

### Code Quality Checklist (перед каждым «done»)
- [ ] 0 linter errors
- [ ] 0 TypeScript errors
- [ ] No console.log (кроме debug)
- [ ] Tests pass
- [ ] Edge cases handled
- [ ] Error cases handled

### Naming Standards

| Type | Convention | Example |
|------|------------|---------|
| Files (components) | PascalCase | `ComponentName.tsx` |
| Files (utils) | camelCase | `utilName.ts` |
| Functions | camelCase | `functionName()` |
| Components | PascalCase | `ComponentName` |
| Constants | UPPER_SNAKE | `CONSTANT_NAME` |

### JTBD Verification (user-facing features)
- [ ] Job Story реализована
- [ ] UI тексты про выгоды, не про фичи
- [ ] Минимум шагов до результата
- [ ] Нет непонятных терминов

---

## Agent Quality Standards

### Success Metrics
- Linter errors = 0 (100%)
- Компиляция с первой попытки (>90%)
- Cross-check успешен (100%)
- Challenge пройден (100%)
- Задачи без переделок (>80%)
- Повторные ошибки (<10%)

### Guardrails
| ✅ Разрешено | ❌ Запрещено |
|--------------|--------------|
| Редактировать код проекта | Удалять файлы без уверенности |
| Создавать файлы по запросу | Файлы с `_fixed`, `_final`, `_v2` |
| Предлагать улучшения | Менять архитектуру без согласования |
| Исправлять ошибки | Скрывать ошибки через try/except |

### Escalation Rules
| Ситуация | Действие |
|----------|----------|
| Уверенность < 50% | Уточнить у пользователя |
| Изменение > 5 файлов | Показать план, ждать OK |
| Архитектурное решение | Предложить варианты |
| Неясные требования | Задать вопросы |
| Ошибка повторилась 3+ раз | STOP → обновить правила немедленно |
| git push | Прогнать ВСЕ тесты, push только на зелёных |
| Push rejected (protected branch, diverged) | СТОП → объяснить → предложить варианты → ждать OK |

---

## Forbidden Actions

- ❌ Файлы с `_fixed`, `_final`, `_v2` — редактируем оригинал
- ❌ Перезаписывать файл целиком — точечные изменения
- ❌ Создавать дубликаты — найти и расширить существующее (`/check-duplicates`)
- ❌ Создание файла без `/check-duplicates`
- ❌ «Готово» без открытия и проверки файлов
- ❌ «Работает» без реального запуска
- ❌ «Визуально совпадает» без `visual-diff < 1%`
- ❌ Игнорировать ошибки терминала
- ❌ Делать assumptions без проверки данных
- ❌ Фиксить симптомы — найти и исправить root cause
- ❌ Писать код ДО таблицы тест-кейсов (TDD)
- ❌ Писать код ДО failing tests (TDD)
- ❌ Пропуск Prompt Preparation для STANDARD/COMPLEX
- ❌ Пропуск pipeline этапов
- ❌ git push без прогона тестов
- ❌ Рефлексия без обновления хотя бы одного файла правил
- ❌ `git push --force` / `--force-with-lease` без явного разрешения пользователя
- ❌ `git reset --hard` на ветке с непушенными коммитами как «quick fix»

---

## Code Standards

### KISS / YAGNI / MVP (mandatory)

Перед добавлением любой абстракции — 5 вопросов:
1. Нужно ли это СЕЙЧАС? → Нет = НЕ делай
2. Решает ли это РЕАЛЬНУЮ проблему? → Нет = НЕ делай
3. Упрощает ли код для ДРУГИХ? → Нет = НЕ делай
4. Можно ли проще? → Да = делай проще
5. Добавляет НОВУЮ зависимость? → Да = подумай дважды

Over-engineering red flags (STOP and simplify):
- > 3 abstraction layers для одной операции
- Factories creating factories
- Multiple ways to do the same thing
- Abstraction для кода используемого один раз
- Code «for later» / «just in case»

Подробнее: `/standard-kiss-yagni`

### File Size Limits

| File type | Soft limit | Hard limit |
|-----------|------------|------------|
| Routes/Controllers | 300 | 600 |
| Services | 400 | 800 |
| Repositories | 400 | 800 |
| React components | 200 | 400 |
| Types/Interfaces | 200 | 400 |
| API client (frontend) | 300 | 600 |

- File > soft = план split ПЕРЕД добавлением кода
- File > hard = ОБЯЗАН split перед любыми изменениями
- Split по бизнес-доменам, НЕ по техническим слоям

Подробнее: `/standard-file-size-limits`

### React Rules
- Hooks ВСЕГДА на верху компонента, ДО любых early returns
- No hooks внутри if/else, циклов, условий
- Data checks ВНУТРИ hook callbacks

### API Pagination
- НИКОГДА не полагаться только на `response.length < limit`
- ВСЕГДА использовать `total` из API metadata
- Safety limits как fallback

Подробнее: `/standard-code-quality`

---

## Project Initialization

### При создании нового проекта:

1. **Создать `<project>/CLAUDE.md`** — ТОЛЬКО проектная специфика (стек, команды, hard rules, ссылки)
2. **Создать `<project>/AGENTS.md`** — архитектура, ключевые файлы, env vars
3. **Создать `<project>/RESEARCH.md`** (если миграция/рефакторинг) — описание исходного кода

Глобальные правила (этот файл) НЕ копировать — они авто-грузятся.

### Если проект имеет workflow (pipeline):

4. **Создать `<project>/WORKFLOW.md`** — pipeline этапы, роли агентов, checkpoints
5. **Создать `<project>/tasks/`** — папка с подпапками по разделам
6. **После каждого цикла** — `/reflection` → обновить правила

---

## Session Workflow

```
/start → [работа] → /session-end
```

| Момент | Skill |
|--------|-------|
| Начало сессии | `/start` — read context, git status, pending tasks |
| Конец сессии | `/session-end` — update memory, log errors, quality score |
| После багфикса | `/error-learning` — Symptom → Root Cause → Fix → Prevention |
| 5+ improvements в backlog | `/backlog-to-rules` — внедрить в правила |
| Анализ UI/UX | `/evaluate-jobs` — JTBD анализ |
| Ошибка в «done» | `/fix-last-task` — исправление |

Ошибки логируются в `experience.md` / memory. Quality scores трекаются для трендов.

---

## Skills

Расположены в `~/.claude/skills/` (глобально) + опционально `<project>/.claude/skills/`. Вызываются по имени (`/skill-name`).

### Core / Verification
| Skill | Когда |
|-------|-------|
| `/verify` | Перед КАЖДЫМ DONE (ШАГ 3) |
| `/visual-diff` | После любой CSS/SCSS работы |
| `/validate-from-end` | RAT перед STANDARD/COMPLEX |

### Process
| Skill | Когда |
|-------|-------|
| `/reflection` | После цикла pipeline |
| `/fix-last-task` | После «done» с багом |
| `/backlog-to-rules` | 5+ improvements |
| `/review` | Перед мержем |

### Analysis
| Skill | Когда |
|-------|-------|
| `/techdebt-scan` | Конец сессии, перед рефакторингом |
| `/check-duplicates` | ПЕРЕД созданием файла/функции |
| `/evaluate-jobs` | Анализ UI/UX, ревью текстов |

### Session
| Skill | Когда |
|-------|-------|
| `/start` | Начало каждой сессии |
| `/session-end` | Конец каждой сессии |

### Protocols (on-demand)
| Skill | Содержит |
|-------|----------|
| `/protocol-development` | Development + TDD |
| `/protocol-bugfix` | Bugfix + 5 Whys |
| `/protocol-refactoring` | Tests first |
| `/protocol-research` | Data first |
| `/protocol-prepare-prompt` | Prompt preparation |
| `/protocol-freeze-recovery` | Когда залип |

### Built-in (Anthropic)
`/Design`, `/frontend-design`, `/pdf`, `/xlsx`, `/pptx`, `/docx`, `/canvas-design`, `/webapp-testing`, `/mcp-builder`, `/doc-coauthoring`, `/skill-creator`, `/brand-guidelines`, `/algorithmic-art`, `/web-artifacts-builder`, `/internal-comms`, `/theme-factory`, `/claude-api`, `/code-review`, `/security-review`, `/run`, `/loop`, `/schedule`, `/verify`, `/review`, `/init`.

Полный список skills — `ls ~/.claude/skills/`.
