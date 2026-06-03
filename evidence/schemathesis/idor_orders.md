# IDOR - Order Details Endpoint

Endpoint:
GET /workshop/api/shop/orders/{order_id}

Finding:
The endpoint returns order details without authentication.

Evidence:

GET /workshop/api/shop/orders/1

Response:
HTTP/1.1 200 OK

Returned data:
- User email
- Phone number
- Product information
- Payment metadata

Impact:
An attacker can enumerate order identifiers and access information belonging to other users.

Classification:
CWE-639: Authorization Bypass Through User-Controlled Key
OWASP API1:2023 Broken Object Level Authorization

Detected by:
Schemathesis