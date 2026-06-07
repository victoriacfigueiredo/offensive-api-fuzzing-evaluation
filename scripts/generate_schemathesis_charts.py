import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

INPUT = Path("results/schemathesis/summary_auto.csv")
OUT_DIR = Path("reports/figures")
OUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT)
df["run"] = df["file"].str.extract(r"seed_(\d+)\.log")[0]
df["run"] = ["run_01", "run_02", "run_03"]

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
    "unique_failures",
    "Unique Failures per Schemathesis Run",
    "Unique Failures",
    "schemathesis_unique_failures.png",
)

save_bar(
    "api_links_covered",
    "API Links Covered per Schemathesis Run",
    "API Links Covered",
    "schemathesis_api_links_covered.png",
)

save_bar(
    "stateful_scenarios",
    "Stateful Scenarios per Schemathesis Run",
    "Stateful Scenarios",
    "schemathesis_stateful_scenarios.png",
)

save_bar(
    "server_error",
    "Server Errors per Schemathesis Run",
    "Server Errors",
    "schemathesis_server_errors.png",
)

print("Charts saved in reports/figures/")