import re
import csv
from pathlib import Path

LOG_DIR = Path("logs/schemathesis")
OUT_FILE = Path("results/schemathesis/summary_auto.csv")

patterns = {
    "operations": r"Operations:\s+(\d+) selected / (\d+) total",
    "scenarios": r"Scenarios:\s+(\d+)",
    "api_links": r"API Links:\s+(\d+) covered / (\d+) selected / (\d+) total",
    "stateful": r"✅\s+(\d+) passed\s+❌\s+(\d+) failed",
    "test_cases": r"(\d+) generated,\s+(\d+) found\s+(\d+) unique failures,\s+(\d+) skipped",
    "seed": r"Seed:\s+(\d+)",
    "duration": r"=+\s+\d+ failures,\s+\d+ warnings in ([\d.]+)s",
}

failure_types = [
    "API accepts requests without authentication",
    "Server error",
    "Response violates schema",
    "API accepted schema-violating request",
    "API rejected schema-compliant request",
    "Malformed media type",
    "Missing header not rejected",
    "Resource is not available after creation",
    "Undocumented Content-Type",
    "Undocumented HTTP status code",
]

def extract_last_stateful_counts(text):
    matches = re.findall(patterns["stateful"], text)
    if matches:
        return matches[-1]
    return ("", "")

def analyze_log(path):
    text = path.read_text(errors="ignore")

    row = {
        "file": path.name,
        "tool": "Schemathesis",
        "api": "crAPI",
    }

    ops = re.search(patterns["operations"], text)
    row["operations_selected"] = ops.group(1) if ops else ""
    row["operations_total"] = ops.group(2) if ops else ""

    scenarios = re.search(patterns["scenarios"], text)
    row["stateful_scenarios"] = scenarios.group(1) if scenarios else ""

    links = re.search(patterns["api_links"], text)
    row["api_links_covered"] = links.group(1) if links else ""
    row["api_links_selected"] = links.group(2) if links else ""
    row["api_links_total"] = links.group(3) if links else ""

    passed, failed = extract_last_stateful_counts(text)
    row["stateful_passed"] = passed
    row["stateful_failed"] = failed

    test_cases = re.search(patterns["test_cases"], text)
    if test_cases:
        row["test_cases_generated"] = test_cases.group(1)
        row["test_cases_found"] = test_cases.group(2)
        row["unique_failures"] = test_cases.group(3)
        row["test_cases_skipped"] = test_cases.group(4)
    else:
        row["test_cases_generated"] = ""
        row["test_cases_found"] = ""
        row["unique_failures"] = ""
        row["test_cases_skipped"] = ""

    seed = re.search(patterns["seed"], text)
    row["seed"] = seed.group(1) if seed else ""

    duration = re.search(patterns["duration"], text)
    row["duration_seconds"] = duration.group(1) if duration else ""

    for failure in failure_types:
        regex = rf"{re.escape(failure)}:\s+(\d+)"
        match = re.search(regex, text)
        key = failure.lower().replace(" ", "_").replace("-", "_")
        row[key] = match.group(1) if match else "0"

    return row

def main():
    logs = sorted(LOG_DIR.glob("authenticated_run_fixed_seed_*.log"))

    if not logs:
        print("No Schemathesis logs found.")
        return

    rows = [analyze_log(log) for log in logs]

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUT_FILE.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved summary to {OUT_FILE}")

if __name__ == "__main__":
    main()
