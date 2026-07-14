# WORKFLOW.md — Global Development Pipeline v3

> **Глобальный пайплайн.** Лежит в `~/.claude/WORKFLOW.md`, применяется ко ВСЕМ
> проектам (проектные копии опциональны — если проект держит свою, синхронизировать с этой). Дополняет
> `~/.claude/CLAUDE.md` (ШАГ 0–5 = протокол ответа; этот файл = пайплайн задачи-с-кодом).
> Product Gate (1c-PG) живёт в CLAUDE.md — здесь не дублируется, только вызывается.

---

## Pipeline (полный, для L/XL)

```
┌──────┐  ┌────────┐  ┌──────────┐  ┌───────────┐  ┌────────┐  ┌──────┐  ┌─────────┐  ┌────────┐
│0.GIT │→ │1.BS+TSK│→ │2.ANALYSIS│→ │3.IMPLEMENT│→ │4.REVIEW│→ │5.TEST│→ │6.REFLECT│→ │7.MERGE │
└──────┘  └────────┘  └──────────┘  └───────────┘  └────────┘  └──────┘  └─────────┘  └────────┘
```

---

## Дорожки по размеру (lane routing)

> Размер задачи оценивает Claude (ШАГ 0 + effort XS/S/M/L) — **механизм оценки не меняется**.
> По размеру выбирается дорожка через тот же пайплайн:

| Размер | Дорожка | Этапы | Субагенты |
|--------|---------|-------|-----------|
| **XS/S** | Inline (solo) | `0.GIT → 3.IMPLEMENT → 5.TEST → [4.REVIEW*] → 7.MERGE` | **нет** для кода — 1 независимый ревьюер на diff (Stage 4); trivial (docs/config/rename/test-only) — solo |
| **M** | **Full + субагенты** | все 7 этапов | **да** (single-track: 1 analyst → 1 developer → 1 reviewer **на Opus + confirm**) |
| **L/XL** | Full + субагенты | все 7 этапов | да (parallel фан-аут: несколько analysts/developers/reviewers **на Opus + confirm + слой оркестратора**) |

**Ключевая граница: S/XS = инлайн (один агент). M и выше = полный workflow с субагентами.**

> \* **Инлайн-код всё равно ревьюится (2026-07-13).** Даже XS/S код-change получает
> **один независимый adversarial ревьюер на `git diff` перед мержем** — оркестратор
> НИКОГДА не self-review-and-merge кода. Ревьюер может **ESCALATE** в Workflow, если
> diff трогает рисковую поверхность. Trivial (docs/config/rename/test-only) — solo.
> Детали и merge-block — в **Этап 4** ниже.

### 🟡 M-lane — полный workflow, single-track оркестрация

M **НЕ** срезает этапы — идёт по всем 7, но оркестрация «лёгкая» (по одному субагенту на роль,
без параллельного фан-аута). Самое важное: **этап 2.ANALYSIS с analyst-субагентом сохраняется** —
именно он даёт нормальное **описание/детализацию задачи** (это ценно, инлайн его не заменяет).

- **1.BRAINSTORM+TASK** — Product Gate (если user-facing, CLAUDE.md 1c-PG) + постановка.
- **2.ANALYSIS** — **1 analyst-субагент** (Opus): описание задачи + архитектура + **RESEARCH.md
  Phase обязателен** (лёгкая заметка для M; полная — для L) + implementation-план.
- **3.IMPLEMENT** — **1 developer-субагент** (Sonnet), TDD по плану.
- **4.REVIEW** — **1 reviewer-субагент** (5-осевой rubric + verdict) + verification-gate.
- **5.TEST / 6.REFLECT / 7.MERGE** — как обычно.

### Отличие M от L/XL

Одно и то же — **полный orchestrated workflow**. Разница — **глубина фан-аута**:
- **M:** по одному субагенту на роль (single-track), задача влезает в один проход.
- **L/XL:** параллельный фан-аут (несколько analysts/developers/reviewers), задача не держится
  в одном контексте (10+ файлов / миграция / 3+ слоя).

Инлайн (без субагентов) — **только XS/S**.

---

## Этап 0: GIT — Создание ветки

**Выход:** новая feature ветка

```bash
# Префикс по типу задачи:
git checkout -b feat/{section}      # новая фича
git checkout -b fix/{section}       # багфикс
git checkout -b refactor/{section}  # рефакторинг
git checkout -b docs/{section}      # документация

# Пример:
git checkout -b feat/error-pages
```

**Правила:**
- Одна задача = одна ветка
- Имя ветки = имя секции (slugified)
- Базовая ветка = `main` (или `develop` если используете gitflow)

---

## Этап 1: BRAINSTORM + TASK (продуктовый контроль — владелец WHAT)

**Выход:** `tasks/{section}/tasks-{section}.md` (с секцией Decisions Log)

> Эта стадия определяет **ЧТО** строим (scope, UX, поведение, тексты). Пользователь
> участвует здесь. Stage 2 (ANALYSIS) — это уже **КАК** (код/архитектура), туда
> пользователь не идёт. Поэтому всю продуктовую неопределённость снимаем ДО анализа.

1. Прочитать `BACKLOG.md` — найти задачу
2. **PRODUCT GATE** (если задача user-facing / задевает scope; технические — пропустить):
   - **a. Brainstorm** — уточняющие вопросы пользователю ПО ОДНОМУ за раз (multiple-choice), пока не ясны цель / scope / UX / критерии успеха.
   - **b. Список продуктовых решений** → пользователю на явный выбор (scope, in/out MVP, UX-флоу, тексты, видимые данные). Технические дефолты — озвучить, не блокировать.
   - **c. 🚦 HARD-GATE:** Stage 2 ANALYSIS и любой код — ТОЛЬКО после апрува продуктовых решений.
   - **d. Decisions Log** в task-файл: решение → кто решил (пользователь / AI-default).
   - 🚩 «я предположил / для удобства / логично» = СТОП, вынести вопрос (см. global CLAUDE.md «1c-PG»).
3. Определить scope: страницы, компоненты, API (из утверждённых решений)
4. Sub-tasks (5-8 высокоуровневых) с тестами в каждом
5. Указать Relevant Files
6. Обновить `BACKLOG.md` — статус задачи `IN_PROGRESS`

### Spec Self-Review (после написания постановки, свежим взглядом)

> Источник: Superpowers `brainstorming`. Для L/XL (где постановка выносится в файл) — обязательно; для
> M — быстрый инлайн-проход. НЕ путать с «design для каждого проекта» (у нас это gate только для
> user-facing/scope; XS/S SIMPLE идут напрямую).

Перед переходом к Stage 2 ANALYSIS прогони постановку по 4 пунктам, чини инлайн:
1. **Placeholder scan:** «TBD», «TODO», незаполненные секции, размытые требования? → уточни.
2. **Internal consistency:** секции не противоречат друг другу? Архитектура совпадает с описанием фич?
3. **Scope check:** фокус на один план реализации, или надо декомпозировать на под-проекты?
4. **Ambiguity check:** требование можно понять двояко? → выбери одно и сделай явным.

---

## Этап 2: ANALYSIS

> ⚙️ Код / архитектура / data flow. **Пользователь НЕ участвует** — стадия
> consumes уже детализированную и продуктово-утверждённую постановку из Stage 1.

**Выход:**
- Manual: `tasks/{section}/analysis-{section}.md`
- Orchestrated: `tasks/{section}/analyst-architect.md` + `analyst-*.md` файлы
- **MANDATORY для всех project types:** дописать новую секцию в `RESEARCH.md`

### 🔴 HARD RULE: каждый Stage 2 дописывает секцию в RESEARCH.md

**Применяется ко всем типам проектов** (greenfield, maintenance, library, migration, content). Различается только структура и частота обновления. См. расширение правила ниже.

**Структура секции — migration-вариант (оригинальный, наиболее детальный):**

```
## Phase N: {Section Name} (YYYY-MM-DD)

### N.1 Architecture
- Файлы: список с LOC
- Cross-module dependencies (что модуль читает извне)
- Routes (URLs из legacy paths.ts)

### N.2 API Endpoints
- Полная таблица: # | endpoint | method | request | response | notes
- TypeScript contracts (interface/type definitions)

### N.3 State Shape
- Legacy Redux slice (если есть)
- Selectors / hooks
- User profile fields consumed

### N.4 Data Flows
- Каждая бизнес-операция: trigger → API → store/cache → component

### N.5 Risks / Quirks
- Race conditions, security, performance, edge cases
- Legacy hacks, технический долг, что НЕ воспроизводить
```

**Структура секции — greenfield / maintenance / library вариант:**

```
## Phase N: {Task Name} (YYYY-MM-DD)

### N.1 What was added/changed
- Новые модули / функции / endpoints (с LOC и ссылками на файлы)
- Изменения в существующих модулях

### N.2 New contracts
- API endpoints (request/response shape)
- Function signatures для public API
- Data structures / types

### N.3 Data flow changes
- Как новый код вписывается в общий flow (обновить/расширить Phase 1 диаграмму при необходимости)

### N.4 Quirks / Gotchas introduced
- Non-obvious behavior
- Edge cases и accepted risks
- Dependencies на других модулях, которые не обязательны к соблюдению
- Новые environment variables

### N.5 Tech debt or follow-ups
- Что оставлено недоделанным
- Что нужно учесть в следующих задачах
```

**Структура секции — content (документация) вариант:** легковесная — просто список изменений в секции "Recent updates" в начале RESEARCH.md, без обязательных подсекций.

И обновить **Лог исследований** таблицу в начале RESEARCH.md (дата, секция, повод, автор).

**Зачем для всех типов:**

- **Migration:** persistent encyclopedia старого проекта, переживает итерации переписывания (исходный use case).
- **Maintenance:** capture tribal knowledge, которое иначе теряется в commit messages. Новый разработчик (или AI агент в новой сессии) начинает с полного контекста вместо reverse-engineering из кода.
- **Greenfield:** инвариант "как оно было задумано" который сохраняется даже после множества рефакторингов. Записывается с первой фичи, а не "когда-нибудь".
- **Library:** API surface, breaking changes, invariants для внешних пользователей.

**Lessons:**
- **Task 10.0 Billing (partners-portal, 2026-04-08):** analyst-architect собрал ~700 строк деталей про legacy billing, но они остались только в `tasks/billing/analyst-architect.md`. Правило добавлено для migration.
- **DL-001 Download CSV (analytics-agent, 2026-04-09):** framework развернули без `/init-project`, RESEARCH.md не появился, работа пошла с неполным контекстом (например, quirks типа `_sanitize_messages` или double-charset в send_file выяснились во время работы). Правило расширено с migration-only на все project types.

**Verification:** перед закрытием Stage 2 agent (или orchestrator) ОБЯЗАН проверить:
```
[ ] RESEARCH.md содержит новую "Phase N" секцию по этой задаче
[ ] Лог исследований обновлён
[ ] Для migration: API endpoints + state shape + data flows + routes
[ ] Для maintenance/greenfield: new contracts + data flow changes + quirks
[ ] Для library: API surface changes + breaking/non-breaking markers
```

**Исключение:** lightweight tasks (S-size, < 30 строк кода, без architectural impact) могут пропустить запись в RESEARCH.md если рефлексия явно подтверждает "nothing architecturally new". Записать в `tasks/reflection-history.md` строку с `Skipped RESEARCH.md update: trivial`.

### Auto-orchestration (для COMPLEX с `multi_agent.enabled: true`)

Orchestrator АВТОМАТИЧЕСКИ spawn analysts параллельно через Task tool:
```
Task("analyst-architect") + Task("analyst-fe-senior")  # parallel
```

После завершения:
1. Orchestrator читает output файлы
2. **MANDATORY:** orchestrator (или analyst-architect) дописывает Phase N в RESEARCH.md
3. Aggregates → `tasks/{section}/implementation-plan.md`

### Manual mode

**Анализ архитектуры:** data flow, dependencies, API endpoints, state shape, risks
**Анализ кода:** component assessment, code smells, decomposition

**Если задача архитектурная** → создать **ADR** в `docs/adr/` (см. ADR template).
**Для ВСЕХ project types** → ОБЯЗАТЕЛЬНО дописать Phase N в `RESEARCH.md` (см. Hard Rule выше). Исключение: trivial S-tasks без architectural impact (записать skip-причину в `tasks/reflection-history.md`).

---

## Этап 3: IMPLEMENT

**Выход:** код + тесты в feature branch

### Auto-orchestration (для COMPLEX)

Orchestrator АВТОМАТИЧЕСКИ spawn developers SEQUENTIALLY:
```
Task("developer-types")     # 1st
→ wait → read output
Task("developer-api")       # 2nd, reads developer-types output
→ wait → read output
Task("developer-ui")        # 3rd, reads developer-api output
→ wait → read output
```

Sequential потому что слои зависят друг от друга. Orchestrator контекст не растёт — sub-agents работают изолированно.

### Manual mode

**Hard Stop:** перед кодом
```
[ ] Прочитал analysis-{section}.md
[ ] Выполнил PRE-ACTION (Duplicate Check + JTBD)
[ ] Таблица тест-кейсов создана (TDD Phase 0)
[ ] Я в feature branch (не в main)
```

**Порядок:** types → api → hooks → components → pages

**После каждого parent task:**
- `tsc --noEmit` — 0 errors
- Tests green
- `git commit` с conventional commit message
- Task file `[x]`

---

## Этап 4: REVIEW (adversarial + confirm-pass)

**Выход:** `tasks/{section}/review-{section}.md` ИЛИ `reviewer-*.md` файлы

> ⭐ **Ревью — адверсариальное, не подтверждающее.** Цель ревьюера — найти
> **воспроизводимый прод-баг**, а не поставить APPROVED. Урок из реального кейса:
> one-shot sub-agent ревью подтвердил код с латентным багом (флаг, который всегда
> `true`) — поймал только независимый второй слой ревью. Отсюда правила ниже.

### Что значит «адверсариальное ревью» (для ЛЮБОЙ дорожки)

1. **Трассируй РЕАЛЬНЫЙ steady-state, не happy-path.** Как код ведёт себя на
   второй запуск / пустые данные / после рестарта / при частичном отказе — а не
   только на чистом первом прогоне.
2. **Каждый finding = `file:line` + `failureScenario` + `testGap`:**
   - `failureScenario` — конкретный вход/состояние → неверный выход или краш.
   - `testGap` — **докажи, что существующие тесты этого НЕ ловят** (назови тест,
     который «зелёный», но пропускает баг). Finding без доказанного testGap — слабый.
3. **Evidence gate (ДО findings):** прогнать ПОЛНЫЙ suite (не только новые тесты) +
   typecheck + build; прочитать реально изменённые файлы (`file:line`); на каждое
   утверждение — процитировать тест-доказательство. Нет доказательства → **UNVERIFIED**.
4. **Adversarial clearing:** явно ПРОВЕРИТЬ и ОЧИСТИТЬ категории риска с доказательством
   (`injection · XSS · authz/scope · secrets-never-leak · partial-failure/idempotency ·
   pagination/N+1`). «CLEAN because <evidence>» — требуемый вывод, не пропуск.

### Confirm-pass (обязателен после каждого фикса)

Ревью — это не «нашёл → закрыл». После того как разработчик починил finding,
**ТОТ ЖЕ ревьюер повторно проверяет фикс В КОРНЕ** — не «тест позеленел», а что
причина устранена и `failureScenario` больше не воспроизводится:
- `confirmStillBroken: true` → **мерж заблокирован**, фикс возвращается на доработку.
- Fixes выполняются через skill **`/receiving-review`** (verify claim → fix at root → жди confirm).

### Verdict (taxonomy)

- **APPROVED** — нет findings выше `minor`.
- **APPROVE-WITH-NITS** — функц. ок, тесты зелёные, только `minor`/by-design ниты (мерж разрешён, ниты перечислить).
- **CHANGES REQUESTED / BLOCK** — ≥1 `critical`/`major`, падающий/отсутствующий тест, или `confirmStillBroken`.

**🚦 Merge-block (non-negotiable):** любой нерешённый `critical`/`major` ИЛИ `confirmStillBroken:true` = **мерж запрещён**. Verdict первой строкой, evidence ниже.

### Ревью-дефолт по дорожкам (non-negotiable)

| Дорожка | Ревьюер | Модель | Confirm | Доп. слой перед мержем |
|---------|---------|--------|---------|------------------------|
| **XS/S inline — код** | 1 независимый adversarial ревьюер на `git diff` (Agent tool) | Sonnet (малый diff) | да | оркестратор **НИКОГДА** не self-review-and-merge кода |
| **XS/S inline — trivial** (docs / config / rename / test-only) | не нужен (solo) | — | — | — |
| **M/L/XL Workflow** | reviewer-субагент (Stage 4) | **Opus** (`REVIEW_MODEL='opus'`) | да, обязателен | **независимое adversarial ревью оркестратора** на полном diff (trace steady-state + verify tests cover edge + live-verify) |
| **XL / critical** | то же + **персистентный reviewer-teammate** через `/orchestrate` (live reviewer↔dev, resume по SendMessage) | Opus | да | + оркестраторский слой выше |

- **One-shot sub-agent ревью НИКОГДА не достаточно для Workflow-задачи** — обязателен второй, независимый слой: оркестратор читает ВЕСЬ diff, трассирует steady-state, проверяет что тесты покрывают edge, и **live-verify**.
- **Инлайн код-change: оркестратор НЕ ревьюит-и-мержит сам.** Ровно ОДИН независимый adversarial ревьюер на реальном diff перед мержем — та же дисциплина (`file:line` + `failureScenario` + `testGap`, «докажи что тесты не ловят»).
- **ESCALATE:** ревьюер оценивает риск на РЕАЛЬНОМ diff (upfront-догадка о риске ненадёжна) и может флагнуть «это должно было идти через Workflow», если diff трогает рисковую поверхность (**auth/tenant · creds/secrets · migrations/data-model · billing · security · two-store / reconciliation · egress/deploy · destructive ops**) И нетривиален → тогда переделать через полный workflow.
- **Trivial (docs / config / rename / test-only) остаётся solo** — ревьюер не нужен.

### Auto-orchestration (M/L/XL)

Orchestrator spawn reviewers PARALLEL (на **Opus**, `REVIEW_MODEL='opus'`):
```
Task("reviewer-architect") + Task("reviewer-fe-senior")  # parallel
+ Task("reviewer-security")   # if backend project
+ Task("reviewer-backend")    # if backend project
```

Если verdict = CHANGES REQUESTED → orchestrator spawn нужного developer для fix →
**confirm-pass ТЕМ ЖЕ ревьюером** → повтор пока не clean → **независимое ревью
оркестратора на полном diff перед мержем**.

### Manual mode

Использовать skill **`/review`** + шаблон **`~/.claude/templates/review-template.md`**:
пройти адверсариальные шаги 1–4 выше, каждый finding с `failureScenario`+`testGap`,
confirm-pass после фикса, verdict-taxonomy. Ревью ≠ «прогнал линтер → APPROVED».

---

## Этап 5: TESTING

**Выход:** `tasks/{section}/testing-{section}.md` ИЛИ `qa-results.md`

### Что Stage 5 проверяет (regression scope)

Stage 5 — это **полный regression**, не только новые тесты:

```bash
npx tsc --noEmit          # вся кодовая база (а не только новые файлы)
npx vitest run            # ВСЕ тесты, не только новые — это и есть regression suite
npx vite build            # production билд всей сборки
python3 scripts/visual-diff.py {page}  # для CSS/UI работы
```

Если новый код сломал существующие фичи — `vitest run` это поймает. Это автоматическая регрессия.

### Visual-diff — MANDATORY для migration projects (HARD RULE с 2026-04-08)

**Если проект — migration с легаси reference (см. `.claude/project-config.yml` → `reference.legacy.path`):**

Visual-diff ОБЯЗАТЕЛЕН для каждой новой страницы перед мержем. Это HARD acceptance gate, не optional.

```
[ ] Каждая новая страница миграции прошла visual-diff < 1% против legacy production
[ ] Если diff > 1% → итерировать SCSS пока не пройдёт, ЛИБО explicitly defer в visual debt с записью в BACKLOG.md
[ ] "Skipped because no reference" — НЕ валидное основание. Reference = legacy production URL.
```

**Lesson (task 10.0 Billing 2026-04-08):** visual-diff был skipped в QA stage (sub-agent не имел Bash, orchestrator забыл re-run), 5 страниц замержились с diff 2.82-27.12% от legacy. Premature merge пойман только пост-фактум по жалобе пользователя. Это структурный fail enforcement → теперь hard rule.

### Auto-orchestration (для COMPLEX)

Orchestrator АВТОМАТИЧЕСКИ spawn qa:
```
Task("qa") → runs tsc, vitest, build, visual-diff
```

QA sub-agent итерирует visual-diff пока < 1%.
**Если QA sub-agent не имеет Bash доступа** → orchestrator ОБЯЗАН re-run static checks И visual-diff сам перед commit. См. `/orchestrate` Circuit Breaker → QA Bash requirement.

### Manual mode

```
[ ] TypeScript: 0 errors
[ ] Tests: all pass (full suite — это regression)
[ ] Coverage: > 70% для новых файлов
[ ] Build: success
[ ] Visual diff: < 1% (если CSS И ЕСТЬ legacy reference) — MANDATORY для migration
```

---

## Этап 6: REFLECTION (ключевой этап)

**Выход:** `tasks/{section}/reflection.md` + **обязательное** обновление одного из:

```
Lesson о поведении агента?  → memory/feedback_*.md
Lesson о процессе?          → CLAUDE.md или WORKFLOW.md
Архитектурное решение?      → docs/adr/ADR-XXX-{title}.md (НОВЫЙ)
Повторяющийся паттерн (3+)? → .claude/skills/{new-skill}.md (НОВЫЙ)
Предложение по продукту?    → tasks/improvements.md
Факт о проекте?             → RESEARCH.md (если есть)
Изменение в продукте?       → CHANGELOG.md
```

**Self-improvement enforcement:** если рефлексия НЕ создала минимум 1 артефакт из списка — она НЕ завершена. DONE заблокирован.

### 7 вопросов
1. Что сделано хорошо?
2. Что пошло не так?
3. Что бы сделал по-другому?
4. Какие паттерны повторять?
5. Какие паттерны избегать?
6. Что нужно доработать?
7. Какие правила/скиллы добавить? **← обязан указать конкретный файл**

---

## Этап 7: MERGE / FINISH

**Выход:** работа интегрирована (merge / PR / kept / discarded), ветка обработана

### Finish Gate (перед выбором опции)

> Источник: Superpowers `finishing-a-development-branch`. Не завершай открытым вопросом «что дальше?» —
> предъяви структурированный выбор.

1. **Verify tests ПЕРВЫМ:** прогнать полный suite. Падают → показать фейлы, СТОП, не предлагать опции.
2. **Определить base branch:** `git merge-base HEAD main`.
3. **Предъявить пользователю ровно 4 опции** (не додумывать за него):
   ```
   Реализация завершена. Что делаем?
   1. Merge в <base> локально
   2. Push + создать Pull Request
   3. Оставить ветку как есть (сам разберусь позже)
   4. Отменить эту работу (discard)
   ```

### Execute choice

**Опция 1 — Merge локально:** `git checkout <base> && git pull && git merge <feat>` → **прогнать тесты на
смердженном результате** → только после успеха `git branch -d <feat>`.

**Опция 2 — Push + PR:**
```bash
git push -u origin feat/{section}
gh pr create --title "{type}({scope}): {description}" --body "..."
# После approval:
gh pr merge --squash --delete-branch
git checkout main && git pull
```

**Опция 3 — Keep as-is:** ничего не удалять, сообщить имя ветки.

**Опция 4 — Discard (🔴 typed confirmation):** показать что будет безвозвратно удалено (ветка + список
коммитов) и потребовать ввести **дословно `discard`**. Без точного слова — не удалять. После подтверждения
`git branch -D <feat>`.

**После merge (опции 1/2):**
- Обновить `BACKLOG.md` → статус DONE + ссылка на PR
- Обновить `CHANGELOG.md` → запись о выпуске

**Красные флаги:** мержить с падающими тестами · мержить без прогона тестов на результате · удалять работу
без typed-confirm · force-push без явного запроса (см. CLAUDE.md Forbidden).

---

## Hard Stop Rules

1. **Нельзя кодить** без feature branch (этап 0)
2. **Нельзя кодить** без `analysis-{section}.md` (этап 2)
3. **Нельзя говорить "готово"** без `review-{section}.md` (этап 4)
4. **Нельзя закрывать задачу** без `reflection.md` + минимум 1 артефакта self-improvement (этап 6)
5. **Нельзя мержить** без passed testing (этап 5)
6. **Нельзя говорить "визуально совпадает"** без visual diff < 1%
7. **"Давай дальше" НЕ отменяет pipeline**
8. **Нельзя мержить КОД без независимого ревью** — оркестратор никогда не self-review-and-merge кода; инлайн-код → 1 независимый ревьюер на diff, Workflow → reviewer+confirm+слой оркестратора (этап 4). Trivial docs/config/rename/test-only — исключение.
9. **Нельзя мержить** при нерешённом `critical`/`major` finding ИЛИ `confirmStillBroken:true` (этап 4 merge-block)

---

## Архивация

Когда `tasks/` накопит 30+ папок:

```bash
# Перенести завершённые задачи в архив
mkdir -p tasks/archive/2026-Q1
mv tasks/{old-section-1,old-section-2,...} tasks/archive/2026-Q1/

# Обновить BACKLOG.md — добавить ссылки на архивные задачи
```

Архивация раз в квартал. Активные задачи остаются в `tasks/`.

---

## Lightweight Mode (для S задач)

Для микро-задач (typo, 1 файл, обновление текста) можно использовать lightweight pipeline:

```
0.GIT → 3.IMPLEMENT → 5.TEST → 7.MERGE
```

Пропускаются: 1.TASK, 2.ANALYSIS, 6.REFLECTION.

**⚠️ 4.REVIEW НЕ пропускается для КОДА (2026-07-13).** Если lightweight-задача меняет
реальный код — перед мержем обязателен **один независимый adversarial ревьюер на `git diff`**
(оркестратор не self-review-and-merge кода; ревьюер может ESCALATE в full workflow —
см. Этап 4 → «Ревью-дефолт по дорожкам»). Полностью solo (без ревьюера) — только
**trivial**: docs / config / rename / test-only.

**Условие:** задача < 30 строк изменений, нет нового функционала, нет архитектурных решений.

**ВНИМАНИЕ:** lightweight mode — это исключение, не правило. Если сомневаешься — используй full pipeline.

---

## Lessons Learned

| Дата | Ошибка | Исправление |
|------|--------|-------------|
| _пример_ | Pipeline пропускался "для скорости" | Все 7 этапов обязательны для full mode |
| _пример_ | Visual match "на глаз" | Automated pixel diff (< 1%) |
| _пример_ | Reflection без обновления правил | Self-improvement enforcement добавлен |
