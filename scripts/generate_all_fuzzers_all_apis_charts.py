import json
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

OUT_DIR = Path("reports/figures")
OUT_DIR.mkdir(parents=True, exist_ok=True)

SUMMARY_OUT = Path("results/all_fuzzers_all_apis_summary.csv")
SUMMARY_OUT.parent.mkdir(parents=True, exist_ok=True)

rows = [
    # crAPI
    {
        "api": "crAPI",
        "tool": "Schemathesis",
        "coverage_percent": 100.0,
        "requests": 4622.0,
        "findings": 120.0,
        "server_errors": 15.67,
    },
    {
        "api": "crAPI",
        "tool": "RESTler",
        "coverage_percent": 49.6,
        "requests": 273.67,
        "findings": 22.33,
        "server_errors": 22.33,
    },
    {
        "api": "crAPI",
        "tool": "EvoMaster",
        "coverage_percent": 50.0,
        "requests": 7611.67,
        "findings": 77.33,
        "server_errors": 77.33,
    },

    # VAmPI
    {
        "api": "VAmPI",
        "tool": "Schemathesis",
        "coverage_percent": 100.0,
        "requests": 1723.0,
        "findings": 25.0,
        "server_errors": 0.0,
    },
    {
        "api": "VAmPI",
        "tool": "RESTler",
        "coverage_percent": 42.9,
        "requests": 14.0,
        "findings": 1.0,
        "server_errors": 1.0,
    },
    {
        "api": "VAmPI",
        "tool": "EvoMaster",
        "coverage_percent": 100.0,
        "requests": 39280.0,
        "findings": 12.0,
        "server_errors": 0.0,
    },
]

df = pd.DataFrame(rows)
df.to_csv(SUMMARY_OUT, index=False)


def save_grouped_bar(metric, title, ylabel, filename):
    pivot = df.pivot(index="api", columns="tool", values=metric)

    ax = pivot.plot(kind="bar")
    ax.set_title(title)
    ax.set_xlabel("API")
    ax.set_ylabel(ylabel)
    ax.legend(title="Tool")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(OUT_DIR / filename)
    plt.close()


def save_tool_bar(metric, title, ylabel, filename):
    labels = df["api"] + " - " + df["tool"]

    plt.figure(figsize=(10, 5))
    plt.bar(labels, df[metric])
    plt.title(title)
    plt.xlabel("API / Tool")
    plt.ylabel(ylabel)
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    plt.savefig(OUT_DIR / filename)
    plt.close()


save_grouped_bar(
    "coverage_percent",
    "Average Coverage by API and Fuzzer",
    "Coverage (%)",
    "all_apis_all_fuzzers_coverage_grouped.png",
)

save_grouped_bar(
    "requests",
    "Average Requests or Tests by API and Fuzzer",
    "Requests / Tests",
    "all_apis_all_fuzzers_requests_grouped.png",
)

save_grouped_bar(
    "findings",
    "Average Findings by API and Fuzzer",
    "Findings",
    "all_apis_all_fuzzers_findings_grouped.png",
)

save_grouped_bar(
    "server_errors",
    "Average Server Errors by API and Fuzzer",
    "Server Errors",
    "all_apis_all_fuzzers_server_errors_grouped.png",
)

save_tool_bar(
    "coverage_percent",
    "Coverage Across All Experiments",
    "Coverage (%)",
    "all_experiments_coverage.png",
)

save_tool_bar(
    "findings",
    "Findings Across All Experiments",
    "Findings",
    "all_experiments_findings.png",
)

print(f"Summary saved in {SUMMARY_OUT}")
print("Charts saved in reports/figures/")
print(df)
