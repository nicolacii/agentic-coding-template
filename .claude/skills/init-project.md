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

### 5. Welcome message с next steps

---

## Re-initialization

Если нужно изменить настройки — запустить `/init-project --reconfigure`. Это обновит config и regenerate sub-agent definitions, но НЕ удалит существующие задачи и историю.
