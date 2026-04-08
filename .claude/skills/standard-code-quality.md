---
name: standard-code-quality
description: Code quality standards reference — React Hooks rules, API pagination patterns, conventional commits, naming conventions. Use as reference when writing or reviewing code. Triggered by code style questions.
---

# Standard: Code Quality

---

## React Hooks

### Context

- **When:** Writing/modifying React components with hooks (useState, useEffect, useMemo, useCallback, useRef, etc.)
- **Critical:** Violating hook call order causes runtime errors (React Error #310, #300)

**CRITICAL:**
Hooks MUST be called in the SAME order on EVERY render!
Hooks CANNOT be called after early return statements!

### Rule #1: Hooks ALWAYS at the top of the component

- ALL hooks (useState, useEffect, useMemo, useCallback, useRef) -- at the TOP of the component
- AFTER all hooks -- early returns (loading, error)
- AFTER early returns -- remaining logic and JSX

```tsx
// CORRECT order
function MyComponent() {
  // 1. All hooks FIRST
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const processedData = useMemo(() => {
    if (!data) return null; // Check inside useMemo -- OK
    return transform(data);
  }, [data]);

  useEffect(() => { /* ... */ }, []);

  // 2. THEN early returns
  if (isLoading) return <Loader />;
  if (error) return <Error />;

  // 3. THEN remaining code and JSX
  return <div>{processedData}</div>;
}
```

### Rule #2: Hooks are NOT called conditionally

```tsx
// FORBIDDEN -- hook after condition
if (isLoading) return <Loader />;
const memoizedValue = useMemo(() => {}, []); // Error!

// FORBIDDEN -- hook inside condition
if (someCondition) {
  useEffect(() => {}, []); // Error!
}

// FORBIDDEN -- hook inside loop
items.forEach(() => {
  const [state] = useState(); // Error!
});
```

### Rule #3: Data checks -- INSIDE the hook

```tsx
// CORRECT -- check inside useMemo
const computed = useMemo(() => {
  if (!data) return defaultValue; // OK
  return processData(data);
}, [data]);

// CORRECT -- check inside useEffect
useEffect(() => {
  if (!data) return; // OK -- early exit from callback
  doSomething(data);
}, [data]);
```

### Hooks Checklist

When adding/modifying hooks:
- [ ] Hook placed BEFORE all early return statements?
- [ ] Hook NOT inside if/else/switch?
- [ ] Hook NOT inside a loop (for/while/map)?
- [ ] Hook NOT inside try/catch?
- [ ] Hook NOT inside a nested function (except custom hooks)?
- [ ] Data checks -- INSIDE hook callback, not outside?

### React Hooks Examples

**GOOD:** All hooks before early returns
```tsx
function VideoDetail({ id }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  // useMemo BEFORE early returns, check INSIDE
  const embedCode = useMemo(() => {
    if (!data) return '';
    return generateCode(data);
  }, [data]);

  useEffect(() => { loadData(id); }, [id]);

  // Early returns AFTER all hooks
  if (loading) return <Spinner />;
  if (!data) return <NotFound />;

  return <Player code={embedCode} />;
}
```

**BAD:** useMemo after early return -- CRASH!
```tsx
function VideoDetail({ id }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => { loadData(id); }, [id]);

  // Early return BEFORE useMemo
  if (loading) return <Spinner />;
  if (!data) return <NotFound />;

  // useMemo NOT called on every render!
  const embedCode = useMemo(() => generateCode(data), [data]);

  return <Player code={embedCode} />;
}
```
Result: React Error #310 "Rendered fewer hooks than expected"

### React Hooks Critical Points

- **ALWAYS:** All hooks at the top of the component, BEFORE any return
- **ALWAYS:** Data checks INSIDE hook callback (if (!data) return default)
- **NEVER:** Hooks after if/return, inside conditions, loops, try/catch
- **VERIFY:** When modifying a component -- check hook order

**Errors prevented:** React Error #310, #300

---

## API Pagination

### Context

- **When:** Writing code that loads data from a paginated API
- **Apply to:** ANY external API (REST, GraphQL) with paginated responses
- **Goal:** Prevent infinite loops and loading of excess data

**CRITICAL:**
NEVER rely ONLY on response size to stop pagination!

### Anti-pattern (FORBIDDEN)

```typescript
// WRONG -- relies only on batch size
while (hasMore) {
  const response = await api.getList({ start, limit });
  results.push(...response);

  if (response.length < limit) {  // DANGEROUS!
    hasMore = false;
  } else {
    start += limit;
  }
}
```

**Why dangerous:**
- API may return a full batch even when records are exhausted
- Some APIs (Bitrix24, Salesforce) when `start > total` return records WITHOUT filter
- Result: infinite loop or loading millions of excess records

### Correct Pattern (MANDATORY)

```typescript
// CORRECT -- uses total from API response
const MAX_RECORDS_SAFETY = 10000; // Safety limit
let total: number | null = null;

while (hasMore) {
  // 1. Get FULL response with metadata
  const rawResponse = await api.getListRaw({ start, limit });
  const items = rawResponse.result;

  // 2. Extract total from first response
  if (total === null && rawResponse.total !== undefined) {
    total = rawResponse.total;

    // 3. Safety check -- if total is unreasonably large
    if (total > MAX_RECORDS_SAFETY) {
      throw new Error(`API returned total=${total}, exceeds safety limit`);
    }
  }

  results.push(...items);

  // 4. CRITICALLY IMPORTANT: stop when reaching total
  if (total !== null && results.length >= total) {
    break;
  }

  // 5. Additional batch size check
  if (items.length < limit) {
    break;
  }

  // 6. Safety limit in case total is inaccurate
  if (results.length >= MAX_RECORDS_SAFETY) {
    throw new Error(`Reached safety limit of ${MAX_RECORDS_SAFETY}`);
  }

  start += limit;
}
```

### Pagination Checklist

When writing pagination:
- [ ] Using a method that returns the FULL response (not just `result`)
- [ ] Extracting `total` from response metadata
- [ ] Stopping when `fetched >= total`
- [ ] Safety limit as ADDITIONAL protection
- [ ] Logging `total` and `fetched` for diagnostics

### API-Specific Details

| API | Total field | Details |
|-----|-------------|---------|
| Bitrix24 REST | `response.total` | When `start > total` returns records without filter! |
| Salesforce | `totalSize` | Has `nextRecordsUrl` for pagination |
| HubSpot | `total` | Uses `after` cursor instead of offset |
| Generic REST | `meta.total`, `pagination.total` | Check documentation |

### Wrapper Methods for API Clients

When creating an API client:

```typescript
// BAD -- method discards metadata
async callMethod<T>(method: string, params: any): Promise<T> {
  const response = await this.request(method, params);
  return response.result; // total lost!
}

// GOOD -- method for full response available
async callMethodRaw<T>(method: string, params: any): Promise<ApiResponse<T>> {
  return this.request(method, params); // total preserved
}
```

### API Pagination Examples

**GOOD:** Correct pagination with total
```typescript
const deals: Deal[] = [];
let start = 0;
let apiTotal: number | null = null;

while (true) {
  const raw = await client.callMethodRaw('crm.deal.list', { filter, start, limit: 50 });

  if (apiTotal === null) {
    apiTotal = raw.total;
    logBitrix(`API reports total=${apiTotal}`);
  }

  deals.push(...raw.result);
  logBitrix(`Fetched ${deals.length}/${apiTotal}`);

  if (deals.length >= apiTotal) break;  // Main condition
  if (raw.result.length < 50) break;    // Additional

  start += 50;
}
```

**BAD:** Pagination without total
```typescript
while (hasMore) {
  const items = await client.callMethod('crm.deal.list', { filter, start, limit: 50 });
  deals.push(...items);

  if (items.length < 50) {
    hasMore = false;  // Only stop condition
  } else {
    start += 50;
  }
}
```
Problem: With API bugs (Bitrix24) may load the ENTIRE database (333000+ records) instead of 100.

### Real-World Bug Example

**Project:** crmai (2026-01-26)
**Symptom:** Sync hung for 30+ hours, loaded 333200 deals instead of 100

**Cause:**
1. Code used `callMethod` which discarded `total`
2. Stop condition: only `response.length < 50`
3. Bitrix24 API: when `start > total` returns records WITHOUT filter
4. Result: infinite loop until entire database loaded

**Solution:**
1. Use `callMethodRaw` to get `total`
2. Stop when `fetched >= total`
3. Safety limit as additional protection

### API Pagination Critical Points

**MANDATORY for pagination:**
1. **Use `total`** from API response metadata
2. **Stop** when `fetched >= total`
3. **Safety limit** as ADDITIONAL protection (not primary!)
4. **Log** total and fetched for diagnostics

**NEVER:**
- Rely only on `response.length < limit`
- Discard response metadata (`total`, `next`)
- Use safety limit as the ONLY protection

---

## Conventional Commits

Все коммиты ДОЛЖНЫ следовать формату:

```
type(scope): description
```

### Types

| Type | Когда |
|------|-------|
| `feat` | Новая функциональность |
| `fix` | Исправление бага |
| `docs` | Документация |
| `style` | Форматирование (не влияет на логику) |
| `refactor` | Рефакторинг (не fix, не feat) |
| `test` | Добавление/исправление тестов |
| `chore` | Сборка, CI, зависимости |

### Scope

Scope = модуль/фича: `auth`, `dashboard`, `api`, `store`, `router`, `i18n`, `wl`

### Примеры

```
feat(auth): add email confirmation page
fix(dashboard): double param encoding in getTransactions
refactor(store): unify RegisterPage state management to Redux
test(dashboard): add missing tests for BundleFilters
docs(workflow): add reflection stage to pipeline
chore(deps): update vitest to v4.2
```

### Правила

- Description на английском, lowercase, без точки в конце
- Не начинать с заглавной буквы
- Imperative mood: "add" не "added", "fix" не "fixed"
- Scope обязателен для feat и fix
- Scope опционален для docs, style, chore

---

**Version:** 1.1
