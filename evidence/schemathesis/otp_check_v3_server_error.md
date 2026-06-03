# Finding: Improper Error Handling in OTP Validation Endpoint v3

## Summary

The Schemathesis fuzzing tool identified that the OTP validation endpoint v3 returns an Internal Server Error (HTTP 500) when receiving invalid or empty input. Manual validation confirmed that the endpoint does not handle malformed requests gracefully and returns a server-side error instead of a controlled client-side validation response.

## Endpoint

```http
POST /identity/api/auth/v3/check-otp
```

## Discovery Method

Detected automatically during Schemathesis fuzzing and manually validated using curl.

## Reproduction Steps

### Request

```bash
curl -i -X POST http://localhost:8888/identity/api/auth/v3/check-otp \
-H "Content-Type: application/json" \
-d '{"otp":"","password":"","email":""}'
```

### Observed Response

```http
HTTP/1.1 500 Internal Server Error
Content-Type: text/plain;charset=UTF-8

User was not found for parameters {userEmail=}
```

## Expected Behavior

The API should reject invalid or empty OTP validation input using a client error code such as:

```http
400 Bad Request
```

or

```http
422 Unprocessable Entity
```

along with a clear validation message describing the missing or invalid fields.

## Security Impact

Although this issue does not directly enable unauthorized access, it demonstrates insufficient input validation and improper exception handling.

Returning HTTP 500 for malformed requests:

* Reduces application robustness.
* Indicates that invalid input reaches internal processing logic.
* May expose implementation details through error messages.
* Can help attackers identify unexpected application behavior.

## Classification

* CWE-20: Improper Input Validation
* CWE-755: Improper Handling of Exceptional Conditions

## Severity

Medium

## Status

Confirmed

## Evidence

The endpoint consistently returned HTTP 500 when provided with empty OTP validation fields instead of rejecting the request through standard input validation.

## Detected By

Schemathesis
