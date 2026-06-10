import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

INPUT = Path("results/restler/restler_run_summary.csv")
OUT_DIR = Path("reports/figures")
OUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT)

# Remove a linha da média
df = df[df["run"] != "mean"].copy()

def save_bar(column, title, ylabel, filename):
    plt.figure()
    plt.bar(df["run"], df[column])
    plt.title(title)
    plt.xlabel("Run")
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(OUT_DIR / filename)
    plt.close()

save_bar(
    "coverage_percent",
    "Specification Coverage per RESTler Run",
    "Coverage (%)",
    "restler_coverage.png",
)

save_bar(
    "valid_requests",
    "Valid Requests per RESTler Run",
    "Valid Requests",
    "restler_valid_requests.png",
)

save_bar(
    "total_requests_sent",
    "Requests Sent per RESTler Run",
    "Requests Sent",
    "restler_requests_sent.png",
)

save_bar(
    "total_object_creations",
    "Dynamic Objects Created per RESTler Run",
    "Objects Created",
    "restler_objects_created.png",
)

save_bar(
    "reproducible_bug_buckets",
    "Reproducible Findings per RESTler Run",
    "Findings",
    "restler_reproducible_findings.png",
)

print("Charts saved in reports/figures/")