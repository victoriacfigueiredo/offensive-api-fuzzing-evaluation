# Finding: Improper Error Handling in OTP Validation Endpoint

## Summary

The Schemathesis fuzzing tool identified that the OTP validation endpoint returns an Internal Server Error (HTTP 500) when receiving invalid input instead of handling the request gracefully.

## Endpoint

```http
POST /identity/api/auth/v2/check-otp
```

## Discovery Method

Detected automatically during stateful fuzzing with Schemathesis and manually validated.

## Reproduction Steps

### Request

```bash
curl -i -X POST http://localhost:8888/identity/api/auth/v2/check-otp \
-H "Content-Type: application/json" \
-d '{"otp":"","password":"","email":""}'
```

### Response

```http
HTTP/1.1 500 Internal Server Error
Content-Type: text/plain;charset=UTF-8

User was not found for parameters {userEmail=}
```

## Expected Behavior

The API should reject invalid input using a client-side error code, such as:

```http
400 Bad Request
```

or

```http
422 Unprocessable Entity
```

with an appropriate validation message.

## Security Impact

Although this issue does not directly allow unauthorized access, it demonstrates insufficient input validation and improper error handling. Internal server errors may expose implementation details and reduce the robustness of the application.

## Classification

* CWE-20: Improper Input Validation
* CWE-755: Improper Handling of Exceptional Conditions

## Severity

Medium

## Status

Confirmed

## Detected By

Schemathesis
