# Experimental Design

## 1. Experiment Objective

The objective of this experiment is to compare the effectiveness of fuzzing tools in detecting cybersecurity vulnerabilities in REST APIs. The tools will be evaluated in an offensive security context, simulating automated pentesting scenarios against intentionally vulnerable APIs.

The research aims to analyze which tools perform better in identifying vulnerabilities related to authentication, authorization, input validation, unexpected responses, and other insecure behaviors in REST APIs.

---

## 2. Evaluated Tools

The fuzzing tools selected for the experiments are:

- Schemathesis
- RESTler
- OWASP ZAP API Scanner
- EvoMaster

These tools were selected because they are widely used for automated REST API security testing and provide different fuzzing and endpoint exploration approaches.

---

## 3. APIs Used

The experiments will be conducted using intentionally vulnerable REST APIs executed in a controlled environment.

The selected APIs are:

- OWASP crAPI
- vulnerable-rest-api

OWASP crAPI was selected because it contains vulnerabilities aligned with the OWASP API Security Top 10, allowing the analysis of realistic offensive security scenarios.

---

## 4. Experimental Environment

The experiments will be executed locally using Docker and isolated containers to ensure reproducibility and controlled testing conditions.

The experimental environment will include:

- APIs running locally through Docker;
- Fuzzing tools executed on the same machine;
- HTTP request and log monitoring;
- Usage of OpenAPI/Swagger specifications when available.

All tools will be executed under the same computational and network conditions.

---

## 5. Experiment Variables

### Independent Variables

The independent variables are the controlled factors during the experiments:

- Fuzzing tool used;
- Target REST API;
- Tool execution configurations.

### Dependent Variables

The dependent variables correspond to the observed metrics:

- Number of detected vulnerabilities;
- Number of unexpected responses;
- Endpoint coverage;
- Number of HTTP 5xx errors;
- Execution time;
- Number of false positives;
- Ability to detect authentication and authorization flaws;
- Ability to detect input validation flaws.

---

## 6. Experimental Procedure

The experimental procedure will follow these steps:

1. Configure the vulnerable API in a Docker environment;
2. Obtain the API OpenAPI/Swagger specification;
3. Configure the fuzzing tool;
4. Execute the tool against the target API;
5. Collect logs, reports, and HTTP responses;
6. Identify detected vulnerabilities and insecure behaviors;
7. Repeat the tests for all selected tools and APIs;
8. Perform quantitative and qualitative comparisons of the results.

Each tool will be executed individually against each selected REST API.

---

## 7. Experimental Control

To ensure result comparability, the following controls will be applied:

- Same computational environment for all executions;
- Same execution time limit for each tool;
- APIs executed under the same configuration;
- Same set of available endpoints;
- Tests performed in isolated and controlled environments;
- Usage of the same OpenAPI specifications whenever applicable.