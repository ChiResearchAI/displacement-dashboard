# What this does and does not tell you

**Deliverable 5.3.** One page, in plain language, that appears on the dashboard, in the web content
and in both printable one-pagers.

ChiResearch proposes this as a named deliverable because it is the difference between a dashboard
the Council can stand behind and a dashboard the Council has to defend. It is the cheapest insurance
in the contract.

---

## What the analysis measures

Annual household movement in and out of station areas along the region's high-frequency transit
corridors, from 2008 to 2025, compared against control corridors that have no frequent transit.
Movement is broken down by income relative to area median, by race and ethnicity, and by the phase
the transit project had reached in that year.

## What it does tell you

It tells you **the direction and size of measured household movement** in a named place in a named
year, and how that compares with a similar place that did not get frequent transit.

Where outflow of lower-income households coincides with inflow of higher-income households,
repeatedly, in a corridor, and not in its control corridor, that is a pattern worth the Council's
attention. Identifying those places early is the point of the dashboard.

## What it does not tell you

**It does not tell you that any household was forced to move.**

Household movement is an *indicator* of displacement. It is not displacement itself. The Council's
own Anti-Displacement Framework, in Imagine 2050, describes displacement as the physical and
involuntary — often violent — loss of one's home, community, or access to resources. A consumer-data
record cannot distinguish an eviction from a promotion, a family moving closer to work from a family
priced out of its block.

The Scope of Work concedes this directly when it asks whether anything in the data "can help us
identify whether movement is voluntary or forced displacement." The honest answer is that it narrows
the question. It does not answer it.

**It does not establish that transit investment caused the movement.** Comparing a corridor against
a control corridor rules out some competing explanations. It does not rule out all of them.

**It does not speak for the people it counts.** The framework holds that displacement is ultimately
defined by the residents of an impacted community. This analysis is one input to that conversation.
It is not a substitute for having it.

## Why some values are missing

A station area is **suppressed** when the number of households behind a figure falls below the
publication threshold. A small cell on a public map can re-identify a household, and this is a public
tool.

A second station area in the same corridor may be suppressed even when its own count clears the
threshold. That is **complementary suppression**: without it, a single suppressed value could be
recovered by subtracting the published ones from a corridor total.

Suppressed cells are drawn as suppressed, with the reason attached. **They are never drawn as zero,
and never left as a gap the eye reads as "no displacement here."** Those two failures are the most
common way a dashboard like this misleads, and they are both avoidable.

## Where the numbers come from

Every figure the dashboard displays traces to:

1. the Analysis team's output file for that cycle,
2. the transformation the pipeline applied to it, which is in `pipeline/` and readable,
3. the suppression rule that governed its release, which is in
   `pipeline/disclosure_control.py` and tested in `tests/`.

In this demonstration repository they trace to a seeded random generator and nowhere else. **Every
number here is invented.**

## How to use a finding responsibly

- **Quote the geography and the year.** A regional figure and a station-area figure are different
  claims.
- **Say "measured net household outflow," not "displacement,"** unless you mean the framework's
  definition and have more than this data behind you.
- **Carry the suppression with the finding.** "Four of the eleven station areas on this corridor are
  suppressed" is part of the result, not a footnote to it.
- **Check the control corridor** before attributing a pattern to transit.
