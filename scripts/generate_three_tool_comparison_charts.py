import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

SCHEM_INPUT = Path("results/schemathesis/summary_auto.csv")
RESTLER_INPUT = Path("results/restler/restler_run_summary.csv")
EVOMASTER_INPUT = Path("results/evomaster/summary.csv")

OUT_DIR = Path("reports/figures")
OUT_DIR.mkdir(parents=True, exist_ok=True)

schem = pd.read_csv(SCHEM_INPUT)
rest = pd.read_csv(RESTLER_INPUT)
evo = pd.read_csv(EVOMASTER_INPUT)

rest_runs = rest[rest["run"] != "mean"].copy()
evo_runs = evo[evo["run"] != "mean"].copy() if "mean" in evo["run"].values else evo.copy()

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
        "server_errors": rest_runs["reproducible_bug_buckets"].mean(),
    },
    {
        "tool": "EvoMaster",
        "coverage_percent": (evo_runs["successful_endpoints"].mean() / evo_runs["total_endpoints"].mean()) * 100,
        "requests": evo_runs["evaluated_tests"].mean(),
        "findings": evo_runs["potential_faults"].mean(),
        "server_errors": evo_runs["potential_faults"].mean(),
    },
])

summary.to_csv("results/three_tool_comparison_summary.csv", index=False)

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
    "comparison_3tools_coverage.png",
)

save_bar(
    "requests",
    "Average Tests or Requests by Tool",
    "Tests / Requests",
    "comparison_3tools_requests.png",
)

save_bar(
    "findings",
    "Average Reported Findings by Tool",
    "Findings",
    "comparison_3tools_findings.png",
)

save_bar(
    "server_errors",
    "Average Error-Related Findings by Tool",
    "Error-Related Findings",
    "comparison_3tools_server_errors.png",
)

print("Three-tool comparison charts saved in reports/figures/")
print("Summary saved in results/three_tool_comparison_summary.csv")
print(summary)