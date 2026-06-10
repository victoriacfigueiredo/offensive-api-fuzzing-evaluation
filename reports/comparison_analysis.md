# Comparative Analysis: Schemathesis vs RESTler

## 1. Experiment Overview

This experiment compares two REST API fuzzing tools, Schemathesis and RESTler, using the OWASP crAPI application as the target API.

Both tools were executed against the same OpenAPI specification and the same local crAPI deployment. The goal was to compare their effectiveness in terms of API coverage, number of generated or sent requests, reproducible findings, and ability to explore stateful API behavior.

---

## 2. Schemathesis Execution

Schemathesis was executed using the OpenAPI specification and an authenticated bearer token.

The tool was able to process all 44 operations described in the specification. Across the three executions, Schemathesis generated thousands of test cases and reached full API coverage.

Schemathesis behaved as a more plug-and-play tool in this setup. After providing the schema, base URL, and authentication header, it was able to execute the experiment without requiring manual changes to the generated test logic.

![Schemathesis Unique Failures](figures/schemathesis_unique_failures.png)

![Schemathesis API Links Covered](figures/schemathesis_api_links_covered.png)

![Schemathesis Stateful Scenarios](figures/schemathesis_stateful_scenarios.png)

![Schemathesis Server Errors](figures/schemathesis_server_errors.png)

---

## 3. RESTler Execution

RESTler required more manual setup before producing comparable results.

Initially, RESTler achieved very low coverage because the authentication token was not being correctly inserted into the generated requests. The grammar contained an `authentication_token_tag` placeholder, but the configured token refresh command was not properly reflected in the requests.

To make the experiment fair, the generated RESTler grammar was manually adjusted to include a valid `Authorization: Bearer` header. After this correction, RESTler's coverage increased significantly.

A second issue was caused by the `/workshop/api/shop/return_qr_code` endpoint, which returns `image/png`. During fuzzing, RESTler attempted to process this binary response as UTF-8 text and failed with a `UnicodeDecodeError`. To prevent this tool-level crash, this endpoint was removed from the RESTler grammar for the final experimental runs.

After these adjustments, RESTler was executed three times using the same grammar, custom dictionary, and random seed.

Final RESTler results:

- Average coverage: 21.33 / 43 operations
- Average coverage percentage: 49.6%
- Average rendered requests: 36.67 / 43
- Average valid requests: 21.33
- Average total requests sent: 273.67
- Average dynamic objects created: 172.67
- Average reproducible bug buckets: 22.33

![RESTler Coverage](figures/restler_coverage.png)

![RESTler Valid Requests](figures/restler_valid_requests.png)

![RESTler Requests Sent](figures/restler_requests_sent.png)

![RESTler Objects Created](figures/restler_objects_created.png)

![RESTler Reproducible Findings](figures/restler_reproducible_findings.png)

---

## 4. Comparative Results

The comparison shows that Schemathesis achieved higher API coverage and generated a much larger number of test cases. RESTler, on the other hand, showed stronger stateful behavior by creating many dynamic objects and using specialized checkers such as `InvalidDynamicObjectChecker`.

![Comparison Coverage](figures/comparison_coverage.png)

![Comparison Requests](figures/comparison_requests.png)

![Comparison Findings](figures/comparison_findings.png)

![Comparison Server Errors](figures/comparison_server_errors.png)

---

## 5. Interpretation

Schemathesis was easier to configure and achieved complete API coverage in this experiment. It required fewer manual adjustments and was able to execute against the target API directly after receiving the schema, base URL, and authentication token.

RESTler required additional manual intervention. Authentication had to be inserted directly into the grammar, and the binary-response endpoint had to be removed to avoid an internal decoding error. However, once correctly configured, RESTler successfully performed stateful fuzzing, created dynamic resources, and identified several reproducible bug buckets.

This suggests that Schemathesis may be more suitable for fast and broad OpenAPI-based fuzzing, while RESTler may provide complementary value when testing stateful behavior and dependencies between API resources.

---

## 6. Confirmed RESTler Findings

The following RESTler findings were manually reproduced:

| Endpoint | Result | Evidence |
|---|---:|---|
| `/workshop/api/mechanic/receive_report` | HTTP 500 | `evidence/restler/mechanic_receive_report_500.txt` |
| `/community/api/v2/coupon/validate-coupon` | HTTP 500 | `evidence/restler/community_coupon_validate_500.txt` |
| `/identity/api/v2/user/verify-email-token` | HTTP 500 | `evidence/restler/verify_email_token_500.txt` |

Other RESTler buckets remain candidates and should be validated manually before being reported as confirmed findings.

---

## 7. Key Takeaways

- Schemathesis achieved full API coverage with less configuration effort.
- RESTler required manual grammar adjustments to properly authenticate requests.
- RESTler's execution had to exclude one binary-response endpoint due to a tool-level decoding issue.
- RESTler created dynamic objects and exposed stateful behavior that is useful for dependency-based testing.
- The tools appear complementary: Schemathesis was stronger for broad coverage, while RESTler provided deeper stateful exploration after configuration.

---

## 8. Limitations

This comparison depends on the quality of the OpenAPI specification and the compatibility of each tool with the target API. RESTler's lower coverage should be interpreted together with the required manual adjustments and the binary-response limitation observed during execution.

Additionally, not all RESTler bug buckets were manually validated. Therefore, the number of confirmed findings is lower than the number of reproduced bug buckets reported by the tool.


# Finding Coverage Matrix

| Finding                          | Endpoint                                         | Schemathesis | RESTler |
| -------------------------------- | ------------------------------------------------ | :----------: | :-----: |
| Authentication Bypass            | `/workshop/api/shop/orders/{order_id}`           |       ✅      |    ❌    |
| IDOR / Broken Access Control     | `/workshop/api/shop/orders/{order_id}`           |       ✅      |    ❌    |
| Improper Authentication Handling | `/identity/api/v2/user/dashboard`                |       ✅      |    ❌    |
| Improper Error Handling          | `/identity/api/auth/v2/check-otp`                |       ✅      |    ✅    |
| Improper Error Handling          | `/identity/api/auth/v3/check-otp`                |       ✅      |    ✅    |
| Improper Error Handling          | `/identity/api/auth/v2.7/user/login-with-token`  |       ✅      |    ✅    |
| Improper Error Handling          | `/workshop/api/mechanic/mechanic_report`         |       ✅      |    ❌    |
| Improper Error Handling          | `/workshop/api/mechanic/receive_report`          |       ❌      |    ✅    |
| Improper Error Handling          | `/community/api/v2/coupon/validate-coupon`       |       ❌      |    ✅    |
| Improper Error Handling          | `/identity/api/v2/user/verify-email-token`       |       ❌      |    ✅    |
| Improper Error Handling          | `/workshop/api/shop/orders/return_order`         |       ❌      |    ✅    |
| Improper Error Handling          | `/workshop/api/shop/apply_coupon`                |       ❌      |    ✅    |
| Improper Error Handling          | `/workshop/api/shop/orders/all`                  |       ❌      |    ✅    |
| Improper Error Handling          | `/workshop/api/merchant/contact_mechanic`        |       ❌      |    ✅    |
| Improper Error Handling          | `/identity/api/v2/user/pictures`                 |       ❌      |    ✅    |
| Improper Error Handling          | `/identity/api/v2/user/videos`                   |       ❌      |    ✅    |
| Invalid Dynamic Object Handling  | `/community/api/v2/community/posts/{id}/comment` |       ❌      |    ✅    |
| Improper Error Handling          | `/community/api/v2/community/posts/recent`       |       ❌      |    ✅*   |
| Improper Error Handling          | `/workshop/api/shop/orders`                      |       ❌      |    ✅*   |

* Finding reported by RESTler during fuzzing but not manually reproduced during validation.

---

## Summary

| Metric                           | Schemathesis | RESTler |
| -------------------------------- | :----------: | :-----: |
| Total Findings                   |       7      |    15   |
| Confirmed Findings               |       7      |    5    |
| Shared Findings                  |       3      |    3    |
| Exclusive Findings               |       4      |    12   |
| Authentication Findings          |       3      |    0    |
| Access Control Findings          |       2      |    0    |
| Improper Error Handling Findings |       4      |    14   |
| Dynamic Object Findings          |       0      |    1    |

### Findings Detected by Both Tools

1. `/identity/api/auth/v2/check-otp`
2. `/identity/api/auth/v3/check-otp`
3. `/identity/api/auth/v2.7/user/login-with-token`

### Findings Exclusive to Schemathesis

1. Authentication Bypass on `/workshop/api/shop/orders/{order_id}`
2. IDOR / Broken Access Control on `/workshop/api/shop/orders/{order_id}`
3. Improper Authentication Handling on `/identity/api/v2/user/dashboard`
4. Improper Error Handling on `/workshop/api/mechanic/mechanic_report`

### Findings Exclusive to RESTler

1. `/workshop/api/mechanic/receive_report`
2. `/community/api/v2/coupon/validate-coupon`
3. `/identity/api/v2/user/verify-email-token`
4. `/workshop/api/shop/orders/return_order`
5. `/workshop/api/shop/apply_coupon`
6. `/workshop/api/shop/orders/all`
7. `/workshop/api/merchant/contact_mechanic`
8. `/identity/api/v2/user/pictures`
9. `/identity/api/v2/user/videos`
10. `/community/api/v2/community/posts/{id}/comment`
11. `/community/api/v2/community/posts/recent`
12. `/workshop/api/shop/orders`
