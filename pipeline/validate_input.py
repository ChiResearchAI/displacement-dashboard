"""
Conformance validator for the Analysis team's delivery.

This is Deliverable 1.2 in the proposal, and in the real engagement it is handed to
the Analysis contractor at no cost in Month 2 so they can run it against their own
outputs before sending anything. It removes an entire category of Month 3 dispute:
instead of a file arriving in a shape the dashboard cannot consume, the Analysis
team sees the failure on their own machine, in their own time, with the offending
rows named.

It fails loudly. A validator that warns and continues is how a mis-mapped column
reaches a published map.

Run it directly:

    python pipeline/validate_input.py data/analysis_output_SAMPLE.csv
"""

import csv
import sys

from corridors import CORRIDORS, PHASES, FIRST_YEAR, LAST_YEAR

# The Data Interface Specification in schema/ is the written contract between the
# two contractors. This list is that contract, expressed so a machine can check it.
REQUIRED_COLUMNS = [
    "corridor_id",
    "corridor_name",
    "mode",
    "phase",
    "station_area",
    "year",
    "households_counted",
    "net_change_per_1000",
    "pct_out_movers_below_80_ami",
    "annual_turnover_pct",
]

VALID_CORRIDOR_IDS = {c["id"] for c in CORRIDORS}
VALID_MODES = {"LRT", "BRT"}
VALID_STATIONS = {(c["id"], s) for c in CORRIDORS for s in c["stations"]}


def validate(path):
    """Return a list of problems. An empty list means the file conforms."""
    problems = []

    with open(path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)

        missing = [col for col in REQUIRED_COLUMNS if col not in (reader.fieldnames or [])]
        if missing:
            problems.append(f"missing required column(s): {', '.join(missing)}")
            return problems  # Nothing else can be checked meaningfully.

        seen_keys = set()
        row_count = 0

        for line_number, row in enumerate(reader, start=2):
            row_count += 1

            corridor_id = row["corridor_id"]
            station = row["station_area"]

            if corridor_id not in VALID_CORRIDOR_IDS:
                problems.append(f"line {line_number}: unknown corridor_id '{corridor_id}'")
                continue

            if (corridor_id, station) not in VALID_STATIONS:
                problems.append(
                    f"line {line_number}: station_area '{station}' is not on corridor '{corridor_id}'"
                )

            if row["mode"] not in VALID_MODES:
                problems.append(f"line {line_number}: mode '{row['mode']}' is not LRT or BRT")

            if row["phase"] not in PHASES:
                problems.append(f"line {line_number}: phase '{row['phase']}' is not a known project phase")

            try:
                year = int(row["year"])
            except ValueError:
                problems.append(f"line {line_number}: year '{row['year']}' is not an integer")
                continue

            if not FIRST_YEAR <= year <= LAST_YEAR:
                problems.append(
                    f"line {line_number}: year {year} is outside the analysis period "
                    f"{FIRST_YEAR}-{LAST_YEAR}"
                )

            key = (corridor_id, station, year)
            if key in seen_keys:
                problems.append(f"line {line_number}: duplicate row for {station} {year}")
            seen_keys.add(key)

            # Every measure must be present and numeric. A blank here would become a
            # hole in the map, and a hole the eye reads as "no displacement".
            for column in (
                "households_counted",
                "net_change_per_1000",
                "pct_out_movers_below_80_ami",
                "annual_turnover_pct",
            ):
                value = row[column]
                if value == "":
                    problems.append(f"line {line_number}: {column} is empty")
                    continue
                try:
                    float(value)
                except ValueError:
                    problems.append(f"line {line_number}: {column} '{value}' is not a number")

        expected_rows = sum(len(c["stations"]) for c in CORRIDORS) * (LAST_YEAR - FIRST_YEAR + 1)
        if row_count != expected_rows:
            problems.append(
                f"row count is {row_count}; the specification expects {expected_rows} "
                f"(every station area, every year, no gaps)"
            )

    return problems


def main():
    if len(sys.argv) != 2:
        print("usage: python pipeline/validate_input.py <analysis_output.csv>")
        return 2

    path = sys.argv[1]
    problems = validate(path)

    if not problems:
        print(f"PASS  {path} conforms to the Data Interface Specification.")
        return 0

    print(f"FAIL  {path} does not conform. {len(problems)} problem(s):\n")
    for problem in problems[:50]:
        print(f"  - {problem}")
    if len(problems) > 50:
        print(f"  ... and {len(problems) - 50} more")
    return 1


if __name__ == "__main__":
    sys.exit(main())
