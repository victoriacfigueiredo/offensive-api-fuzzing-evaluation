import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

INPUT = Path("results/evomaster/summary.csv")
OUT_DIR = Path("reports/figures")
OUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT)

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
    "potential_faults",
    "Potential Faults per EvoMaster Run",
    "Potential Faults",
    "evomaster_potential_faults.png",
)

save_bar(
    "covered_targets",
    "Covered Targets per EvoMaster Run",
    "Covered Targets",
    "evomaster_covered_targets.png",
)

save_bar(
    "evaluated_tests",
    "Evaluated Tests per EvoMaster Run",
    "Evaluated Tests",
    "evomaster_evaluated_tests.png",
)

save_bar(
    "successful_endpoints",
    "Successfully Executed Endpoints",
    "Endpoints",
    "evomaster_successful_endpoints.png",
)

print("Charts saved in reports/figures/")