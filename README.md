# Displacement Dashboard — working build

**A functioning build of the dashboard described in ChiResearch Technologies' proposal to the
Metropolitan Council, Contract 26P232, Displacement Dashboard — Dashboard Development.**

Not a mockup and not a slide. The pipeline runs, the disclosure-control rules execute, the tests
pass, and the dashboard opens from a local disk with no server. Clone it and run it in under a
minute.

> ### Every number in this repository is synthetic
>
> The corridor names, station-area names, transit modes and project phases are real Twin Cities
> facts. **The figures attached to them are invented**, generated from a fixed seed so the build is
> reproducible on any machine. This is not Metropolitan Council data, not Data Axle data, and not a
> finding about any Twin Cities community. It exists to show the machinery, not to report a result.

---

## Run it

```bash
git clone <this repository>
cd displacement-dashboard

python pipeline/make_sample_analysis_output.py   # stands in for the Analysis team's delivery
python pipeline/build.py                         # validate, suppress, publish
python tests/test_disclosure_control.py          # prove the suppression rules work
```

Then open `index.html` in any browser. No server, no install, no network. It works from a file on
a disk, which is also how it will work the first time a Council staff member opens it.

Requires Python 3.9 or later. Nothing else — no packages to install.

---

## What the build actually does

```
[1/5] Validating data/analysis_output_SAMPLE.csv against the Data Interface Specification
      PASS
      1458 cells read, 2008-2025

[2/5] Applying disclosure control
      threshold                   : 30 households
      published                   : 1270
      suppressed, primary         : 129
      suppressed, complementary   : 59

[3/5] Stripping measured values from suppressed cells
      PASS - no suppressed cell carries a value

[4/5] Writing data/dashboard_data.json
      77,204 bytes

[5/5] Writing the data block into index.html
      index.html is now 119,664 bytes and self-contained
```

Step 3 is the one worth pausing on. Up to that point a suppressed row still holds its real numbers.
After it, the published artifact cannot leak them even if somebody opens the raw file. **The build
refuses to finish if any suppressed cell still carries a value.**

---

## Every deliverable in the Scope of Work, present in miniature

| Scope of Work task | In this repository |
|---|---|
| **Task 2** — coordinate with the Analysis Team on data structure, outputs and documentation | [`schema/data_interface_specification.md`](schema/data_interface_specification.md) — the written contract between the two contractors, and [`pipeline/validate_input.py`](pipeline/validate_input.py), the conformance validator handed to the Analysis team at no cost so they can check their own file before sending it |
| **Task 4** — online web application: map, corridors, control corridors, displacement trends, filter by mode and year | [`index.html`](index.html) — and it also filters by **transit project phase**, which the Scope of Work does not require and the Analysis research questions cannot be answered without |
| **Task 5** — communication materials, including a printable one-pager | [`onepager.html`](onepager.html) — one sheet, legible printed in black and white, no colour carrying meaning alone |
| **Task 6** — simplified, reproducible procedures and documentation so TOD staff can run annual updates | [`docs/ANNUAL_UPDATE_RUNBOOK.md`](docs/ANNUAL_UPDATE_RUNBOOK.md) — written for a competent analyst who is not a developer, with the five failures that actually happen and what to do about each |
| **Disclosure control** — the deliverable the Scope of Work does not name | [`pipeline/disclosure_control.py`](pipeline/disclosure_control.py) and [`tests/test_disclosure_control.py`](tests/test_disclosure_control.py) |
| **The limits statement** | [`docs/WHAT_THIS_DOES_AND_DOES_NOT_TELL_YOU.md`](docs/WHAT_THIS_DOES_AND_DOES_NOT_TELL_YOU.md) |

---

## Three things the dashboard does that most do not

**The project phase filter works, and it changes the picture.** Filter to construction-phase
corridors and the pattern separates from operation-phase corridors. The Analysis research questions
ask specifically during which project phase displacement occurs; without the filter, that finding is
the one the public cannot see.

**Every view has a parallel path that is not the map.** The right-hand panel is not a summary of the
map — it is the same data, as a live plain-language sentence that re-announces to assistive
technology on every filter change, a sortable keyboard-navigable table, a limits statement, and an
export with the suppression already applied. Every station area on the map is reachable by keyboard.
An interactive map encodes its whole finding in colour and position, which is exactly what a
screen-reader user cannot access; retrofitting that after a conformance test fails does not work, so
it is built alongside the map rather than after it.

**Suppressed cells are drawn as suppressed.** Hatched, labelled, and carrying the reason — including
complementary suppression. Never as zero. Never as a blank the eye reads as "no displacement here."

---

## Repository layout

```
index.html                  the dashboard, self-contained, opens from disk
onepager.html               printable communication material (Task 5)

pipeline/
  corridors.py              the network: names, modes, phases, schematic geometry
  make_sample_analysis_output.py   stands in for the Analysis team's delivery
  validate_input.py         conformance validator (given to the Analysis team)
  disclosure_control.py     small-cell and complementary suppression
  build.py                  one command regenerates every published artifact

schema/
  data_interface_specification.md  the contract between the two contractors

docs/
  ANNUAL_UPDATE_RUNBOOK.md             how TOD staff run this each year
  WHAT_THIS_DOES_AND_DOES_NOT_TELL_YOU.md   the limits statement

tests/
  test_disclosure_control.py  fourteen checks on the rules that decide what is published

data/
  analysis_output_SAMPLE.csv  1,458 synthetic cells, the shape the Analysis team delivers
  dashboard_data.json         the published artifact, post-suppression
```

---

## What this is, and what it is not

**It is** ChiResearch's own work, built for this solicitation, which Addendum No. 1 Response 4
expressly permits as a required work sample. It is a working example of the architecture the
proposal describes: an open, portable pipeline that must run every year, feeding a presentation
layer, with disclosure control encoded in code rather than applied by hand.

**It is not** deployed production software, and it is not the delivered system. Under contract the
presentation layer is built in the Council's own ArcGIS Online organisation through a partnered
collaboration, so the Council owns the content from the first week; this static page is the
companion content layer that carries the narrative, the tables and the exports alongside the Esri
map. The data is synthetic throughout.

---

## Accessibility

Built to WCAG 2.1 Level AA, which Appendix A of the RFP and the IS General Requirements and Data
Security Exhibit § 5.11(f) both require for externally facing content.

- Every station area is a focusable control with an accessible name carrying its value.
- The summary is an `aria-live` region that re-announces on every filter change.
- The data table carries the identical values the map encodes in colour, sortable and
  keyboard-operable.
- No colour carries meaning alone, in the dashboard or in the one-pager.
- Light and dark themes, both designed rather than inverted.
- The one-pager prints on one sheet in black and white without losing meaning.

---

## Who built this

**ChiResearch Technologies, LLC** — a Maryland Certified Small Business, registered and active in
SAM.gov as a Small Disadvantaged Business, minority-owned and Black-founded.

Wilfred C. Ikejiofor, Managing Member · wilfred@chiresearchai.com · 410-929-2170 ·
[chiresearchai.com](https://www.chiresearchai.com)

Prepared for Metropolitan Council RFP 26P232, November 2026.
