# Finding: Improper Authentication Handling in User Dashboard Endpoint

## Summary

The Schemathesis fuzzing tool identified inconsistent authentication handling in the user dashboard endpoint. During manual validation, requests without a valid JWT token did not return the expected authentication error (`401 Unauthorized`). Instead, the application returned a `404 Not Found` response indicating that the user was not registered.

## Endpoint

```http
GET /identity/api/v2/user/dashboard
```

## Discovery Method

Detected automatically during Schemathesis fuzzing and manually validated using curl.

## Reproduction Steps

### Request Without Authentication

```bash
curl -i http://localhost:8888/identity/api/v2/user/dashboard
```

### Response

```http
HTTP/1.1 404 Not Found
```

```json
{
  "message": "Given Email is not registered!",
  "status": 404
}
```

### Request With Invalid JWT

```bash
curl -i -H "Authorization: Bearer abc" \
http://localhost:8888/identity/api/v2/user/dashboard
```

### Response

```http
HTTP/1.1 404 Not Found
```

```json
{
  "message": "Given Email is not registered!",
  "status": 404
}
```

### Request With Valid JWT

```bash
curl -i -H "Authorization: Bearer <VALID_TOKEN>" \
http://localhost:8888/identity/api/v2/user/dashboard
```

### Response

```http
HTTP/1.1 200 OK
```

```json
{
  "id": 8,
  "name": "barbara milicent roberts",
  "email": "barbie@email.com",
  "role": "ROLE_USER"
}
```

## Expected Behavior

Requests without authentication or with an invalid JWT should be rejected with:

```http
401 Unauthorized
```

The endpoint should not process the request as if it were associated with a non-existent user.

## Security Impact

No authentication bypass was observed. However, the endpoint handles authentication failures inconsistently by returning a resource-related error (`404 Not Found`) instead of an authentication-related error (`401 Unauthorized`).

This behavior:

* Makes API behavior harder to reason about and test.
* May leak implementation details about how user identities are resolved.
* Can complicate monitoring, logging, and security tooling that relies on standard HTTP authentication semantics.

## Classification

* CWE-388: Error Handling
* CWE-670: Always-Incorrect Control Flow Implementation
* API Design / Authentication Handling Issue

## Severity

Low

## Status

Confirmed

## Detected By

Schemathesis
