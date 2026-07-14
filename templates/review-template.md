# Code Review: {Section}

> Дата: YYYY-MM-DD · Ревьюер: {agent/model} · Дорожка: XS/S-inline | M | L/XL
> **Verdict (первой строкой):** APPROVED / APPROVE-WITH-NITS / CHANGES REQUESTED

---

## Evidence gate (ДО findings)

- [ ] Прогнан ПОЛНЫЙ suite (не только новые): `N passed, M skipped`
- [ ] Typecheck: 0 errors · Build: success
- [ ] Реально изменённые файлы прочитаны (`file:line`), не только summary разработчика
- [ ] На каждый finding есть тест-доказательство (или помечен `UNVERIFIED`)

---

## Findings (по severity)

> Каждый finding обязан иметь **`failureScenario`** и **`testGap`**. Без доказанного
> testGap finding — слабый (`UNVERIFIED`). Трассируй РЕАЛЬНЫЙ steady-state, не happy-path.

### 🔴 Critical / 🟡 Major / 🟢 Minor: {название}
- **file:line:** `path:NN`
- **failureScenario:** конкретный вход/состояние → неверный выход/краш (шаги воспроизведения)
- **testGap:** какой «зелёный» тест это пропускает и почему
- **fix:** как чинить (root cause, не симптом)
- **confirmStillBroken:** true/false (заполняется на confirm-pass после фикса)

---

## Adversarial clearing (обязательно — «CLEAN because <evidence>», не пропуск)

| Категория | Verdict | Доказательство |
|-----------|---------|----------------|
| Injection (SQL/command) | CLEAN / ISSUE | |
| XSS / output encoding | CLEAN / ISSUE / N-A | |
| AuthZ / access control / tenant-scope | CLEAN / ISSUE | |
| Secrets never leak | CLEAN / ISSUE | |
| Partial-failure / idempotency (2-й запуск) | CORRECT / BROKEN | |
| Pagination / N+1 | CORRECT / ISSUE | |

---

## File Size Check

| File | Lines | Limit | Status |
|------|-------|-------|--------|
| | | | ✅/⚠️ |

---

## Confirm-pass (после фикса, ТОТ ЖЕ ревьюер)

- [ ] Причина устранена в КОРНЕ (не «тест позеленел»)
- [ ] `failureScenario` больше не воспроизводится
- [ ] `confirmStillBroken: false` по всем critical/major

---

## Verdict: APPROVED / APPROVE-WITH-NITS / CHANGES REQUESTED

**🚦 Merge-block:** любой нерешённый `critical`/`major` ИЛИ `confirmStillBroken:true` = мерж запрещён.

- APPROVE-WITH-NITS → перечислить оставшиеся minor/by-design ниты (мерж разрешён).
- CHANGES REQUESTED → fixes через `/receiving-review` → confirm-pass → повтор.
