# Claude Code Framework v3

Фреймворк для структурированной разработки с AI-агентом (Claude Code). Обеспечивает предсказуемое качество через правила, протоколы, верификацию, рефлексию, self-improvement loop и multi-agent orchestration.

## Что нового в v3

- 🆕 **Multi-agent orchestration** — для XL задач, sub-agents в isolated contexts
- 🆕 **`/init-project` wizard** — интерактивная настройка нового проекта
- 🆕 **Universal sub-agent templates** — analyst, developer, reviewer, qa роли
- 🆕 **`.claude/project-config.yml`** — конфигурация stack, ролей, конвенций
- 🆕 **26 skills** (было 24) — добавлены init-project и orchestrate

## Что было в v2

- ✅ **Git workflow** интегрирован в pipeline (feature branch → PR → merge)
- ✅ **ADR (Architecture Decision Records)** — фиксация архитектурных решений
- ✅ **BACKLOG.md** — единый реестр задач с приоритетами
- ✅ **CHANGELOG.md** — история изменений
- ✅ **AGENTS.md** — хаб проекта, единая точка входа памяти
- ✅ **Reflection enforcement** — рефлексия ОБЯЗАНА создать минимум 1 артефакт
- ✅ **Skills с правильными frontmatter** — Claude автоматически детектит
- ✅ **Архивация tasks/** — скрипт для квартальной архивации
- ✅ **Lightweight mode** — упрощённый pipeline для S задач

## Быстрый старт

```bash
# 1. Скопировать в свой проект
cp -r agentic-coding-template/.claude /path/to/your/project/
cp -r agentic-coding-template/scripts /path/to/your/project/
cp -r agentic-coding-template/tasks /path/to/your/project/
cp -r agentic-coding-template/templates /path/to/your/project/
cp -r agentic-coding-template/docs /path/to/your/project/
cp agentic-coding-template/CLAUDE.md /path/to/your/project/
cp agentic-coding-template/WORKFLOW.md /path/to/your/project/
cp agentic-coding-template/BACKLOG.md /path/to/your/project/
cp agentic-coding-template/CHANGELOG.md /path/to/your/project/
cp agentic-coding-template/AGENTS.md /path/to/your/project/

# 2. Заполнить AGENTS.md — описание проекта, стек, конвенции

# 3. Настроить visual-diff (опционально)
# Отредактировать scripts/visual-diff.py — указать URL reference и localhost

# 4. Начать работу
# Claude Code автоматически прочитает CLAUDE.md, AGENTS.md, RESEARCH.md (если есть)
```

### Установка глобального слоя (один раз на машину, для каждого сотрудника)

Этот шаблон содержит полную копию глобальной конфигурации Claude Code в папке `.claude/`.
Чтобы правила, протоколы и skills работали во ВСЕХ проектах автоматически — разверни их в `~/.claude/`:

```bash
# Глобальные правила (авто-загрузка в каждый чат Claude Code)
cp agentic-coding-template/.claude/CLAUDE.md   ~/.claude/CLAUDE.md

# 26 skills (вызываются по /skill-name из любого проекта)
cp -r agentic-coding-template/.claude/skills   ~/.claude/skills
```

> ⚠️ `~/.claude/CLAUDE.md` перезапишется — если у сотрудника уже есть свой, сначала сделать бэкап.
> `settings.json` (permissions, env) НЕ входит в шаблон — он машинно-специфичный, настраивается отдельно.

---

## Как это работает

### Архитектура: 3 уровня

```
┌──────────────────────────────────────────────────────┐
│  Уровень 1: ПРАВИЛА (always loaded)                  │
│  ~/.claude/CLAUDE.md (global) + <project>/CLAUDE.md   │
│  Загружается в КАЖДЫЙ разговор автоматически          │
└──────────────────────────────────────────────────────┘
        ↓ routing по типу задачи
┌──────────────────────────────────────────────────────┐
│  Уровень 2: ПРОТОКОЛЫ (on-demand skills)             │
│  .claude/skills/protocol-*.md                        │
│  Загружается ТОЛЬКО когда нужен                      │
└──────────────────────────────────────────────────────┘
        ↓ результаты записываются
┌──────────────────────────────────────────────────────┐
│  Уровень 3: АРТЕФАКТЫ (файлы проекта)                │
│  tasks/, WORKFLOW.md, RESEARCH.md                    │
│  Накапливают знания и решения                        │
└──────────────────────────────────────────────────────┘
```

### Каждый ответ AI-агента: 5 шагов

```
ШАГ 0: Оценка сложности
  🟢 SIMPLE (1-2 файла) → Execute → Verify → DONE
  🟡 STANDARD (фича, баг) → Prompt Prep → Plan → Execute → Verify → DONE
  🔴 COMPLEX (архитектура) → Prompt Prep → Plan → Execute → Verify + Review → DONE

ШАГ 1: Routing → загрузить нужный протокол
  Новая фича → protocol-development.md (TDD)
  Баг         → protocol-bugfix.md (5 Whys)
  Рефакторинг → protocol-refactoring.md (Tests first)
  Данные      → protocol-research.md (Data first)

ШАГ 2: Выполнение (маленькие шаги, один файл за раз)

ШАГ 3: Проверка
  - Cross-check (каждый файл открыть и проверить)
  - Challenge (4 вопроса)
  - Confidence Score (100% минус штрафы)
  - Visual Diff (для CSS — automated pixel comparison)

ШАГ 4: DONE блок (обязательно в конце каждого ответа)

ШАГ 5: Post-Task (обновить задачи, документацию, память)
```

---

## Pipeline для задач с кодом (WORKFLOW.md)

Каждая задача, которая приводит к появлению кода, проходит **6 обязательных этапов:**

```
┌────────┐   ┌──────────┐   ┌───────────┐   ┌────────┐   ┌────────┐   ┌───────────┐
│ 1.TASK │ → │2.ANALYSIS│ → │3.IMPLEMENT│ → │4.REVIEW│ → │5.TEST  │ → │6.REFLECT  │
└────────┘   └──────────┘   └───────────┘   └────────┘   └────────┘   └───────────┘
  Что делать   Как делать     Код + тесты    Проверка      tsc/vitest   Что улучшить
                                             качества      + visual     + обновить
                                                           diff         правила
```

### Hard Stops (блокирующие правила)

| Правило | Блокирует |
|---------|-----------|
| Нет `analysis.md` | Нельзя писать код (этап 3) |
| Нет `review.md` | Нельзя говорить "готово" |
| Нет `reflection.md` | Нельзя закрывать задачу |
| Visual diff > 1% | Нельзя говорить "визуально совпадает" |
| "Давай дальше" от пользователя | НЕ отменяет pipeline |

### Артефакты каждого этапа

```
tasks/{section}/
├── tasks-{section}.md          # Этап 1: список задач
├── analysis-{section}.md       # Этап 2: архитектурный анализ
├── review-{section}.md         # Этап 4: code review
├── testing-{section}.md        # Этап 5: результаты тестов
└── reflection.md               # Этап 6: рефлексия
```

---

## Система рефлексий

### Как рефлексии превращаются в правила

Это **ключевая механика** фреймворка. Без неё рефлексии = просто текст.

```
Рефлексия (reflection.md)
    │
    ├── Actionable lesson о ПОВЕДЕНИИ агента?
    │   └── → memory/feedback_*.md (персистентная память)
    │       └── → Загружается в КАЖДУЮ сессию автоматически
    │
    ├── Actionable lesson о ПРОЦЕССЕ?
    │   └── → CLAUDE.md или WORKFLOW.md (правила)
    │       └── → Загружается в КАЖДЫЙ ответ
    │
    ├── Предложение по ПРОДУКТУ/UX?
    │   └── → tasks/improvements.md (backlog)
    │       └── → Приоритезируется и берётся в работу
    │
    └── Факт о ПРОЕКТЕ (API, архитектура)?
        └── → RESEARCH.md (база знаний)
            └── → Читается при анализе задач
```

### Формат рефлексии (7 вопросов)

```markdown
1. Что сделано хорошо? → паттерны для повторения
2. Что пошло не так? → ошибки для предотвращения
3. Что бы сделал по-другому? → конкретные изменения
4. Какие паттерны повторять? → в memory/feedback
5. Какие паттерны избегать? → в memory/feedback
6. Что нужно доработать? → в tasks/improvements.md
7. Какие правила добавить? → в CLAUDE.md / WORKFLOW.md
```

### Чеклист после рефлексии

```
[ ] Записана reflection.md с 7 вопросами?
[ ] Обновлён tasks/reflection-history.md?
[ ] Actionable items → memory/feedback_*.md?
[ ] Критичные lessons → CLAUDE.md?
[ ] Process improvements → WORKFLOW.md?
[ ] UX/product ideas → tasks/improvements.md?
[ ] Факты о проекте → RESEARCH.md?
```

---

## Visual Diff — автоматическое сравнение скриншотов

Для задач с CSS/UI агент **обязан** использовать automated pixel comparison.

```
1. Playwright снимает reference screenshot (production)
2. Playwright снимает current screenshot (localhost)
3. pixelmatch вычисляет diff → diff image + %
4. Агент читает diff image → красные пиксели = проблемы
5. Агент исправляет CSS
6. Повторяет пока diff < 1%
```

### Установка

```bash
npm install -D pixelmatch pngjs
pip install playwright && playwright install chromium
```

### Использование

```bash
python3 scripts/visual-diff.py login     # сравнить login page
python3 scripts/visual-diff.py dashboard # сравнить dashboard
```

### Настройка для своего проекта

Отредактировать `scripts/visual-diff.py`:

```python
REFERENCE_BASE = "https://your-production-site.com"  # reference
CURRENT_BASE = "http://localhost:3000"                # dev server

PAGES = {
    "login": {
        "path": "/login",
        "login_required": False,
        "viewport": {"width": 1440, "height": 900},
    },
    "dashboard": {
        "path": "/dashboard",
        "login_required": True,
        "viewport": {"width": 1440, "height": 900},
    },
}
```

---

## Полная карта скиллов (24 шт.)

### Протоколы — загружаются автоматически через Routing Table

| Скилл | Trigger | Что делает |
|-------|---------|-----------|
| `protocol-development` | Новая фича, создать, добавить | Duplicate Check → JTBD → TDD (Red→Green→Refactor) |
| `protocol-bugfix` | Баг, ошибка, не работает | STOP → CAPTURE → 5 Whys → Fix Root Cause |
| `protocol-refactoring` | Рефакторинг, улучшить | Tests FIRST → Small Steps → Run After Each |
| `protocol-research` | Данные, анализ | Load → Schema → Profile → Hypothesis → Experiment |
| `protocol-freeze-recovery` | Зависание, freeze | Understand Before Retry |
| `protocol-prepare-prompt` | STANDARD/COMPLEX задачи | Извлечение constraints из запроса |

### Process — вызываются в конкретных точках workflow

| Скилл | Когда вызывается | Что делает |
|-------|-----------------|-----------|
| `verify` | **ШАГ 3 каждого ответа** | Cross-check + Challenge + Confidence + RAT |
| `visual-diff` | **Любое CSS/SCSS изменение** | Playwright screenshot → pixelmatch → iterate < 1% |
| `reflection` | **Этап 6 pipeline** | 7 вопросов + gap analysis + обновление правил |
| `review` | **Этап 4 pipeline** | Code review: архитектура + качество + тесты |
| `start` | **Начало каждой сессии** | Read context, git status, pending tasks |
| `session-end` | **Конец каждой сессии** | Update memory, log errors, quality score |
| `check-duplicates` | **Перед созданием файла** | Поиск существующих аналогов |
| `validate-from-end` | **Перед STANDARD/COMPLEX** | Определить expected output до начала работы |
| `fix-last-task` | **После "done" с багами** | Исправление последней задачи |
| `backlog-to-rules` | **5+ улучшений накопилось** | Внедрение улучшений из improvements в правила |
| `error-learning` | **После каждого багфикса** | Symptom → Root Cause → Fix → Prevention |
| `techdebt-scan` | **Перед рефакторингом** | Поиск дублей, больших файлов, code smells |
| `evaluate-jobs` | **Анализ UI/UX** | JTBD анализ лендингов и интерфейсов |

### Standards — справочные материалы (on-demand)

| Скилл | Содержит |
|-------|---------|
| `standard-code-quality` | React Hooks правила, API Pagination, Conventional Commits |
| `standard-file-size-limits` | Soft/Hard limits + 6-step splitting procedure |
| `standard-kiss-yagni` | KISS/YAGNI/MVP + 8 red flags over-engineering |
| `standard-agent-quality` | Метрики успешности агента, QA чеклисты |
| `standard-api-testing` | API тестирование паттерны |

---

## Структура файлов

```
your-project/
├── CLAUDE.md                           # Правила проекта (always loaded; глобальные — в ~/.claude/CLAUDE.md)
├── .claude/
│   └── skills/                         # 24 скилла (on-demand)
│       ├── protocol-development.md     # TDD протокол
│       ├── protocol-bugfix.md          # 5 Whys протокол
│       ├── protocol-refactoring.md     # Tests first
│       ├── protocol-research.md        # Data first
│       ├── protocol-freeze-recovery.md # Freeze recovery
│       ├── protocol-prepare-prompt.md  # Prompt preparation
│       ├── verify.md                   # Верификация (ШАГ 3)
│       ├── visual-diff.md             # Pixel diff pipeline
│       ├── reflection.md              # Рефлексия (этап 6)
│       ├── review.md                  # Code review (этап 4)
│       ├── start.md                   # Начало сессии
│       ├── session-end.md             # Конец сессии
│       ├── check-duplicates.md        # Проверка дублей
│       ├── validate-from-end.md       # Валидация от результата
│       ├── fix-last-task.md           # Исправление после "done"
│       ├── backlog-to-rules.md        # Улучшения → правила
│       ├── error-learning.md          # Обучение на ошибках
│       ├── techdebt-scan.md           # Поиск техдолга
│       ├── evaluate-jobs.md           # JTBD анализ
│       ├── standard-code-quality.md   # Стандарт кода
│       ├── standard-file-size-limits.md # Лимиты файлов
│       ├── standard-kiss-yagni.md     # KISS/YAGNI
│       ├── standard-agent-quality.md  # Качество агента
│       └── standard-api-testing.md    # API тестирование
│       └── visual-diff.md         # Visual regression pipeline
├── scripts/
│   └── visual-diff.py             # Automated screenshot diff
├── tasks/
│   ├── checklists/
│   │   └── implementation-checklist.md  # Чеклист перед кодом
│   ├── improvements.md            # Backlog улучшений
│   └── reflection-history.md      # История рефлексий
├── CLAUDE.md                      # Главный конфиг (project-specific)
└── WORKFLOW.md                    # Pipeline (6 этапов)
```

---

## Адаптация под свой проект

### 1. CLAUDE.md — добавить проектную специфику

```markdown
## Контекст проекта
- Стек: [ваш стек]
- Архитектура: [ваша архитектура]
- Ключевые файлы: [список]

## Правила проекта
- [ваши специфичные правила]
```

### 2. WORKFLOW.md — настроить этапы

Этапы универсальные, но можно настроить:
- Acceptance criteria для testing
- Формат review (кто ревьюит)
- Частоту рефлексий

### 3. Visual Diff — указать URLs

Настроить reference URL и pages в `scripts/visual-diff.py`.

### 4. Memory — начать с пустой

```
.claude/projects/{project}/memory/
├── MEMORY.md                 # Индекс (создастся автоматически)
└── (feedback файлы появятся из рефлексий)
```

---

## FAQ

**Q: Обязательно ли проходить все 6 этапов pipeline?**
A: Да, для КАЖДОЙ задачи с кодом. Это правило появилось после того, как пропуск этапов привёл к накоплению багов и повторным исправлениям.

**Q: Что если пользователь говорит "давай дальше", а этапы не пройдены?**
A: Агент обязан предупредить: "Пропускаем этап X? Это нарушение pipeline." Пользователь может подтвердить, но это осознанное решение.

**Q: Как часто обновлять правила из рефлексий?**
A: После КАЖДОЙ рефлексии. Если lesson actionable — сразу в правила. Не "потом добавлю".

**Q: Visual diff обязателен для каждого CSS изменения?**
A: Да. Агент не может оценить визуальное соответствие "на глаз". 5% diff = сотни пиксельных расхождений, невидимых агенту.

---

## Лицензия

MIT — используйте свободно.
