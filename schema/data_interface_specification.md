# Data Interface Specification

**Deliverable 1.1.** The written contract between the Analysis contractor and the Dashboard
contractor, covering what the Analysis team delivers and in what shape.

In the real engagement this is drafted by ChiResearch in Month 1 and agreed by the Analysis team and
the TOD office before either side builds anything. Addendum No. 1, Responses 11 and 22, confirm the
Council intends the two teams to settle the format together; this document is ChiResearch bringing
the draft rather than waiting for one.

It is enforced by `pipeline/validate_input.py`, which the Analysis team may run against its own
outputs before sending anything. The validator and this document are kept in step: if one changes,
the other changes in the same commit.

---

## Delivery

| | |
|---|---|
| Format | UTF-8 CSV, comma-separated, one header row |
| Filename | `analysis_output_<YYYY>.csv`, where YYYY is the final year of the analysis period |
| Cadence | Once per annual cycle, plus any corrected reissues |
| Mechanism | Council-provided SharePoint, per Appendix A |
| Completeness | **Every station area, every year, no gaps.** A missing cell is an error, not an implicit zero |

## Geography

The analysis covers the seven-county Twin Cities metropolitan area. Three geographic levels appear:

- **Station area** — the unit of delivery. Every row is one station area in one year.
- **Corridor** — derived by the pipeline from `corridor_id`. Not delivered separately.
- **Region** — derived by the pipeline. Not delivered separately.

Corridor identifiers and the station areas belonging to each are fixed in
`pipeline/corridors.py` and reproduced here by reference rather than duplicated, so there is one
list rather than two that can drift apart.

Control corridors are delivered on the same terms as transit corridors, with their own
`corridor_id`.

## Columns

| Column | Type | Permitted values | Notes |
|---|---|---|---|
| `corridor_id` | string | One of the identifiers in `pipeline/corridors.py` | Lowercase, no spaces |
| `corridor_name` | string | The name the Council uses publicly | Carried for human readability; the pipeline keys on `corridor_id` |
| `mode` | string | `LRT` or `BRT` | |
| `phase` | string | `pre-development`, `planning`, `construction`, `operation` | The phase the transit project had reached **in that year**, not its phase today |
| `station_area` | string | A station area listed against that corridor | Exact match, including punctuation |
| `year` | integer | 2008–2025 | The analysis period |
| `households_counted` | integer | ≥ 0 | The denominator behind the measures. **Drives suppression** |
| `net_change_per_1000` | integer | May be negative | Net household movement per 1,000 households. Negative is net outflow |
| `pct_out_movers_below_80_ami` | integer | 0–100 | Share of out-moving households below 80% of area median income |
| `annual_turnover_pct` | number | 0–100 | Share of households that moved in or out during the year |

## Nulls, suppression and unclassifiable records

**The Analysis team does not suppress.** It delivers the full counts, including small cells, and the
Dashboard pipeline applies disclosure control. This is deliberate and it matters:

- Suppression is a publication decision governed by the Council-approved Disclosure Control Plan,
  and it belongs at the point of publication.
- Complementary suppression needs the full picture of a corridor-year to work out which second cell
  must go. A pre-suppressed file cannot support it.
- If the threshold is ever revised by the Council, the pipeline re-runs. The Analysis team does not
  have to redeliver.

Consequently: **no cell in the delivered file may be blank.** A blank is a validator failure. A
genuine zero is delivered as `0`. A record that cannot be classified to a station area is excluded
from the file and reported separately in the Analysis team's own documentation, with a count.

## Provenance metadata

Each delivery is accompanied by a short plain-text note carrying:

- the analysis period covered,
- the Data Axle vintage the analysis drew on,
- the date of generation and the person or process that generated it,
- any methodological change since the previous delivery,
- a count of records excluded as unclassifiable.

The dashboard displays the analysis period and the methodological-change note on its data-sources
panel. It is the reason a figure can be traced back three years later.

## Changing this specification

Changes are agreed in writing between the Analysis team, the TOD office and ChiResearch, and take
effect in this order:

1. This document.
2. `pipeline/validate_input.py`.
3. `pipeline/build.py` and the presentation layer.

Never the other way round. A pipeline changed to accept a file that the specification does not
describe is how a mis-mapped column reaches a published map.
