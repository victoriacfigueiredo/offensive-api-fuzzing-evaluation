# Comparative Analysis of API Fuzzing Results

## Overview

This study evaluated three API fuzzing tools — Schemathesis, RESTler, and EvoMaster — against two intentionally vulnerable REST APIs: OWASP crAPI and VAmPI.

The objective was to compare the effectiveness of each tool in terms of:

* API coverage
* Number of requests generated
* Fault discovery capability
* Types of vulnerabilities identified
* Ability to explore API workflows

The experiments were repeated three times using the same seed whenever possible, and the reported values represent the average results obtained across executions.

---

# Overall Results

| API   |         Tool | Coverage (%) | Requests | Findings | Server Errors |
| ----- | -----------: | -----------: | -------: | -------: | ------------: |
| crAPI | Schemathesis |        100.0 |     4622 |    120.0 |         15.67 |
| crAPI |      RESTler |         49.6 |   273.67 |    22.33 |         22.33 |
| crAPI |    EvoMaster |         50.0 |  7611.67 |    77.33 |         77.33 |
| VAmPI | Schemathesis |        100.0 |     1723 |     25.0 |             0 |
| VAmPI |      RESTler |         42.9 |       14 |      1.0 |             1 |
| VAmPI |    EvoMaster |        100.0 |    39280 |     12.0 |             0 |

---

# OWASP crAPI Results

## Schemathesis

Schemathesis achieved complete OpenAPI coverage and generated thousands of requests during testing.

The tool successfully identified several security issues, including:

* Authentication bypass
* Insecure Direct Object Reference (IDOR)
* Improper authentication handling
* Multiple improper error handling conditions
* Internal server errors triggered by malformed requests

Examples include:

* Access to order information without authentication.
* Access to order data belonging to other users.
* OTP validation endpoints returning HTTP 500.
* Token validation endpoints returning HTTP 500.

The findings demonstrate Schemathesis' ability to efficiently discover both authorization flaws and robustness issues.

---

## RESTler

RESTler achieved lower coverage than Schemathesis but identified several server-side failures through stateful request generation.

The confirmed findings included:

* Improper error handling in mechanic report submission.
* Improper error handling in coupon validation.
* Improper error handling in email verification.
* Improper error handling in OTP validation.
* Improper error handling in token-based authentication.

RESTler also produced additional potential findings involving:

* File upload endpoints.
* Coupon application endpoints.
* Pagination handling.
* Order return workflows.

Some of these findings were not manually reproduced and therefore remained unconfirmed.

The results indicate that RESTler was particularly effective at discovering server-side exception paths generated through API state exploration.

---

## EvoMaster

EvoMaster generated the highest number of requests among the tools and discovered a large number of faults.

Most findings were related to:

* Server-side exceptions
* Invalid state transitions
* Unexpected API responses
* Error handling weaknesses

Compared with RESTler, EvoMaster explored a larger portion of the application behavior and generated significantly more fault-inducing requests.

---

# VAmPI Results

## Schemathesis

Schemathesis achieved complete coverage of all documented operations.

The most important finding was the discovery of a debug endpoint:

```http
GET /users/v1/_debug
```

This endpoint exposed:

* Usernames
* Email addresses
* Plaintext passwords
* Administrative privileges

This represents a severe information disclosure vulnerability.

Additional findings involved:

* OpenAPI schema violations
* Response validation failures
* Incorrect content types
* Undocumented response formats

Schemathesis proved particularly effective at identifying inconsistencies between implementation and specification.

---

## RESTler

RESTler achieved partial coverage of the API.

Coverage results:

* Successful operations: 6 / 14
* Coverage: 42.9%

The primary confirmed finding was an internal server error triggered by invalid values generated during fuzzing.

Compared to the results obtained against crAPI, RESTler produced substantially fewer findings on VAmPI.

This suggests that RESTler's effectiveness is highly dependent on the complexity and statefulness of the target application.

---

## EvoMaster

EvoMaster achieved full endpoint coverage.

The tool discovered two main categories of issues:

### Schema Validation Failures

Several endpoints returned responses that did not match the OpenAPI specification.

Examples included:

* Incorrect content types
* Unexpected response structures
* Mismatched schemas

### Hidden Accessible Operations

EvoMaster identified operations that were reachable despite not being documented as supported.

Examples included:

* GET /users/v1/login
* GET /users/v1/register
* DELETE /users/v1/_debug
* DELETE /users/v1/login
* DELETE /users/v1/register

These findings indicate discrepancies between the implementation and the published API specification.

---

# Comparative Analysis

## Coverage

Schemathesis consistently achieved the highest coverage across both APIs.

RESTler obtained the lowest coverage values, particularly on VAmPI.

EvoMaster achieved full coverage on VAmPI and moderate coverage on crAPI.

---

## Request Generation

EvoMaster generated substantially more requests than the other tools.

This aggressive exploration strategy contributed to the larger number of discovered faults but also resulted in longer execution times and higher computational cost.

---

## Vulnerability Discovery

Each tool demonstrated different strengths:

### Schemathesis

Best at:

* Authentication flaws
* Authorization flaws
* IDOR vulnerabilities
* Specification inconsistencies

### RESTler

Best at:

* Stateful workflow exploration
* Server-side exception discovery
* Invalid state transitions

### EvoMaster

Best at:

* Large-scale input exploration
* Schema mismatch detection
* Hidden endpoint discovery
* Contract validation

---

# Key Observation

The results suggest that no single tool is sufficient to uncover all classes of API vulnerabilities.

Schemathesis, RESTler, and EvoMaster identified largely different categories of issues.

Rather than competing directly, the tools appear to complement one another:

* Schemathesis excels at specification-driven security testing.
* RESTler excels at workflow-oriented fuzzing.
* EvoMaster excels at large-scale exploration and fault discovery.

Consequently, combining multiple fuzzing approaches provides significantly broader coverage than relying on a single tool.

---

# Limitations

Several findings required manual validation.

Some faults identified by RESTler and EvoMaster could not be reproduced and were therefore not considered confirmed vulnerabilities.

In addition, differences in API complexity, authentication mechanisms, and application state may have influenced the observed coverage and fault counts.

---

# Future Work

Future experiments may include:

* Additional REST APIs.
* GraphQL APIs.
* Authenticated and unauthenticated testing modes.
* Performance and execution time comparisons.
* False positive analysis.
* Comparison with commercial API security testing tools.

These extensions would provide a broader understanding of the strengths and limitations of modern API fuzzing approaches.
