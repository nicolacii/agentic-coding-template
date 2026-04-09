---
name: init-project
description: Initialize project — interactive setup wizard. Use ONCE at the start of a new project to configure agents, tech stack, sub-agent roles, and project conventions. Generates PROJECT_KNOWLEDGE.md, agent definitions, and writes config to .claude/project-config.yml.
---

# Skill: Init Project

> Запускается ОДИН РАЗ при инициализации нового проекта.
> Интерактивный wizard, который настраивает фреймворк под конкретный проект.

---

## Когда вызывать

- Первый запуск Claude Code в новом проекте
- Когда нужно перенастроить роли sub-agents
- При смене tech stack или процессов

---

## Процесс инициализации

### Шаг 1: Project Type

Спросить у пользователя:
```
Какой тип проекта?
1. Новый проект (greenfield)
2. Миграция legacy на новый стек
3. Поддержка существующего проекта (maintenance)
4. Библиотека / SDK
5. Документация / контент
```

### Шаг 2: Languages & Stack

```
Какие языки/технологии используются? (выбрать все применимое)

Frontend:
[ ] TypeScript / JavaScript
[ ] React / Vue / Svelte / Angular
[ ] CSS / SCSS / Tailwind / styled-components
[ ] Mobile: React Native / Flutter / Swift / Kotlin

Backend:
[ ] Node.js / Bun / Deno
[ ] Python (FastAPI / Django / Flask)
[ ] Go / Rust / Java / C#
[ ] Database: PostgreSQL / MySQL / MongoDB / etc.

Infrastructure:
[ ] Docker / Kubernetes
[ ] AWS / GCP / Azure / Vercel
[ ] CI/CD: GitHub Actions / GitLab / etc.

Testing:
[ ] Unit: Jest / Vitest / pytest / etc.
[ ] E2E: Playwright / Cypress / Selenium
[ ] Visual regression
```

### Шаг 3: Multi-Agent Mode

```
Хотите использовать multi-agent orchestration?

[ ] No — один агент делает всё (проще, дешевле, для S/M проектов)
[ ] Yes, lightweight — orchestrator + 2-3 sub-agents (для M/L проектов)
[ ] Yes, full — orchestrator + 8 specialized sub-agents (для XL проектов)

Когда выбрать:
- No: < 10K LOC, малые задачи, прототипы
- Lightweight: 10K-100K LOC, регулярная работа
- Full: 100K+ LOC, миграции, большие команды
```

### Шаг 4: Sub-Agent Roles (если выбран Yes)

На основе выбранного стека предложить роли. Примеры пар:

**Frontend проект:**
- `analyst-architect` (универсальный)
- `analyst-ui-senior` (если есть CSS/UI работа)
- `developer-types` (если TypeScript)
- `developer-api` (если есть backend integration)
- `developer-ui` (если есть компоненты)
- `reviewer-architect` (универсальный)
- `reviewer-fe-senior` (если CSS/UI)
- `qa` (универсальный)

**Backend проект:**
- `analyst-architect`
- `analyst-database` (если есть схема БД)
- `developer-database` (миграции, ORM)
- `developer-backend` (роуты, бизнес-логика)
- `reviewer-architect`
- `reviewer-backend` (качество backend кода)
- `reviewer-security` (auth, OWASP, secrets)
- `qa`

**Mobile проект:**
- `analyst-architect`
- `developer-types` (если TS shared)
- `developer-api` (если client-server)
- `developer-mobile` (screens, navigation, native)
- `reviewer-architect`
- `qa`

**Data/ML проект:**
- `analyst-data` (профилирование данных, гипотезы)
- `developer-data` (pipelines, ETL, training)
- `reviewer-architect`
- `qa`

**DevOps / Infrastructure проект:**
- `analyst-architect`
- `developer-devops` (IaC, CI/CD, monitoring)
- `reviewer-security` (infrastructure security)
- `qa`

**Fullstack проект:** объединение Frontend + Backend.

---

### Pre-defined presets

| Preset | Roles |
|--------|-------|
| **Frontend SPA** | analyst-architect, analyst-fe-senior, developer-types, developer-api, developer-ui, reviewer-architect, reviewer-fe-senior, qa |
| **Backend API** | analyst-architect, analyst-database, developer-database, developer-backend, reviewer-architect, reviewer-backend, reviewer-security, qa |
| **Fullstack** | все из Frontend SPA + Backend API |
| **Mobile App** | analyst-architect, developer-types, developer-api, developer-mobile, reviewer-architect, qa |
| **Data Pipeline** | analyst-data, developer-data, reviewer-architect, qa |
| **Infrastructure** | analyst-architect, developer-devops, reviewer-security, qa |

### Шаг 5: Conventions

```
Какие конвенции использовать?

Git:
- Branch naming: feat/, fix/, refactor/, docs/ (default)
- Commit format: conventional commits (default)
- PR per task: yes (default)

Code:
- File size limits: components < 200 / services < 400 (default)
- Test coverage: ≥ 80% for new code (default)
- TypeScript strict / strict mode equivalent: yes (если язык поддерживает)

Architecture (опционально):
[ ] DDD (Domain Driven Design)
[ ] Hexagonal architecture
[ ] Feature-based folders
[ ] Layered architecture
[ ] Vertical slices
```

### Шаг 6: Reference / Visual

```
Есть ли reference (старый проект, design system, Figma)?

[ ] Visual reference URL (для visual-diff)
    Reference URL: __________
    Current URL:   __________
[ ] Figma file
    File key: __________
[ ] Legacy code
    Path: __________
[ ] Design system / UI kit
    Path: __________
```

---

### Шаг 7: RESEARCH.md — Persistent Project Encyclopedia (MANDATORY)

**Цель:** создать `RESEARCH.md` в корне проекта — deep-dive encyclopedia, которая отвечает на "как оно устроено" и "почему так". Читается агентом перед первой задачей в сессии. Без этого файла ни одна задача не может быть взята в работу.

**Подход зависит от `project.type`:**

#### Type = `greenfield` (новый проект с нуля)

RESEARCH.md создаётся из шаблона `templates/research-template.md` с пустыми секциями. Заполняется incrementally в рамках этапа 2 (Analysis) каждой задачи — каждая фича дописывает свою секцию `Phase N`.

```
Action: cp templates/research-template.md RESEARCH.md
Then: заполнить Phase 0 (Project Overview) — описание проекта, status, deployment
```

#### Type = `maintenance` или `library` (существующий код)

RESEARCH.md генерируется через **deep analysis session** — прочитать все основные файлы проекта целиком (не grep!), записать находки. Это отдельный phase, занимает время, но **окупается** на первой же задаче.

Процесс:
1. **Inventory:** `find . -type f -name "*.py" -o -name "*.ts" -o -name "*.tsx"` (or equivalent) — список основных файлов с LOC
2. **Read in full** каждый файл > 50 LOC (не grep, не первые 100 строк — полностью)
3. **Записать в RESEARCH.md** по структуре шаблона:
   - Phase 0: Project Overview — что это, deployment, sizes
   - Phase 1: Architecture — модули, импорты, data flow для типичного запроса
   - Phase 2-N: по доменам проекта (API, persistence, UI, security, и т.д.)
   - Phase final: Quirks / Gotchas / Technical Debt — то, на что легко наступить
4. **Environment vars** — полная таблица из `os.environ.get(...)` / `process.env.*`
5. **Known accepted risks** — таблица с likelihood/impact/rationale

**Размер:** целевой 400-1500 строк для среднего проекта. Если > 2000 — разбить на RESEARCH-submodule.md с оглавлением в главном.

#### Type = `migration`

Для migration-проектов RESEARCH.md — это **encyclopedia старого проекта**. Каждая analyst-stage каждой задачи ОБЯЗАНА дописать новую секцию `Phase N` (см. WORKFLOW.md Stage 2, hard rule). Этот режим уже работает, init-project просто создаёт skeleton с правильной структурой логи.

#### Type = `content` (документация)

RESEARCH.md может быть lightweight — общее описание структуры и стилей, без deep-dive в код.

---

### Шаг 8: Welcome message + next steps

После завершения всех шагов показать пользователю:

```
✅ Framework initialized for {project name}

Created files:
  - .claude/project-config.yml
  - PROJECT_KNOWLEDGE.md
  - RESEARCH.md ({type}-mode skeleton OR deep-analysis draft)
  - .claude/sub-agents/*.md ({N} roles from {preset} preset)
  - BACKLOG.md (empty sprint, status legend)
  - CHANGELOG.md (Unreleased section)

Next steps:
  1. Review RESEARCH.md — add anything important that deep-analysis missed
  2. Populate BACKLOG.md with initial tasks
  3. First task will follow the full pipeline (see WORKFLOW.md)

Hard rule: read RESEARCH.md before starting any task. If it's empty or
stale, do a deep analysis first before coding.
```

---

## Output

Создаёт следующие файлы:

### 1. `.claude/project-config.yml`

```yaml
project:
  name: "{name}"
  type: "{greenfield|migration|maintenance|library|content}"
  initialized: "{date}"

stack:
  languages: [typescript, python, ...]
  frameworks: [react, fastapi, ...]
  testing: [vitest, pytest, ...]

multi_agent:
  enabled: true
  mode: "full" # none | lightweight | full
  roles:
    - analyst-architect
    - developer-types
    - reviewer-fe-senior
    - qa

conventions:
  git:
    branch_prefix: ["feat", "fix", "refactor", "docs"]
    commit_format: "conventional"
    pr_per_task: true
  code:
    max_component_lines: 200
    max_service_lines: 400
    test_coverage: 80
  architecture: "feature-based"

reference:
  visual_diff:
    reference_url: "https://..."
    current_url: "http://localhost:3000"
  figma:
    file_key: "..."
  legacy:
    path: "../old-project"
```

### 2. `PROJECT_KNOWLEDGE.md` (filled with answers)

### 3. `.claude/sub-agents/{role}.md` (для каждой выбранной роли)

Generated from templates in `templates/sub-agent-templates/`.

### 4. `BACKLOG.md` initialized

### 5. **`RESEARCH.md` — MANDATORY** (новое, 2026-04-09)

Создаётся по шаблону `templates/research-template.md`. Для `type=greenfield` — пустой skeleton с Phase 0 заполненной. Для `type=maintenance`/`library` — **обязательная deep analysis session** прежде чем agent возьмёт первую задачу: читать все основные файлы целиком, записывать находки в Phase 0-N + Quirks/Gotchas.

**Без этого файла** core-rules.md блокирует первую задачу в проекте. Hard rule.

### 6. Welcome message с next steps

---

## Re-initialization

Если нужно изменить настройки — запустить `/init-project --reconfigure`. Это обновит config и regenerate sub-agent definitions, но НЕ удалит существующие задачи и историю.
