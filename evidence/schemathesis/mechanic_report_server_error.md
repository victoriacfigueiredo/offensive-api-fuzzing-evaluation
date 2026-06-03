# Finding: Improper Error Handling in Mechanic Report Endpoint

## Endpoint

GET /workshop/api/mechanic/mechanic_report

## Description

Schemathesis identified that the endpoint returns HTTP 500 when the required `report_id` parameter is omitted.

## Reproduction

### Request

curl -i -X GET http://localhost:8888/workshop/api/mechanic/mechanic_report \
-H "Authorization: Bearer <VALID_TOKEN>"

### Response

HTTP/1.1 500 Internal Server Error

### Additional Validation

report_id=0 -> 400 Bad Request

report_id=999999 -> 400 Bad Request

## Impact

The API handles invalid report identifiers correctly but fails when the required parameter is omitted, indicating improper error handling.

## Severity

Medium

## Status

Confirmed