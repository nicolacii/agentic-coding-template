---
name: standard-file-size-limits
user-invocable: true
description: File size limits standard — soft and hard limits for components, services, types, and a 6-step splitting procedure when files grow too large. Use when files approach limits or for refactoring planning.
---

# Standard: File Size Limits

## Context

- Apply BEFORE creating/modifying code files
- Apply during Code Review
- Goal: prevent "monolithic" files, reduce risk of functionality loss

**CRITICAL:**
- File > soft limit = splitting plan required BEFORE adding code
- File > hard limit = MUST split before any changes

---

## Requirements

### File Size Limits

| File type | Soft limit | Hard limit | Action on exceeding |
|-----------|------------|------------|---------------------|
| Routes/Controllers | 300 lines | 600 lines | Split by domain |
| Services | 400 lines | 800 lines | Extract sub-services |
| Repositories | 400 lines | 800 lines | Split by entity |
| Analytics/Calculations | 500 lines | 1000 lines | Extract helpers/transformers |
| API client (frontend) | 300 lines | 600 lines | Split by feature |
| React components | 200 lines | 400 lines | Extract sub-components |
| Types/Interfaces | 200 lines | 400 lines | Split by domain |

### Splitting Rules

1. **Single Responsibility** -- one file = one responsibility
2. **Domain-based splitting** -- split by business domains, NOT by technical layers
3. **Barrel exports** -- create `index.ts` for re-export from directory
4. **Max 10 exports** -- file with >10 exports = candidate for splitting
5. **Dependency direction** -- dependencies go from specific to general

### Splitting Structure

**Backend (Express/Node.js):**
```
src/modules/<domain>/
  ├── <domain>.routes.ts        # Only route definitions (< 300 lines)
  ├── <domain>.controller.ts    # Request handling logic
  ├── <domain>.service.ts       # Business logic (< 400 lines)
  ├── <domain>.repository.ts    # Data access (< 400 lines)
  ├── <domain>.types.ts         # Types/interfaces
  └── index.ts                  # Barrel export
```

**Frontend (React/Next.js):**
```
lib/api/
  ├── <feature>.api.ts          # API calls for one feature (< 300 lines)
  ├── types/
  │   └── <feature>.types.ts    # Types for feature
  └── index.ts                  # Barrel export

features/<feature>/
  ├── components/               # Feature-specific components
  ├── hooks/                    # Feature-specific hooks
  ├── <feature>.types.ts        # Feature types
  └── index.ts                  # Barrel export
```

### Splitting Process

1. **Identify domains** -- list all business domains in the file
2. **Create directories** -- create directories for each domain
3. **Move incrementally** -- move code in small steps (1 domain at a time)
4. **Update imports** -- update all imports via barrel files
5. **Test after each step** -- verify functionality after each step
6. **Delete old code** -- delete old code ONLY after verifying the new code

### Naming When Splitting

| Before | After |
|--------|-------|
| `routes.ts` (everything) | `<domain>.routes.ts` (by domains) |
| `api.ts` (everything) | `<feature>.api.ts` (by features) |
| `service.ts` (large) | `<sub-domain>.service.ts` |

---

## Examples

**GOOD:** Splitting routes by domains
```
src/modules/crm/
  ├── deals/
  │   ├── deals.routes.ts       # 150 lines -- only deals endpoints
  │   ├── deals.service.ts
  │   └── index.ts
  ├── customers/
  │   ├── customers.routes.ts   # 120 lines -- only customers endpoints
  │   ├── customers.service.ts
  │   └── index.ts
  └── index.ts                  # re-exports all routers
```

**GOOD:** Splitting api.ts by features
```
lib/api/
  ├── deals.api.ts              # 180 lines -- deals API
  ├── customers.api.ts          # 90 lines -- customers API
  ├── analytics.api.ts          # 150 lines -- analytics API
  ├── types/
  │   ├── deals.types.ts
  │   └── customers.types.ts
  └── index.ts                  # export * from './deals.api'; ...
```

**BAD:** One file with everything
```
routes.ts                       # 1800 lines -- ALL endpoints in one file
api.ts                          # 1200 lines -- ALL API calls in one file
```
Problem: If the file is corrupted, ALL functionality is lost.

**BAD:** Splitting by technical layers (not by domains)
```
routes/
  ├── get-routes.ts             # all GET requests
  ├── post-routes.ts            # all POST requests
  └── put-routes.ts             # all PUT requests
```
Problem: Related logic scattered across files, hard to maintain.

---

## Critical Points

### BEFORE adding code to a file > soft limit:

1. **STOP** -- do not add code immediately
2. **CHECK** -- count current size: `wc -l <file>`
3. **PLAN** -- if > soft limit, create a splitting plan
4. **SPLIT FIRST** -- split first, then add new code
5. **TEST** -- verify everything works after splitting

### NEVER:
- Do not add code to a file > hard limit without splitting
- Do not create files `_part1.ts`, `_part2.ts`
- Do not split by technical layers (GET/POST/PUT)

### ALWAYS:
- Split by business domains
- Use barrel exports (`index.ts`)
- Test after each splitting step

---

**Version:** 1.1 (2026-02-02: expanded limits based on TechDebt Scan)
