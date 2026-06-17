# Offensive API Fuzzing Evaluation

A comparative evaluation of modern API fuzzing tools using intentionally vulnerable REST APIs.

## Overview

This repository contains the artifacts, automation scripts, experimental data, and analysis produced during a comparative study of three API fuzzing tools:

* Schemathesis
* RESTler
* EvoMaster

The goal of the project is to evaluate how different fuzzing approaches perform when testing real-world REST APIs, focusing on:

* API coverage
* Fault discovery
* Vulnerability detection
* Specification compliance
* Stateful workflow exploration

The study uses vulnerable applications commonly adopted in API security research and training environments.

---

## APIs Evaluated

### OWASP crAPI

Completely Ridiculous API (crAPI) is an intentionally vulnerable API developed by OWASP to demonstrate common API security weaknesses.

Examples of vulnerabilities identified during testing include:

* Authentication bypass
* IDOR (Insecure Direct Object Reference)
* Improper error handling
* Internal server errors

---

### VAmPI

VAmPI (Vulnerable API) is a vulnerable REST API designed for API security testing and education.

Examples of vulnerabilities identified during testing include:

* Information disclosure
* Debug endpoint exposure
* Plaintext password exposure
* OpenAPI specification inconsistencies

---

## Fuzzers Evaluated

### Schemathesis

OpenAPI-based property testing and fuzzing tool focused on specification-driven API testing.

Strengths:

* High API coverage
* Schema validation
* Authentication and authorization issues
* Contract testing

---

### RESTler

Stateful REST API fuzzer developed by Microsoft Research.

Strengths:

* Stateful workflow exploration
* Dependency-aware request generation
* Server-side exception discovery

---

### EvoMaster

Evolutionary test generation tool capable of black-box API fuzzing.

Strengths:

* Large-scale input exploration
* Fault discovery
* Hidden endpoint detection
* Specification consistency testing

---

## Repository Structure

```text
.
├── apis/
│   ├── crAPI/
│   └── vampi/
│
├── configs/
│   ├── openapi/
│   └── fuzzers/
│
├── docs/
│   ├── experimental-design.md
│   ├── data-collection-plan.md
│   └── results-analysis.md
│
├── evidence/
│
├── logs/
│   ├── schemathesis/
│   ├── restler/
│   └── evomaster/
│
├── reports/
│   └── figures/
│
├── results/
│   ├── crapi/
│   └── vampi/
│
└── scripts/
```

---

## Experimental Methodology

Each tool was executed multiple times using fixed seeds whenever supported.

For each execution, the following metrics were collected:

* Coverage
* Number of requests generated
* Unique findings
* Server-side failures
* Specification violations

Results were manually reviewed to distinguish:

* Confirmed vulnerabilities
* Implementation bugs
* Specification inconsistencies
* False positives

---

## Running the Experiments

### Schemathesis

```bash
schemathesis run configs/openapi/api-spec.json \
  --url=http://localhost:8080
```

### RESTler

```bash
Restler fuzz-lean \
  --grammar_file Compile/grammar.py \
  --dictionary_file Compile/dict.json
```

### EvoMaster

```bash
./scripts/run_evomaster.sh run_01 12345
```

---

## Results

Detailed findings, figures, and analysis can be found in:

```text
docs/results-analysis.md
```

Generated charts are stored in:

```text
reports/figures/
```

Raw execution results are stored in:

```text
results/
```

---

## Key Observation

The experiments indicate that the evaluated fuzzers are largely complementary.

* Schemathesis excels at specification-driven security testing.
* RESTler excels at workflow-oriented exploration.
* EvoMaster excels at large-scale fault discovery.

No single tool identified all categories of issues, suggesting that combining multiple fuzzing approaches provides broader API security coverage.

---

## License

This repository is intended for academic research, security education, and experimental evaluation purposes.
