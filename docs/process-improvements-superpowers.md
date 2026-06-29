# Process Improvements — Product Control + Superpowers Adoption

**Date:** 2026-06-29
**Status:** Decisions captured — NOT yet applied to rules
**Source:** End-to-end test of the Superpowers methodology (obra/superpowers) on the
Localisation Agent project (brainstorming → spec → writing-plans → TDD → review → finish).
**Owner:** Nik

> This is a working doc. It records WHAT we decided to adopt and WHY. It does NOT
> yet edit any rules. Applying it is a later, separate step (see §5 Rollout).

> ⚠️ Note: `core-rules.md` is **deprecated / no longer used** in development. The
> live rule files are **`CLAUDE.md`** and **`WORKFLOW.md`** (+ `.claude/skills/`,
> `.claude/sub-agents/`). All target-file mappings below point there. Any mapping
> is **provisional** until the §5.1 audit confirms how the current flow actually
> runs.

---

## 0. Two goals of this change

1. **Add PRODUCT CONTROL to the dev process** (the priority). Today the AI makes
   product/scope/UX decisions on its own; Nik then has to redo work or catch
   things that were never fully discussed. We want product decisions to surface
   to Nik *before* code, explicitly, not silently defaulted.
2. **Adopt the high-value parts of Superpowers** that our flow is missing or that
   are more rigorous than ours.

---

## 1. PRODUCT CONTROL (highest priority — new)

**Problem:** AI silently decides product questions (scope, behavior, UX, copy,
data model, what's in/out of MVP) → rework and surprises.

**Mechanism — a Product Decision Gate before any code on STANDARD/COMPLEX work
that changes user-facing behavior:**

### 1.1 Decision classification (the core rule)

Before coding, the AI MUST split decisions into two buckets and handle each:

| Bucket | Rule |
|--------|------|
| **Product decisions** — scope, in/out of MVP, user-facing behavior, UX flow, copy/wording, data the user sees, naming the user will read, trade-offs a user would care about | **MUST go to Nik for an explicit choice** (AskUserQuestion / numbered options). NEVER decided silently by the AI. |
| **Technical decisions** — library choice, file layout, internal naming, algorithm, test structure | AI may pick a sensible default, but **MUST state it** in the plan/response so Nik can veto. |

### 1.2 Product Decision Gate — placement (corrected 2026-06-29)

**Decided with Nik:** the gate does NOT sit between ANALYSIS and IMPLEMENT.
ANALYSIS is already about code & architecture — Nik does **not** want to be
involved there. Product control + requirement detailing happen **before**
analysis. So **WORKFLOW Stage 1 is redesigned**:

```
OLD:  1.TASK → 2.ANALYSIS(code/arch) → 3.IMPLEMENT …
NEW:  1.BRAINSTORM + TASK → 2.ANALYSIS(code/arch) → 3.IMPLEMENT …
            │
            ├─ a. Brainstorm intent (one question at a time)
            ├─ b. PRODUCT GATE — surface product decisions, Nik approves
            └─ c. Detail the task / requirements spec (the approved WHAT)
```

- **Stage 1 owns the WHAT** (problem, scope, UX, product decisions). Nik is in
  the loop here.
- **Stage 2 ANALYSIS owns the HOW** (architecture, code, data flow). AI-led,
  Nik not involved — it consumes the *already-detailed* task from Stage 1.

- **Scope (decided):** the gate fires when a task touches **user-facing
  behavior / UX / copy OR scope (what's in MVP)**. Purely technical tasks
  (refactor, bugfix with no UX change) skip the gate and the brainstorm.
- **HARD-GATE:** no analysis/code/scaffolding until Nik has approved the product
  decisions in Stage 1.
- The gate's output is a **Decisions Log** in the task file, recording *who*
  decided each item (Nik vs AI-default) so nothing is an unspoken assumption.
- One question at a time, multiple-choice preferred (from `brainstorming`).

### 1.3 Silent-assumption red flags (STOP and ask)

If the AI is about to write any of these, it must stop and surface the decision:
- "Я предположил…" / "I assumed…"
- "Логично предположить…" / "logically…"
- "Для удобства я…" / "for convenience I…"
- "Очевидно, пользователь хочет…" / "obviously the user wants…"
- Picking ONE option where 2+ reasonable product options exist, without asking.

### 1.4 One question at a time

Surface product questions **one at a time, multiple-choice preferred** (from
`brainstorming`). Avoids dumping 5 questions and getting shallow answers.

**Target files:** `CLAUDE.md` (Response Protocol — add the gate + classification),
`WORKFLOW.md` (a "Product Decision Gate" checkpoint before Implement). Optionally a
new skill `.claude/skills/product-decision-gate.md`.

**This change directly proved itself in the test:** the gate caught
"widget-in-page vs standalone app" and the "export locks the project" design flaw
*before* any code was written.

---

## 2. What to adopt from Superpowers (decided)

### 2.1 Brainstorming HARD-GATE — ✅ adopt (folds into §1)
- "No code/scaffold/implementation until the design is presented AND approved."
- "Explore project context first" → then "verify the design against the real
  code" before planning. (This is what surfaced the production-dangerous flaw.)
- **Target:** `CLAUDE.md` Response Protocol step between Plan and Execute;
  `protocol-development` skill PRE-CODE step.

### 2.2 Self-review checklists — ✅ adopt (cheap, high value)
Two explicit checklists run by the AI on its own artifacts:
- **Spec self-review:** placeholder scan · internal contradictions · scope (does
  it need decomposition?) · ambiguity (any requirement readable two ways → pick
  one, make it explicit).
- **Plan self-review:** spec-coverage (every requirement → a task?) · placeholder
  scan · **type-consistency** (signatures used in task N match task M).
- **Target:** extend `validate-from-end` skill with a "Self-review (artifact)"
  section. (Our current RAT checks the *input*; this checks the *output*.)

### 2.3 Plan-quality rules — ✅ adopt the rules, not the skill
Our analyst sub-agent already does analysis; take only Superpowers' *definition of
a good plan*:
- **"No Placeholders"** ban list: no "TODO / handle edge cases / add error
  handling / similar to Task N / write tests for the above". (Highest value.)
- **Bite-sized steps (2–5 min)** with exact file path + complete code + exact
  command + expected output.
- **`Interfaces: Consumes / Produces`** block per task (signatures the neighboring
  tasks rely on) so a task is implementable without reading siblings.
- **`Global Constraints` copied verbatim from the spec** at the top of the plan
  (this is what kept the "no immediate import / batch nightly" invariant from
  being lost).
- **Target:** analyst/developer sub-agent prompt (`.claude/sub-agents/`) +
  `templates/analysis-template.md` (add a task template).

### 2.4 Whole-branch review — ✅ strengthen ours (Superpowers most detailed here)
Take into our `/review` skill:
- **5-axis rubric:** Plan alignment · Code quality · Architecture · Testing (tests
  verify real behavior, not mocks) · Production readiness. A checklist, not "look
  at the code."
- **Severity calibration** Critical / Important / Minor; each finding =
  `file:line + what's wrong + why it matters + how to fix`. Mandatory **verdict**
  (Ready: Yes / No / With fixes). Acknowledge strengths first.
- **Read-only review** — reviewer never mutates the working tree.
- **NEW skill `receiving-review`** (we have nothing for this): response pattern
  READ → UNDERSTAND → VERIFY → EVALUATE → RESPOND → IMPLEMENT; verify external
  feedback is correct *for this codebase* before implementing; YAGNI-grep on
  "implement properly"; push back with technical reasoning; fix order
  blocking → simple → complex, test each.
- **Target:** rewrite `review` skill around the rubric; add
  `.claude/skills/receiving-review.md`; reference both in `WORKFLOW.md` stage 4.

### 2.5 Continuous execution — ✅ adopt, but resolve the conflict
- Superpowers: "don't check in with the user between tasks."
- Ours: "DONE block after EVERY response."
- **Resolution:** continuous execution applies **inside one approved plan**
  (Implement / Test / Review phases) — no "should I continue?" between tasks.
  DONE block only at a **response boundary to the user**, not after each internal
  task. Stop only on BLOCKED / genuine ambiguity / plan complete.
- **Target:** `CLAUDE.md` Execute step + `WORKFLOW.md` execution phase note.

### 2.6 BONUS — verification-before-completion — ✅ adopt (strongest single item)
Stronger version of our Confidence Formula + "no 'works' without running":
- **Iron Law:** no completion claim without **fresh verification evidence in the
  same message**.
- **Gate Function:** identify the command that proves the claim → run the full
  command → read exit code / failure count → only then claim.
- **"Claim → Requires → Not Sufficient"** table (e.g. "Bug fixed → original
  symptom test passes", not "code changed").
- **Rationalization table** ("should work / I'm confident / agent said success" →
  run it).
- **Target:** fold Iron Law + Gate Function into the `verify` skill on top of the
  Confidence Formula.

---

## 3. What NOT to adopt

- "No thanks / no performative agreement" — stylistic, optional.
- Git worktrees per task — overhead; single-dev, feature branches are enough.
- Their TDD / systematic-debugging wholesale — our `protocol-*` are equivalent.
  (Optional: borrow the TDD Iron Law "code written before the test → delete it.")
- **Keep our advantage:** Superpowers has **no reflection→rules loop**; ours does
  (`/reflection` → update rules). Do not lose it.

---

## 4. Priority order (minimum high-impact set)

1. **Product Decision Gate** (§1) — the actual pain.
2. **verification-before-completion Gate Function** (§2.6).
3. **5-axis review rubric + receiving-review** (§2.4).
4. **Self-review checklists** (§2.2).
5. Plan-quality rules (§2.3) and continuous-execution clarification (§2.5).

---

## 5. Rollout sequence (agreed with Nik — do AFTER this file)

1. **Audit current flow (super-detailed):** how development actually runs today on
   the *live Claude settings* — read `CLAUDE.md`, `WORKFLOW.md`, `.claude/skills/`,
   `.claude/sub-agents/`, `.claude/settings*`. Map the real path a task takes.
   Confirm `core-rules` is dead and what replaced it.
2. **Check template reflection:** how well the live settings are mirrored in
   `agentic-coding-template/` (drift between Nik's real `~/.claude` + project files
   and this template).
3. **Edit the live settings:** apply §1–§2 changes to the real rule files.
4. **Sync into the template:** port the same changes here so the template stays the
   source of truth for new projects.

---

## 7. AUDIT — how the current flow actually works (step 1, done 2026-06-29)

**Live rule sources (the real chain):**
1. **`~/.claude/CLAUDE.md` (global, v12.1)** — master Response Protocol: ШАГ 0
   Complexity → 1 Routing (+ Prompt Prep + RAT) → 2 Execute → 3 Verify → 4 DONE
   → 5 Post-Task. This is the always-loaded driver.
2. **per-project `CLAUDE.md`** — project specifics + a local echo of the Response
   Protocol + hard rules + file-size limits.
3. **`WORKFLOW.md`** — 7-stage pipeline: `0.GIT → 1.TASK → 2.ANALYSIS →
   3.IMPLEMENT → 4.REVIEW → 5.TEST → 6.REFLECT → 7.MERGE`.
4. **`.claude/skills/*`** — on-demand: `protocol-development` (PRE-ACTION
   Duplicate+JTBD → PLAN → TDD → VERIFY), `verify`, `review`, `validate-from-end`,
   `reflection`, `orchestrate`, etc.
5. **`.claude/sub-agents/*`** — analyst/developer/reviewer/qa roles for orchestrated
   COMPLEX tasks.

**`core-rules.md`:** still physically present and still *referenced* by global
CLAUDE.md (2×) and by skills `verify`, `reflection`, `backlog-to-rules` — but per
Nik it is **no longer the driver**. Treat references as stale; edits go to
CLAUDE.md / WORKFLOW.md, not core-rules.

### 7.1 Where each improvement injects

| Improvement | Current state | Injection point |
|-------------|---------------|-----------------|
| **Product Decision Gate** (§1) | **MISSING.** `protocol-development` has *JTBD analysis*, but that's the AI reasoning about the job — NOT surfacing product decisions to Nik for sign-off. **This is the core gap.** | **Redesign WORKFLOW Stage 1: `1.TASK` → `1.BRAINSTORM + TASK`** (brainstorm → product gate → detailed requirements), BEFORE `2.ANALYSIS`. Stage 2 stays code/arch, no user. + step in `protocol-development`; + Product Decision Gate block in global `~/.claude/CLAUDE.md`. |
| **Self-review checklists** (§2.2) | `validate-from-end` checks *work output* vs expected + gap analysis. No *artifact* self-review (placeholder scan, type-consistency of the spec/plan). | Add "Self-review (spec/plan artifact)" section to `validate-from-end`. |
| **Plan-quality rules** (§2.3) | Plans exist (`implementation-plan.md` / analyst output) but no "No Placeholders" ban, no Consumes/Produces, no verbatim Global Constraints. | analyst/developer `sub-agents/*` prompt + `templates/analysis-template.md`. |
| **Review rubric + receiving-review** (§2.4) | `review` skill = interactive BIG/SMALL, 4–5 sections (Arch/Quality/Tests/Perf/CTO). Decent, but no enforced severity+verdict rubric, no read-only-reviewer norm, **no receiving-review skill at all**. | Strengthen `review` skill (rubric + mandatory verdict + read-only); add new `receiving-review` skill; reference both in WORKFLOW **stage 4**. |
| **Verification Gate** (§2.6) | `verify` = Cross-check + Challenge + Confidence + Forbidden + RAT. Strong but no "fresh evidence in THIS message" Iron Law / Gate Function / claim→requires table. | Add to `verify` skill (on top of Confidence Formula). |
| **Continuous execution** (§2.5) | Implicit; conflicts with "DONE block every response". | Clarify in global CLAUDE.md ШАГ 2 + WORKFLOW execution note. |

## 8. AUDIT — template reflection / drift (step 2, done 2026-06-29)

- **Skills:** `~/.claude/skills/` and `agentic-coding-template/.claude/skills/` —
  **identical name set** (26 skills). Low drift on skill roster.
- **WORKFLOW.md:** template == live (Pipeline v2, same 7 stages). Low drift.
- **CLAUDE.md (corrected):** there are TWO in the template — root `CLAUDE.md` is a
  stub (how-to-use), but **`agentic-coding-template/.claude/CLAUDE.md` IS a full
  copy of the global `~/.claude/CLAUDE.md` v12.1**. So a behavioral edit to the
  global file MUST be synced into `template/.claude/CLAUDE.md` too (done for the
  Product Gate). The root stub stays as-is.
- **`core-rules` references** appeared across the template too (CLAUDE.md, README,
  AGENTS.md, WORKFLOW.md, 3 skills, 2 templates). **Cleanup DONE 2026-06-29** — all
  *functional* pointers repointed to `CLAUDE.md` / `WORKFLOW.md` (live + template).
  Only the historical version-note (`merged … v5.3 core-rules`, line 5 of both
  CLAUDE.md copies) is intentionally kept as provenance. Physical file
  `Localisation-Agent/.claude/rules/core-rules.md` still exists — pending Nik's
  decision (delete vs keep), see §9.

**Implication for §5 rollout:** the live↔template skill drift is low, so step 4
(sync) is mostly: copy the edited skills + WORKFLOW checkpoints from `~/.claude`
into the template, and update the global `~/.claude/CLAUDE.md` (which the template
does NOT mirror — it only points at it).

## 9. CHANGELOG — what's been applied

**2026-06-29 — Product Decision Gate (#1) applied** (live + template synced):
- `~/.claude/CLAUDE.md` → new **1c-PG** Product Decision Gate block.
- `~/.claude/skills/protocol-development/SKILL.md` → new **Step 1.5** Product Gate.
- `agentic-coding-template/.claude/CLAUDE.md` → 1c-PG (synced).
- `agentic-coding-template/.claude/skills/protocol-development/SKILL.md` → Step 1.5 (synced).
- `agentic-coding-template/WORKFLOW.md` → **Stage 1 redesigned** `1.TASK → 1.BRAINSTORM + TASK` (brainstorm → product gate → detail), diagram box `1.BS+TSK`, Stage 2 marked "code/arch, no user".

**2026-06-29 — items #4–#8 + plan-quality applied** (live + template synced, grep-verified):
- **#6** `verify` skill → **VERIFICATION GATE** (Iron Law fresh-evidence + Gate Function + claim→requires + rationalization stops).
- **#4** `review` skill → 5-axis rubric + severity calibration + read-only reviewer + **mandatory verdict** + pointer to `/receiving-review`.
- **#5** new skill **`receiving-review`** (response pattern, verify-before-implement, YAGNI-grep, push-back, fix order).
- **#7** `validate-from-end` → **Self-review артефакта** (spec: placeholder/contradiction/scope/ambiguity; plan: spec-coverage/placeholder/type-consistency).
- **#8** global `CLAUDE.md` ШАГ 2 → **Continuous execution** within an approved plan (no check-ins between tasks; DONE only at response boundary).
- **§2.3** `templates/analysis-template.md` → **Definition of a Good Plan** (Global Constraints verbatim, bite-sized, Consumes/Produces, No-Placeholders ban).
- Sync: edited `~/.claude` skills + `CLAUDE.md` copied into `template/.claude/*` (diff IDENTICAL).

**2026-06-29 — core-rules reference cleanup DONE** (live + template): all functional
`core-rules.md` pointers → `CLAUDE.md` / `WORKFLOW.md` across `~/.claude/CLAUDE.md`,
skills (verify, reflection, backlog-to-rules), template `WORKFLOW.md`, `README.md`,
`AGENTS.md`, `CLAUDE.md` ×2, 3 `templates/*`, `system-architecture.html`. Historical
version-note kept. Verified: 0 functional residuals (only line-5 provenance + this doc).

**Still open — Nik's decision:** physical file `Localisation-Agent/.claude/rules/core-rules.md`
(the only one that exists; auto-loads for that project only) — delete or keep?
Optional: register `/receiving-review` in the CLAUDE.md skills tables.

---

## 6. Open questions for Nik

- Product Decision Gate: should it fire on **all** STANDARD+ tasks, or only those
  touching user-facing behavior? (Default proposal: user-facing behavior + scope.)
- Should the **Decisions Log** live in the task file, the spec, or `BACKLOG.md`?
- `receiving-review` as a separate skill, or a section inside `review`?
- Is a standalone `product-decision-gate` skill wanted, or inline in `CLAUDE.md`?
