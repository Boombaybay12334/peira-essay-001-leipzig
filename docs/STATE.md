# State document — peira-essay-001-leipzig

Freeze snapshot written 2026-11-12. Base SHA `4c9bbead0fa7aa8f31c60a8ad2a7a6deb4360613`.

---

## Table of contents

1. [Purpose and site connection](#1-purpose-and-site-connection)
2. [Repo layout](#2-repo-layout)
3. [Inputs](#3-inputs)
4. [Export format](#4-export-format)
5. [Scenario model](#5-scenario-model)
6. [Reproducibility](#6-reproducibility)
7. [CI](#7-ci)
8. [Known issues and plausibility audit](#8-known-issues-and-plausibility-audit)
9. [How-to guide](#9-how-to-guide)
10. [Starting a second research repo](#10-starting-a-second-research-repo)

---

## 1. Purpose and site connection

This repository holds the candidate research inputs and reproducible JSON export for
**PEIRA Essay 001**, *The Battle of Leipzig (1813): Strategy, Chaos, and the Fate of an Empire*.

The PEIRA site (`github.com/Boombaybay12334/PEIRA`) renders the essay. It copies the
versioned JSON export from this repository and reads it at build time. This repository
contains no site code. The connection is one-directional: research repo produces exports,
site repo consumes them via `pnpm sync:data`.

The separation means research data can be audited, versioned, and reproduced independently
of the site. Every figure in the export carries its candidate/verified status so the site
renderer cannot silently promote unverified numbers.

Evidence: `README.md` lines 5–6, `data/input/PEIRA_COMMIT.txt`. OWNER-CONFIRM (the owner
must confirm that the site's sync command is still `pnpm sync:data`).

---

## 2. Repo layout

```
peira-essay-001-leipzig/
├── AGENTS.md                        Agent rules and stop conditions
├── LICENSE                          MIT (owner must confirm assumption)
├── README.md                        Quick-start and status overview
├── pyproject.toml                   Build config; defines the `export` script entry-point
├── .python-version                  Pins Python 3.12 for uv
├── uv.lock                          Pinned dependency lockfile
├── .gitignore                       Excludes .venv, __pycache__, .pytest_cache, dist, build
│
├── data/input/
│   ├── research.md                  Cited sources, candidate figures, gaps, and doubts
│   ├── figures.csv                  One disputed figure per row with low/high range and source IDs
│   ├── timeline.csv                 One dated event per row; rows without coordinates are omitted
│   └── PEIRA_COMMIT.txt             The PEIRA site commit from which inputs were originally copied
│
├── docs/
│   ├── data-format.md               Schema reference for the points export (schemaVersion 1)
│   ├── scenario-brief.md            Owner-confirmed brief for the scenario exploration (S0/S1/S2)
│   └── STATE.md                     This document
│
├── exports/
│   └── leipzig-points.v1.json       The committed, reproducible export (schemaVersion 1, kind=points)
│
├── src/leipzig/
│   ├── __init__.py                  Package init
│   └── export.py                    Builds and writes `leipzig-points.v1.json`
│
├── tests/
│   ├── test_export.py               Six determinism, schema, and source-validation tests
│
├── prompts/
│   ├── freeze-research.md           This freeze task prompt
│   ├── p-016.md                     Earlier research sprint prompt
│   └── p-026.md                     Earlier scenario sprint prompt
│
└── .github/
    ├── workflows/reproduce.yml      CI: sync, test, export, diff
    └── skills/
        ├── peira-research-repo/     Agent skill: how to work in a PEIRA research repo
        └── peira-scenario-analysis/ Agent skill: how to build a scenario model here
```

Note: `src/leipzig/scenarios.py`, `tests/test_scenarios.py`, and
`exports/leipzig-scenarios.v1.json` exist on the unmerged branch
`origin/docs/cavalry-and-north-rows` but are **not** on `main`. See
[§8](#8-known-issues-and-plausibility-audit).

Evidence: `find . -not -path './.git/*' -not -path './.venv/*' | sort`. VERIFIED.

---

## 3. Inputs

All three input files live in `data/input/`. They are the only files the export reads.
Their SHA-256 digests are recorded inside `exports/leipzig-points.v1.json` under `inputs`.

### 3.1 `research.md`

108 lines. Contains the research brief, a source table, a candidate figures table, figure
interpretation notes, gaps and doubts, and a verification report. Every source and figure
row carries the note `candidate — author must verify`. The file was produced by an agent
research run; no row has been owner-verified.

Source table has 14 source IDs (WHE, DHM, LSE-HORSE, HISTORY, USF-BRIT-1911, MAUDE,
PFLUGK, SMITH, BRETT, DLI, NAP-SERIES-NORTH, HISTORYOFWAR-17OCT, NAP-ORDER-FR,
NAP-ORDER-ALL). Plus two additional source IDs (WIKI-FR-OOB, WIKI-FR-COAL) added in a
later commit to cover the cavalry rows. The export script validates all figure source IDs
against the source table header.

Evidence: `wc -l data/input/research.md` → 108. Source table parsed by
`src/leipzig/export.py:_sources_from_research`. VERIFIED.

### 3.2 `figures.csv`

17 data rows (1 header + 17). Schema: `schemaVersion, figure, side_category, low, high,
source_ids, note, status`.

| Metric | Count |
|---|---|
| Total rows | 17 |
| `candidate` rows | 17 |
| `verified` rows | 0 |
| Agent-researched rows | All 17 |
| Single-source rows | 11 |
| Multi-source rows | 6 |

All rows were written by agent runs (p-016, p-026, and the cavalry/northern-army sprint).
The owner has not marked any row `verified`.

Evidence: `wc -l data/input/figures.csv` → 18 (17 data rows). `grep -c candidate` → 17.
`grep -c "^1,.*verified" data/input/figures.csv` → 0. OWNER-CONFIRM (owner must verify
rows before the export status can change).

### 3.3 `timeline.csv`

18 data rows (1 header + 18). Schema: `id, date, label, place, lat, lon, coord_source,
source_ids, confidence, status`.

| Metric | Count |
|---|---|
| Total rows | 18 |
| Rows with coordinates (exported as points) | 9 |
| Rows without coordinates (omitted) | 9 |
| `candidate` rows | 18 |
| `verified` rows | 0 |

Evidence: `wc -l data/input/timeline.csv` → 19 (18 data rows). VERIFIED.

---

## 4. Export format

Single export file: `exports/leipzig-points.v1.json`. Schema version 1.

### Top-level fields

| Field | Type | Value / meaning |
|---|---|---|
| `schemaVersion` | integer | Always `1` |
| `essay` | string | `"leipzig-1813"` |
| `kind` | string | `"points"` |
| `seed` | integer | `1601` (fixed; recorded for reproducibility) |
| `inputs` | object | SHA-256 of each input file at export time |
| `points` | array | 9 dated place-events with coordinates |
| `figures` | array | 17 candidate figures with ranges |
| `omitted` | array | 9 events omitted because no source-backed coordinate exists |

There is **no** `scenarios`, `median`, or scenario-specific field in the current `main`
export. Those fields exist only in `exports/leipzig-scenarios.v1.json` on the unmerged
branch `origin/docs/cavalry-and-north-rows`.

### Point record fields

`id`, `time` (ISO date), `label`, `place`, `lat`, `lon`, `unit` (null), `side` (null),
`strength` (null), `source` (array of source IDs), `confidence` (`"low"`), `status`
(`"candidate"`).

### Figure record fields

`id` (`"figure-01"` … `"figure-17"`), `figure` (name string), `side`, `low`, `high`,
`unit` (`"people"` or `"guns"`), `sources` (array), `single_source` (bool), `note`,
`status`.

Unit is `"guns"` when the figure name contains the word "artillery"; otherwise `"people"`.

### Omitted record fields

`id`, `reason` (always: `"No source-backed coordinates were recorded for this event."`).

Evidence: `exports/leipzig-points.v1.json` inspected directly; `docs/data-format.md`
cross-checked. VERIFIED.

---

## 5. Scenario model

> **This section describes code on the unmerged branch `origin/docs/cavalry-and-north-rows`.
> The model is not on `main` and the scenario export is not committed to `main`.**
> The description is included here so the owner can decide whether to merge or close the branch.

### What it samples

For each of 1,000 draws the model samples uniformly from the low–high range of these
`figures.csv` rows:

| Quantity | Figure row |
|---|---|
| French starting strength | "Forces concentrated near Leipzig before the battle" |
| Coalition starting strength | "Forces approaching Leipzig" |
| French total losses | "French casualties during the battle" |
| Coalition total losses | "Coalition casualties" |
| French cavalry | "French cavalry at Leipzig" |
| Coalition cavalry | "Coalition cavalry at Leipzig" |
| Coalition reinforcements (17 Oct) | "Allied reinforcements arriving on 17 October" |
| French reinforcements (17 Oct) | "French reinforcements arriving on 17 October" |
| Northern Army strength | "Army of the North at Leipzig" |

### Daily loss shares (author assumptions, not sourced)

| Date | Loss share |
|---|---|
| 16 October 1813 | 35 % of total battle losses |
| 17 October 1813 | 5 % |
| 18 October 1813 | 45 % |
| 19 October 1813 | 15 % |

These shares are explicit author assumptions recorded in `src/leipzig/scenarios.py`.

### Strength formula

For each side, day, and draw:

```
effective_strength = starting_strength
                   − (cumulative_loss_share × total_losses)
                   + arrivals
```

Cavalry follows the same formula, with the French cavalry value optionally multiplied by
the scenario's `french_cavalry_multiplier` before losses are applied.

### Scenarios and parameters

| ID | Label | `french_cavalry_multiplier` | `northern_army_delay_days` |
|---|---|---|---|
| S0 | historical (baseline) | 1.0 (fixed) | 0 (fixed) |
| S1 | cavalry parity | uniform 1.0 – 1.5 (sampled once per scenario) | 0 (fixed) |
| S2 | delayed northern army | 1.0 (fixed) | choice of 0, 1, or 2 (sampled once) |

### Output metrics

For each scenario × day × side: p10, p50 (median), p90 of effective strength and of
cavalry strength across 1,000 draws. Stored in the export as `strength.low` (p10),
`median` (p50), `strength.high` (p90), and `cavalry.low`/`cavalry.high`.

### What the model does NOT do

- No terrain, morale, leadership, or timing within a day.
- No combat resolution — it is bookkeeping, not a battle simulation.
- Does not vary casualty totals by scenario (losses are always sampled from the same
  figures.csv ranges regardless of scenario parameters).
- Does not model cavalry attrition separately from infantry attrition.
- Does not account for prisoners separately from killed/wounded.
- Scenario parameters (multiplier, delay) are sampled once per scenario, not per draw.

Evidence: `src/leipzig/scenarios.py` on branch `origin/docs/cavalry-and-north-rows`
inspected directly. OWNER-CONFIRM (owner must decide whether to merge this branch).

---

## 6. Reproducibility

Fixed seed: `1601`, recorded in `export.py` (`SEED = 1601`) and in the JSON export under
`"seed": 1601`.

The points export uses `random.seed(SEED)` via `random.Random(SEED)` but does not actually
draw random numbers — the seed is present for forward-compatibility. The scenario model
(unmerged branch) uses 1,000 draws with `random.Random(seed)`.

Determinism is tested by `tests/test_export.py::test_export_is_byte_identical` (writes
the export twice to a temp dir, diffs bytes) and
`tests/test_export.py::test_committed_export_matches_fresh_export` (re-runs export,
compares to the committed file byte-for-byte).

### Fresh-clone commands (fish shell)

```fish
git clone https://github.com/Boombaybay12334/peira-essay-001-leipzig
cd peira-essay-001-leipzig
uv sync --frozen
uv run pytest
uv run export
git diff --exit-code exports/
```

Re-running must produce byte-identical output. If `git diff` exits non-zero, the
environment is not reproducing correctly.

### Fresh-clone verification output (run 2026-11-12, local clone)

```
6 passed in 0.03s
# git diff --exit-code exports/ → exit 0 (no diff)
```

Evidence: local clone test run in temp dir during freeze. VERIFIED.

---

## 7. CI

Workflow file: `.github/workflows/reproduce.yml`. Triggers on every push and pull request.

Steps:
1. `actions/checkout@v7` — check out the repo.
2. `actions/setup-python@v7` with `python-version-file: .python-version` — install Python 3.12.
3. `astral-sh/setup-uv@v7` — install uv.
4. `uv sync --frozen` — install pinned dependencies (no network resolution).
5. `uv run pytest` — run all tests.
6. `uv run export` — regenerate the export.
7. `git diff --exit-code exports/` — fail if the committed export differs from the freshly generated one.

The workflow does **not** run `export-scenarios`. The scenario export is not part of CI.

Evidence: `.github/workflows/reproduce.yml` inspected directly. VERIFIED.

---

## 8. Known issues and plausibility audit

This section audits the scenario export (`exports/leipzig-scenarios.v1.json`) on the
unmerged branch `origin/docs/cavalry-and-north-rows` without changing it.

### 8.1 Cavalry ranges vs. source figures

**Coalition cavalry.**
`figures.csv` row: `low=86658, high=86658` (single source, WIKI-FR-COAL).
Scenario export (S0, 16 October, coalition side): `cavalry.low=67,439, cavalry.high=67,727`.
Difference: the export's p10–p90 cavalry band is **19,219–19,231 below** the source figure.

**French cavalry.**
`figures.csv` row: `low=28294, high=36361` (WIKI-FR-OOB).
Scenario export (S0, 16 October, French side): `cavalry.low=15,892, cavalry.high=22,238`.
Difference: the export's p10 is **12,402 below** the source low of 28,294. The p90 is
**14,123 below** the source high.

Both cavalry ranges in the export are substantially below the corresponding source
figures. The model applies cumulative loss shares to cavalry strength using the same formula
as total strength, but total losses (`French casualties during the battle` = 38,000;
`Coalition casualties` = 54,000–55,000) are not cavalry-only losses. The formula subtracts
a share of *total battle casualties* from the cavalry count, which inflates the cavalry
reduction far beyond what a cavalry-specific loss rate would produce.

### 8.2 S0 vs. S1 comparison

S0 and S1 differ only in `french_cavalry_multiplier` (S0 = 1.0 fixed; S1 sampled from
1.0–1.5). Effect on **coalition** side: negligible — S0 coalition total strength (16 Oct)
is 305,781–306,069; S1 is 305,788–306,066. Difference of about 7–9 men. Effect on
**French** cavalry: S0 = 15,892–22,238; S1 = 22,308–30,159. The multiplier raises
French cavalry by approximately 6,400–7,900 men at the p10–p90 band, which is a meaningful
relative change but still far below the source figure low of 28,294.

S1 is internally consistent with the model's design (the multiplier is applied) but the
absolute cavalry numbers on both sides are implausibly low relative to the source figures
for the reason described in §8.1.

### 8.3 Summary reading

| Issue | Numbers | Assessment |
|---|---|---|
| Coalition cavalry export vs. source | 67,439–67,727 vs. 86,658 | ~22% below source; likely caused by applying total-loss share to cavalry count |
| French cavalry export vs. source | 15,892–22,238 vs. 28,294–36,361 | 44–56% below source low; same cause |
| S0 vs. S1 coalition strength | differ by <10 men | The multiplier does not affect the coalition side, as designed |
| S0 vs. S1 French cavalry | ~6,400–7,900 men difference | Multiplier effect is present but absolute values remain below source range |

The model's counting may effectively double-count cavalry losses by subtracting a share of
*all* battle losses (infantry + cavalry + artillery) from a cavalry-only starting count.
This is a model design question, not a data error. The export is not changed here.

Evidence: `exports/leipzig-scenarios.v1.json` on branch `origin/docs/cavalry-and-north-rows`
parsed with Python. `figures.csv` rows 16–17. `src/leipzig/scenarios.py`. OWNER-CONFIRM
(owner must decide whether to merge the branch and whether to fix the cavalry formula).

---

## 9. How-to guide

### Add a figure

1. Add a row to `data/input/figures.csv`. All fields are required: `schemaVersion`,
   `figure`, `side_category`, `low`, `high`, `source_ids`, `note`, `status`.
2. Add the source ID(s) to the source table in `data/input/research.md` if they are new.
3. Run `uv run pytest` to confirm source IDs validate.
4. Run `uv run export` and commit the updated export alongside the CSV change.
5. Set `status` to `candidate — author must verify` until the owner has checked the source.

### Rerun the exports

```fish
uv sync --frozen
uv run export
git diff exports/
```

If `git diff` is empty, the export is already up to date. Commit any diff.

### Verify a row

Only the owner can mark a row verified. Change the `status` cell from
`candidate — author must verify` to `verified — <date> — <initials>`. Then rerun the
export; the status propagates into the JSON automatically.

### Copy exports into the site

In the PEIRA site repo:

```fish
pnpm sync:data
```

This copies the versioned JSON files from this research repo into the site. Confirm the
command with the site's own documentation before running it.

Evidence: `README.md`, `docs/data-format.md`. OWNER-CONFIRM (confirm `pnpm sync:data` is
still the correct site command).

---

## 10. Starting a second research repo

1. Create a new repo under the PEIRA organisation, e.g. `peira-essay-002-<topic>`.
2. Copy these files as the starting scaffold:
   - `AGENTS.md` (edit the essay title and ADR references)
   - `pyproject.toml` (edit name and description)
   - `.python-version`, `uv.lock` (keep identical for now; update if Python version changes)
   - `.gitignore` (keep identical)
   - `.github/workflows/reproduce.yml` (keep identical)
   - `.github/skills/peira-research-repo/SKILL.md` (keep or update)
   - `data/input/research.md` (blank new template)
   - `data/input/figures.csv` (header row only)
   - `data/input/timeline.csv` (header row only)
3. Write a new `src/<topic>/export.py` mirroring the structure of `src/leipzig/export.py`.
4. Write matching tests in `tests/test_export.py`.
5. Record the starting PEIRA site commit in `data/input/PEIRA_COMMIT.txt`.
6. Run `uv sync --frozen && uv run pytest` to confirm the scaffold is green before first research sprint.
7. The scenario model (`src/leipzig/scenarios.py`) is optional; include it only if the
   new essay needs a quantitative exploration.

Evidence: this document, `AGENTS.md`. OWNER-CONFIRM (confirm the new repo's name and
whether the scenario kit should be included from the start).
