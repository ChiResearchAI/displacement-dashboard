"""
Stand-in for the Analysis team's delivery.

THIS FILE EXISTS ONLY SO THE DEMONSTRATION HAS SOMETHING TO BUILD FROM. In the real
engagement the Analysis contractor produces this file from Data Axle Consumer data
under the Data Interface Specification in schema/, and ChiResearch never sees the
household-level records behind it.

Every number it writes is invented. It is generated from a fixed seed so that the
file is byte-identical on every machine, which is what makes the rest of the
pipeline reproducible and testable.

    python pipeline/make_sample_analysis_output.py
"""

import csv
import os

from corridors import CORRIDORS, FIRST_YEAR, LAST_YEAR

OUTPUT = os.path.join(os.path.dirname(__file__), "..", "data", "analysis_output_SAMPLE.csv")

# Project phase is given a deliberate effect, so that the dashboard's phase filter
# shows a pattern the mode-and-year filters alone cannot. Corridors under
# construction carry the strongest net outflow. This is a property of the synthetic
# generator, not a finding about the Twin Cities.
PHASE_PRESSURE = {
    "pre-development": -3,
    "planning": -7,
    "construction": -16,
    "operation": -5,
}


def stable_unit(text):
    """
    A repeatable number in [0, 1) derived from a string.

    FNV-1a, written out step by step rather than imported, so that the JavaScript in
    index.html and this Python agree exactly and the build is reproducible in both.
    """
    h = 2166374261
    for character in text:
        h = h ^ ord(character)
        h = (h * 16777619) & 0xFFFFFFFF
    h = h ^ (h >> 15)
    h = (h * 2246822507) & 0xFFFFFFFF
    h = h ^ (h >> 13)
    return (h & 0xFFFFFFFF) / 4294967296


def build_rows():
    rows = []
    for corridor in CORRIDORS:
        for station in corridor["stations"]:
            for year in range(FIRST_YEAR, LAST_YEAR + 1):
                key = f"{corridor['id']}|{station}|{year}"
                noise_a = stable_unit(key)
                noise_b = stable_unit(key + "|b")
                noise_c = stable_unit(key + "|c")

                # How many households the analysis actually counted in this cell.
                # Some land below the publication threshold, which is the point:
                # the disclosure-control step needs real small cells to act on.
                households = round(14 + noise_b * 180)

                drift = (year - FIRST_YEAR) * 0.55
                net_change = round(PHASE_PRESSURE[corridor["phase"]] + drift + (noise_a - 0.5) * 34)

                below_ami = round(34 + noise_c * 44)
                turnover = round((9 + noise_b * 13) * 10) / 10

                rows.append({
                    "corridor_id": corridor["id"],
                    "corridor_name": corridor["name"],
                    "mode": corridor["mode"],
                    "phase": corridor["phase"],
                    "station_area": station,
                    "year": year,
                    "households_counted": households,
                    "net_change_per_1000": net_change,
                    "pct_out_movers_below_80_ami": below_ami,
                    "annual_turnover_pct": turnover,
                })
    return rows


def main():
    rows = build_rows()
    path = os.path.normpath(OUTPUT)
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"wrote {len(rows)} rows to {path}")
    small_cells = sum(1 for r in rows if r["households_counted"] < 30)
    print(f"  of which {small_cells} cells fall below the publication threshold of 30 households")


if __name__ == "__main__":
    main()
