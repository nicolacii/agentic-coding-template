# Changelog

> История изменений проекта. Формат: [Keep a Changelog](https://keepachangelog.com/).
> Обновляется на этапе 7 (MERGE) каждой задачи.

## [Unreleased]

### Added
-

### Changed
- **Review process hardening (2026-07-13)** — Stage 4 ревью стало адверсариальным + confirm-pass. Каждый finding = `file:line` + `failureScenario` + `testGap` («докажи, что тесты не ловят»); ревьюер перепроверяет фикс в корне (`confirmStillBroken`). Ревью-дефолт по дорожкам: M/L/XL Workflow → reviewer **на Opus** (`REVIEW_MODEL='opus'`) + confirm + независимый слой оркестратора перед мержем; **XS/S инлайн-код тоже получает 1 независимого ревьюера** (оркестратор не self-review-and-merge кода) с возможностью ESCALATE в Workflow; trivial (docs/config/rename/test-only) — solo. Merge-block: нерешённый critical/major ИЛИ `confirmStillBroken:true`. Затронуто: `.claude/WORKFLOW.md`, `WORKFLOW.md`, `.claude/CLAUDE.md` (модель-таблица), `.claude/skills/review/SKILL.md`, `templates/review-template.md`, все `reviewer-*` sub-agent шаблоны.

### Fixed
-

### Removed
-

---

## [1.0.0] — 2026-04-08

### Added
- _пример: Groups CRUD (G-001) — see PR #42_

### Changed
-

### Fixed
-

---

## Convention

- **Added** — новая функциональность
- **Changed** — изменения существующей функциональности
- **Deprecated** — функциональность будет удалена
- **Removed** — функциональность удалена
- **Fixed** — багфиксы
- **Security** — security фиксы

Каждая запись = ссылка на PR + краткое описание для пользователя (не для разработчика).
