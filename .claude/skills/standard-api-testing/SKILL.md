---
name: standard-api-testing
user-invocable: true
description: API testing patterns with authentication — how to test endpoints requiring auth tokens, mocking strategies, integration vs unit testing. Use when writing API tests.
---

# Standard: API Testing with Auth

> Паттерн тестирования API endpoints, требующих авторизацию.
> Запуск: `/standard-api-testing` или при тестировании protected API

---

## Когда применять

- При тестировании API endpoints через curl
- При написании integration tests для authenticated routes
- При проверке API после деплоя

---

## Два уровня авторизации

| Уровень | Когда нужен | Как получить |
|---------|-------------|--------------|
| **Basic Auth** | Nginx/proxy layer | Credentials из env или secrets |
| **Session/Cookie Auth** | API endpoints | Login endpoint → save cookies |
| **Token Auth (JWT)** | Stateless API | Login → получить token → header |

## Процесс тестирования

### 1. Получить session

```bash
# Cookie-based auth (как в Albato):
curl -c /tmp/session.txt \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"..."}' \
  "https://domain/api/auth/login"

# Token-based auth:
TOKEN=$(curl -s -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"..."}' \
  "https://domain/api/auth/login" | jq -r '.token')
```

### 2. Использовать session для запросов

```bash
# Cookie:
curl -b /tmp/session.txt "https://domain/api/protected/endpoint"

# Token:
curl -H "Authorization: Bearer $TOKEN" "https://domain/api/protected/endpoint"
```

### 3. Cleanup

```bash
rm /tmp/session.txt
```

---

## Правила

- **ВСЕГДА** авторизоваться перед тестированием protected endpoints
- **НИКОГДА** не хардкодить пароли в скриптах или правилах
- **CLEANUP** session files после тестов
- **SECURITY** credentials только из env vars или secrets (не в git)
- Тестовый пользователь должен иметь доступ к тестируемым endpoints
