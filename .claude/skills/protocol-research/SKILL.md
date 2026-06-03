---
name: protocol-research
user-invocable: true
description: Protocol for data analysis and research tasks. Triggers on keywords данные, анализ, исследование, research, data, analyze, investigate, dataset. Enforces Data First Code Second — verify schema, profile, hypothesis before any code.
---

# Protocol: Data Research

## Context

- **Когда:** Работа с данными, анализ, исследование
- **Ключевые слова:** данные, parquet, csv, анализ, pandas, dataframe
- **Принцип:** DATA FIRST, CODE SECOND

---

## Requirements

### Workflow

**REQUIRED:**
1. LOAD → Загрузить, проверить доступность
2. SCHEMA → Показать структуру (types, shape, samples)
3. PROFILE → Найти риски (nulls, duplicates, anomalies)
4. HYPOTHESIS → Что хотим доказать?
5. EXPERIMENT → Один маленький тест
6. DOCUMENT → Записать по 5W+H

### Schema Analysis (MANDATORY)

**CRITICAL:**
ВСЕГДА показывать перед выводами:
```python
print(f"Shape: {df.shape}")
print(f"dtypes:\n{df.dtypes}")
print(f"head:\n{df.head()}")
print(f"nunique:\n{df.nunique()}")
print(f"nulls:\n{df.isnull().sum()}")
```

### Risk Profiling

| Risk | Check | Action |
|------|-------|--------|
| Missing data | `df.isnull().sum()` | Document, decide handling |
| Duplicates | `df.duplicated().sum()` | Investigate |
| Wrong types | Manual inspection | Convert types |
| Outliers | `df.describe()` | Investigate |

### Mini-Experiment Protocol

```python
# EXPERIMENT: [Description]
# HYPOTHESIS: [What we expect]

result = df[df['column'] == 'value'].shape[0]

print(f"Result: {result}")
print(f"Expected: {expected}")
print(f"Status: {'PASS' if result == expected else 'FAIL'}")
```

**REQUIRED:**
- Один вопрос per experiment
- Быстрый (< 30 секунд)
- Logged (print results)
- Сравнён с expectation

---

## Examples

GOOD: Schema перед выводами
```python
df = pd.read_parquet("deals.parquet")
print(f"Shape: {df.shape}")  # (1500, 25)
print(f"dtypes:\n{df.dtypes}")
print(f"nulls:\n{df.isnull().sum()}")
# → Вижу 50 nulls в manager_id

# Hypothesis: Эти записи — архивные
# Experiment:
archived = df[df['manager_id'].isnull()]['status'].value_counts()
print(archived)
# → 48 из 50 — status='archived' PASS
```

BAD: Выводы без schema
```
Данные вероятно содержат информацию о сделках...
```
Проблема: Нет фактов, нет доказательств. Confidence -40%.

---

## Critical Points

**CRITICAL:**
### Cognitive Bias Prevention:
- Survivorship: НЕ только первые N записей
- Confirmation: НЕ искать только подтверждения
- Анализируй ВСЕ данные
- Искать ОПРОВЕРЖЕНИЯ гипотезы

### Anti-patterns

- "Данные вероятно содержат..." — без проверки
- Сложный анализ сразу — маленький эксперимент сначала
- Skip schema — ВСЕГДА показывать dtypes, head, nunique

---

**Версия:** 1.1
**Связанные модули:** `base-verification.md`
