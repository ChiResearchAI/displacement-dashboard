"""
Tests for the rules that decide what may be published.

These are the tests that matter most in this repository. A defect anywhere else
makes the dashboard wrong; a defect here puts a household on a public map.

    python tests/test_disclosure_control.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pipeline"))

from disclosure_control import (  # noqa: E402
    SUPPRESSION_THRESHOLD,
    suppress,
    strip_suppressed_values,
    summarise,
)

FAILURES = []


def check(condition, description):
    if condition:
        print(f"  PASS  {description}")
    else:
        print(f"  FAIL  {description}")
        FAILURES.append(description)


def cell(corridor, station, year, households, net=5):
    return {
        "corridor_id": corridor,
        "station_area": station,
        "year": year,
        "households_counted": households,
        "net_change_per_1000": net,
        "pct_out_movers_below_80_ami": 50,
        "annual_turnover_pct": 12.0,
    }


print("Disclosure control")
print("-" * 62)

# ---------------------------------------------------------------- primary
rows = [
    cell("blue", "A", 2020, SUPPRESSION_THRESHOLD - 1),
    cell("blue", "B", 2020, SUPPRESSION_THRESHOLD),
    cell("blue", "C", 2020, 500),
    cell("blue", "D", 2020, 400),
]
suppress(rows)
check(rows[0]["suppression"] == "primary",
      f"a cell below {SUPPRESSION_THRESHOLD} households is suppressed")
check(rows[1]["suppression"] is not None,
      "a cell exactly at the threshold is not suppressed primarily, "
      "but is caught by complementary suppression here")
check(rows[1]["suppression"] == "complementary",
      "the next-smallest cell is suppressed to protect the single primary suppression")
check(rows[2]["suppression"] is None and rows[3]["suppression"] is None,
      "large cells in the same corridor-year stay published")

# ------------------------------------------------- complementary not needed
rows = [
    cell("green", "A", 2020, 10),
    cell("green", "B", 2020, 12),
    cell("green", "C", 2020, 500),
]
suppress(rows)
complementary = [r for r in rows if r["suppression"] == "complementary"]
check(len(complementary) == 0,
      "with two primary suppressions, no complementary suppression is added "
      "(subtraction cannot isolate either value)")

rows = [
    cell("gold", "A", 2020, 100),
    cell("gold", "B", 2020, 200),
]
suppress(rows)
check(all(r["suppression"] is None for r in rows),
      "with no small cells, nothing is suppressed")

# ------------------------------------------------------- isolation by group
rows = [
    cell("blue", "A", 2020, 5),
    cell("blue", "B", 2020, 600),
    cell("blue", "A", 2021, 700),
    cell("blue", "B", 2021, 800),
]
suppress(rows)
check(rows[2]["suppression"] is None and rows[3]["suppression"] is None,
      "suppression in one year does not leak into another year")

# ------------------------------------------------------------- value strip
rows = [
    cell("orange", "A", 2020, 5, net=-99),
    cell("orange", "B", 2020, 900, net=7),
]
suppress(rows)
published = strip_suppressed_values(rows)
suppressed_rows = [r for r in published if r["suppression"]]
check(all(r["net_change_per_1000"] is None for r in suppressed_rows),
      "a suppressed cell carries no measured value after stripping")
check(all(r["households_counted"] is None for r in suppressed_rows),
      "a suppressed cell carries no household count either "
      "(a count narrows the range of the suppressed value)")
check(all(r["suppression"] is not None for r in suppressed_rows),
      "a suppressed cell carries the reason, so it can be drawn as suppressed "
      "rather than as zero or as a gap")

published_rows = [r for r in published if not r["suppression"]]
check(all(r["net_change_per_1000"] is not None for r in published_rows),
      "a published cell keeps its value")

# ------------------------------------------------------------ against real data
HERE = os.path.dirname(os.path.abspath(__file__))
sample = os.path.normpath(os.path.join(HERE, "..", "data", "analysis_output_SAMPLE.csv"))
if os.path.exists(sample):
    import csv
    with open(sample, newline="", encoding="utf-8") as handle:
        real_rows = [
            {
                "corridor_id": r["corridor_id"],
                "station_area": r["station_area"],
                "year": int(r["year"]),
                "households_counted": int(r["households_counted"]),
                "net_change_per_1000": int(float(r["net_change_per_1000"])),
                "pct_out_movers_below_80_ami": int(float(r["pct_out_movers_below_80_ami"])),
                "annual_turnover_pct": float(r["annual_turnover_pct"]),
            }
            for r in csv.DictReader(handle)
        ]
    suppress(real_rows)
    stats = summarise(real_rows)
    out = strip_suppressed_values(real_rows)
    leaks = [r for r in out if r["suppression"] and r["net_change_per_1000"] is not None]

    print("\nAgainst the full sample analysis file")
    print("-" * 62)
    check(len(leaks) == 0,
          f"no suppressed cell leaks a value across all {stats['cells_total']} cells")
    check(stats["cells_suppressed_primary"] > 0,
          "the sample file contains real small cells for the rules to act on")

    # Every corridor-year must have either zero or two-or-more suppressions.
    # Exactly one is the condition complementary suppression exists to remove.
    groups = {}
    for r in real_rows:
        groups.setdefault((r["corridor_id"], r["year"]), []).append(r)
    singletons = [
        key for key, group in groups.items()
        if len([g for g in group if g["suppression"]]) == 1
    ]
    check(len(singletons) == 0,
          "no corridor-year is left with exactly one suppressed cell")

print("\n" + "=" * 62)
if FAILURES:
    print(f"{len(FAILURES)} FAILURE(S)")
    sys.exit(1)
print("All checks passed.")
