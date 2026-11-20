# Annual Update Runbook

**Who this is for:** a TOD staff member who is a competent analyst and not a developer.
**How long it takes:** about twenty minutes, most of it waiting.
**What you need:** this folder, Python 3.9 or later, and the new analysis file from the Analysis team.

This is Deliverable 6.1 in the proposal. In the real engagement, two named TOD staff run it end to
end on real data in **Month 3**, while ChiResearch is still under contract to fix whatever does not
work. Every place you hesitate is a defect in this document, not in you, and it gets fixed here
rather than explained to you.

---

## Before you start

Check that Python is available. Open a terminal in this folder and run:

```
python --version
```

You should see `Python 3.9` or higher. If the command is not found, try `python3 --version`. If
neither works, Python needs installing — ask Council IS, and use `python3` in place of `python`
everywhere below if that is the one that works.

Nothing else needs installing. The pipeline uses only what comes with Python.

---

## Step 1 — Put the new analysis file in place

The Analysis team sends one CSV each year. Save it into the `data/` folder.

Keep the previous year's file. Do not overwrite it — rename the old one with its year if you need
to, for example `analysis_output_2025.csv`. You will want it if a figure is ever questioned.

**Expected result:** the new file sits in `data/` beside the old one.

---

## Step 2 — Check the file before you build anything

```
python pipeline/validate_input.py data/analysis_output_SAMPLE.csv
```

Replace the filename with the new file's name.

**Expected result:**

```
PASS  data/analysis_output_SAMPLE.csv conforms to the Data Interface Specification.
```

**If it says FAIL**, stop. Do not continue to Step 3. The output lists each problem with the line
number it is on. Send that output to the Analysis team — it is their file to correct, and the
message tells them exactly what to fix. This is the whole point of running the check first: a
problem found here costs an email, and the same problem found after publication costs a correction
on a public map.

See *What to do when it goes wrong*, below, for the five failures that actually happen.

---

## Step 3 — Build

```
python pipeline/build.py
```

**Expected result:** five numbered steps, each reporting PASS or a count, ending with
`Build complete.` Read the disclosure-control numbers in step 2 of the output:

```
      threshold                   : 30 households
      published                   : 1270
      suppressed, primary         : 129
      suppressed, complementary   : 59
```

**Compare these to last year's.** They should be broadly similar. If the number of suppressed cells
jumps sharply, something changed in the analysis — perhaps a geography was split, perhaps a data
source thinned out. That is worth an email to the Analysis team before you publish, even though the
build will have succeeded.

The build stops by itself if any suppressed cell still carries a value. That check cannot be skipped
and is not configurable.

---

## Step 4 — Look at it

Open `index.html` by double-clicking it. It opens in any browser straight from the disk; there is no
server to start and nothing to deploy yet.

Check four things:

1. The year slider reaches the new final year.
2. Move the slider to the newest year. Station areas have colour.
3. Click the **Table** tab. Suppressed rows say `suppressed (primary)` or `suppressed (complementary)` —
   not `0`, not blank.
4. Click the **Limits** tab. The wording is still right for this year's analysis.

---

## Step 5 — Publish

Copy these files to wherever the Council hosts the dashboard:

- `index.html`
- `onepager.html`
- `data/dashboard_data.json`

Then open the published address and repeat the four checks from Step 4 against the live page, not
the local copy.

---

## Step 6 — Record what you did

Add a line to `docs/UPDATE_LOG.md` (create it the first time):

```
2027-03-14  ran by <name>  source file: analysis_output_2026.csv
            published 1,284 cells; suppressed 131 primary, 61 complementary
            notes: suppression counts in line with 2026
```

This takes a minute and it is the record that answers "where did this number come from" in 2029.

---

## What to do when it goes wrong

These are the five failures that actually happen, in the order they are likely.

### 1. `validate_input.py` reports "missing required column(s)"

The Analysis team changed their column names. **Do not rename the columns yourself to make the error
go away.** The column names are the written contract between the two contractors — see
`schema/data_interface_specification.md`. Send the error to the Analysis team. If the change is
deliberate and permanent, the specification gets updated first, then the validator, then the
pipeline, in that order.

### 2. "row count is N; the specification expects M"

Usually a station area was added or removed from a corridor, or a year is missing. If the network
genuinely changed — a line opened, a station was added — then `pipeline/corridors.py` needs the new
station added to that corridor's `stations` list, in the order the station sits on the line. That is
a one-line edit and it is the only file you should ever need to change by hand.

### 3. "unknown corridor_id" or "station_area is not on corridor"

A spelling difference between the Analysis team's file and `pipeline/corridors.py`. Check for a
changed station name — stations do get renamed. Fix it in `corridors.py` to match the Analysis
team's file, not the other way round, and note the rename in the update log.

### 4. The build says a suppressed cell still carries a value

This should be impossible and it means something is wrong in the pipeline code rather than in the
data. **Do not publish.** Stop and get a developer. Nothing in this runbook will fix it and no
workaround is safe.

### 5. The dashboard opens blank, or the map has no dots

Open the browser's developer console (F12, then the Console tab) and look for a red error. The
usual cause is that `build.py` was never run after the new file arrived, so the data block in
`index.html` is still last year's or empty. Run Step 3 again and reload.

---

## What you must not change

- **The suppression threshold** in `pipeline/disclosure_control.py`. It comes from the
  Council-approved Disclosure Control Plan. Changing it changes what is published about real
  households, and that is a decision for the named Council approver, not for the person running the
  annual update.
- **Anything between the generated-data markers** in `index.html`. The build overwrites it.
- **The field order** in `build.py`'s `to_compact_records`. The dashboard reads those positions.
