# Architecture Decision Records (ADR)

> ADR — короткие документы, фиксирующие архитектурные решения, их контекст и последствия.

## Когда создавать ADR

- Выбор технологии (Redux vs Zustand, REST vs GraphQL)
- Архитектурный паттерн (god-component → split, monolith → microservices)
- Trade-off между альтернативами
- Решение которое сложно отменить
- Решение которое влияет на будущих разработчиков

## Когда НЕ создавать

- Тривиальные решения (имя переменной, форматирование)
- Решения внутри одного файла
- Очевидные решения

## Формат имени файла

```
ADR-{NNN}-{kebab-case-title}.md

Примеры:
ADR-001-react-query-instead-of-redux-thunks.md
ADR-002-feature-based-folder-structure.md
ADR-003-tailwind-removal.md
```

## Process

1. Создать ADR файл из шаблона `templates/adr-template.md`
2. Статус: `Proposed` → обсуждение → `Accepted` / `Rejected`
3. Если решение отменено — статус `Superseded by ADR-XXX`
4. Никогда НЕ удалять ADR — только менять статус

## Index

| # | Title | Status | Date |
|---|-------|--------|------|
| _пример_ | _ADR-001 React Query vs Redux Thunks_ | _Accepted_ | _2026-04-08_ |
