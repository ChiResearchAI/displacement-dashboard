"""
The build. One command regenerates every published artifact from the Analysis
team's file.

    python pipeline/build.py

What it does, in order:

  1. Validates the Analysis team's delivery against the Data Interface
     Specification. Stops if it does not conform.
  2. Applies disclosure control: primary suppression on small cells, then
     complementary suppression so no suppressed value can be recovered by
     subtraction.
  3. Strips the measured values out of every suppressed cell, so the published
     artifact cannot leak them.
  4. Writes data/dashboard_data.json.
  5. Writes that same data into index.html, between the generated-data markers, so
     the dashboard is a single self-contained file that works from a local disk
     with no web server and no network.

This is the procedure TOD staff run once a year. It is documented step by step for
a competent analyst who is not a developer in docs/ANNUAL_UPDATE_RUNBOOK.md.
"""

import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)

from corridors import CORRIDORS, CONTROL_CORRIDORS, FIRST_YEAR, LAST_YEAR  # noqa: E402
from disclosure_control import suppress, strip_suppressed_values, summarise  # noqa: E402
import validate_input  # noqa: E402

ANALYSIS_INPUT = os.path.join(ROOT, "data", "analysis_output_SAMPLE.csv")
JSON_OUTPUT = os.path.join(ROOT, "data", "dashboard_data.json")
HTML_TARGET = os.path.join(ROOT, "index.html")

BEGIN_MARKER = "/* ===== BEGIN GENERATED DATA"
END_MARKER = "/* ===== END GENERATED DATA ===== */"


def read_analysis_output(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            rows.append({
                "corridor_id": row["corridor_id"],
                "station_area": row["station_area"],
                "year": int(row["year"]),
                "households_counted": int(row["households_counted"]),
                "net_change_per_1000": int(float(row["net_change_per_1000"])),
                "pct_out_movers_below_80_ami": int(float(row["pct_out_movers_below_80_ami"])),
                "annual_turnover_pct": float(row["annual_turnover_pct"]),
            })
    return rows


def to_compact_records(published_rows):
    """
    Pack each published cell as a short array rather than an object.

    The dashboard reads roughly 1,500 cells. As objects that is a quarter of a
    megabyte of repeated key names; as arrays it is a third of the size, which keeps
    the single-file dashboard quick to open on a phone.

    Field order, which index.html relies on:
        0 corridor_id
        1 station_area
        2 year
        3 households_counted   (null when suppressed)
        4 net_change_per_1000  (null when suppressed)
        5 pct_out_movers_below_80_ami (null when suppressed)
        6 annual_turnover_pct  (null when suppressed)
        7 suppression          (null, "primary" or "complementary")
    """
    return [
        [
            r["corridor_id"],
            r["station_area"],
            r["year"],
            r["households_counted"],
            r["net_change_per_1000"],
            r["pct_out_movers_below_80_ami"],
            r["annual_turnover_pct"],
            r["suppression"],
        ]
        for r in published_rows
    ]


def write_html(payload_js):
    with open(HTML_TARGET, encoding="utf-8") as handle:
        html = handle.read()

    start = html.find(BEGIN_MARKER)
    end = html.find(END_MARKER)
    if start == -1 or end == -1:
        raise SystemExit(
            "index.html is missing the generated-data markers. "
            "The build will not guess where the data belongs."
        )

    head = html[:start]
    tail = html[end + len(END_MARKER):]
    block = (
        BEGIN_MARKER + " - written by pipeline/build.py, do not edit by hand ===== */\n"
        + payload_js + "\n"
        + END_MARKER
    )

    with open(HTML_TARGET, "w", encoding="utf-8") as handle:
        handle.write(head + block + tail)


def main():
    print("ChiResearch Displacement Dashboard - build")
    print("=" * 62)

    print(f"\n[1/5] Validating {os.path.relpath(ANALYSIS_INPUT, ROOT)} against the Data Interface Specification")
    problems = validate_input.validate(ANALYSIS_INPUT)
    if problems:
        print(f"      FAILED with {len(problems)} problem(s). The build stops here.")
        for problem in problems[:20]:
            print(f"        - {problem}")
        return 1
    print("      PASS")

    rows = read_analysis_output(ANALYSIS_INPUT)
    print(f"      {len(rows)} cells read, {FIRST_YEAR}-{LAST_YEAR}")

    print("\n[2/5] Applying disclosure control")
    suppress(rows)
    stats = summarise(rows)
    print(f"      threshold                   : {stats['threshold']} households")
    print(f"      published                   : {stats['cells_published']}")
    print(f"      suppressed, primary         : {stats['cells_suppressed_primary']}")
    print(f"      suppressed, complementary   : {stats['cells_suppressed_complementary']}")

    print("\n[3/5] Stripping measured values from suppressed cells")
    published = strip_suppressed_values(rows)
    leaked = [r for r in published if r["suppression"] and r["net_change_per_1000"] is not None]
    if leaked:
        print(f"      FAILED: {len(leaked)} suppressed cell(s) still carry a value. The build stops here.")
        return 1
    print("      PASS - no suppressed cell carries a value")

    payload = {
        "generated_by": "pipeline/build.py",
        "source_file": os.path.basename(ANALYSIS_INPUT),
        "data_is_synthetic": True,
        "disclosure_control": stats,
        "first_year": FIRST_YEAR,
        "last_year": LAST_YEAR,
        "corridors": CORRIDORS,
        "control_corridors": CONTROL_CORRIDORS,
        "records": to_compact_records(published),
    }

    print(f"\n[4/5] Writing {os.path.relpath(JSON_OUTPUT, ROOT)}")
    with open(JSON_OUTPUT, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, separators=(",", ":"))
    print(f"      {os.path.getsize(JSON_OUTPUT):,} bytes")

    print(f"\n[5/5] Writing the data block into {os.path.relpath(HTML_TARGET, ROOT)}")
    payload_js = "const DASHBOARD_DATA = " + json.dumps(payload, separators=(",", ":")) + ";"
    write_html(payload_js)
    print(f"      index.html is now {os.path.getsize(HTML_TARGET):,} bytes and self-contained")

    print("\n" + "=" * 62)
    print("Build complete. Open index.html in any browser - no server required.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
