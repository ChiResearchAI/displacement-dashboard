"""
Disclosure control.

This is the module that decides what may be published. In the delivered system its
rules come from a written Disclosure Control Plan approved by a named Council
decision-maker in Month 1, and they live here in code rather than in anyone's head,
so that next year's suppression is identical to this year's without anyone
remembering to do it.

Two rules operate.

PRIMARY SUPPRESSION
    A station-area cell whose underlying household count falls below the publication
    threshold is suppressed. A small cell on a public map can re-identify a
    household, and the dashboard is a public tool.

COMPLEMENTARY SUPPRESSION
    Suppressing one cell is not enough on its own. If a corridor publishes a total
    and publishes every station area but one, the suppressed value can be recovered
    by subtraction. So when a corridor-year has exactly one primary suppression, the
    next-smallest cell in that corridor-year is suppressed as well.

Suppressed cells are never written out as zero and never written out as blank. They
carry the reason, so the presentation layer can draw them as suppressed and say why.
"""

# The minimum number of counted households a cell needs before its value may be
# published. The Disclosure Control Plan sets this; it is stated here as the single
# place the number lives.
SUPPRESSION_THRESHOLD = 30


def apply_primary_suppression(rows):
    """Mark every cell whose household count is below the threshold."""
    for row in rows:
        if row["households_counted"] < SUPPRESSION_THRESHOLD:
            row["suppression"] = "primary"
        else:
            row["suppression"] = None
    return rows


def apply_complementary_suppression(rows):
    """
    Protect each primary suppression from being recovered by subtraction.

    Group the rows by corridor and year. If exactly one cell in a group was
    suppressed primarily, the published cells plus a corridor total would give that
    value away, so suppress the next-smallest published cell in the same group.
    """
    groups = {}
    for row in rows:
        key = (row["corridor_id"], row["year"])
        groups.setdefault(key, []).append(row)

    for group_rows in groups.values():
        primary = [r for r in group_rows if r["suppression"] == "primary"]
        if len(primary) != 1:
            # Zero primary suppressions: nothing to protect.
            # Two or more: subtraction alone cannot isolate any single value.
            continue

        still_published = [r for r in group_rows if r["suppression"] is None]
        if not still_published:
            continue

        smallest = min(still_published, key=lambda r: r["households_counted"])
        smallest["suppression"] = "complementary"

    return rows


def suppress(rows):
    """Run both rules, in order. Primary first; complementary depends on its result."""
    apply_primary_suppression(rows)
    apply_complementary_suppression(rows)
    return rows


def strip_suppressed_values(rows):
    """
    Remove the measured values from every suppressed cell before publication.

    This is the step that matters. Up to this point a suppressed row still carries
    its real numbers; after it, the published artifact cannot leak them even if
    somebody reads the raw file. The household count goes too, because a count on
    its own narrows the range of the suppressed value.
    """
    published = []
    for row in rows:
        out = {
            "corridor_id": row["corridor_id"],
            "station_area": row["station_area"],
            "year": row["year"],
            "suppression": row["suppression"],
        }
        if row["suppression"] is None:
            out["households_counted"] = row["households_counted"]
            out["net_change_per_1000"] = row["net_change_per_1000"]
            out["pct_out_movers_below_80_ami"] = row["pct_out_movers_below_80_ami"]
            out["annual_turnover_pct"] = row["annual_turnover_pct"]
        else:
            out["households_counted"] = None
            out["net_change_per_1000"] = None
            out["pct_out_movers_below_80_ami"] = None
            out["annual_turnover_pct"] = None
        published.append(out)
    return published


def summarise(rows):
    """Counts for the build log, so the operator sees what the rules did."""
    total = len(rows)
    primary = sum(1 for r in rows if r["suppression"] == "primary")
    complementary = sum(1 for r in rows if r["suppression"] == "complementary")
    return {
        "cells_total": total,
        "cells_published": total - primary - complementary,
        "cells_suppressed_primary": primary,
        "cells_suppressed_complementary": complementary,
        "threshold": SUPPRESSION_THRESHOLD,
    }
