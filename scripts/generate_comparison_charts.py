import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

SCHEMA_INPUT = Path("results/schemathesis/summary_auto.csv")
RESTLER_INPUT = Path("results/restler/restler_run_summary.csv")
OUT_DIR = Path("reports/figures")
OUT_DIR.mkdir(parents=True, exist_ok=True)

schem = pd.read_csv(SCHEMA_INPUT)
rest = pd.read_csv(RESTLER_INPUT)

rest_runs = rest[rest["run"] != "mean"].copy()

summary = pd.DataFrame([
    {
        "tool": "Schemathesis",
        "coverage_percent": 100.0,
        "requests": schem["test_cases_generated"].mean(),
        "findings": schem["unique_failures"].mean(),
        "server_errors": schem["server_error"].mean(),
    },
    {
        "tool": "RESTler",
        "coverage_percent": rest_runs["coverage_percent"].mean(),
        "requests": rest_runs["total_requests_sent"].mean(),
        "findings": rest_runs["reproducible_bug_buckets"].mean(),
        "server_errors": (
            rest_runs["reproducible_bug_buckets"].mean()
        ),
    },
])

summary.to_csv("results/comparison_summary.csv", index=False)

def save_bar(column, title, ylabel, filename):
    plt.figure()
    plt.bar(summary["tool"], summary[column])
    plt.title(title)
    plt.xlabel("Tool")
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(OUT_DIR / filename)
    plt.close()

save_bar(
    "coverage_percent",
    "Average Specification Coverage by Tool",
    "Coverage (%)",
    "comparison_coverage.png",
)

save_bar(
    "requests",
    "Average Requests Generated/Sent by Tool",
    "Requests",
    "comparison_requests.png",
)

save_bar(
    "findings",
    "Average Findings by Tool",
    "Findings",
    "comparison_findings.png",
)

save_bar(
    "server_errors",
    "Average Server Error Findings by Tool",
    "Server Error Findings",
    "comparison_server_errors.png",
)

print("Comparison charts saved in reports/figures/")
print("Summary saved in results/comparison_summary.csv")
print(summary)