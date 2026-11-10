---
name: peira-scenario-analysis
description: Build PEIRA Essay 001's scenario analysis in the research repo — a small seeded Monte Carlo over sourced figure ranges and explicit scenario parameters, exported as module data (points v1 with scenarios). Use for P-026 and any scenario or what-if export.
---

# Scenario analysis (P-026)

Goal: **2 to 3 scenarios defined by explicit parameters, reproducible with fixed seeds, exported as module data** (DR-03, DR-05). Deliberately modest (R-02): an uncertainty exploration, not a battle simulation. Over-claiming is the main risk (R-10).

## Gate
`docs/scenario-brief.md` must contain the line `CONFIRMED: yes`. If not, stop and tell the owner. The brief is the specification: implement the scenarios, parameters and assumptions exactly as written there. Do not add scenarios or parameters.

## Rules
1. **Stdlib only.** Use `random.Random(SEED)` instances, not global state. `SEED` and the draw count are named constants. Same inputs and same code give **byte-identical** output.
2. Starting strengths and total losses are sampled uniformly between `low` and `high` from `data/input/figures.csv` rows you map by id. Record which rows map to which quantity in a small table in `docs/scenario-model.md`, **with their source ids**. If a quantity the brief needs has no row, stop and report the gap.
3. Arrivals or other facts come from `research.md` or `timeline.csv` with source ids only.
4. Assumptions from the brief (day shares, parameter ranges) are written into each scenario's `assumptions[]`, flagged as the author's assumptions, not sourced facts.
5. Wording: "exploration", "under these assumptions". Never "proves", "would have won", or "predicts". `exploration: true` on every scenario.
6. Round all output floats to 3 decimals so results are stable across machines.

## Code
`src/leipzig/scenarios.py` (model, pure functions), `src/leipzig/export.py` extended (or a second entry `export-scenarios`) to write `exports/leipzig-scenarios.v1.json`. The model: for each scenario, N draws; per day per side, effective strength and cavalry strength = start − cumulative loss share × total loss + arrivals present; report p10/p50/p90 across draws.

## Export (`exports/leipzig-scenarios.v1.json`)
Same top-level shape as `leipzig-points.v1.json` (`schemaVersion: 1`, `essay`, `kind: "points"`, `seed`, `inputs` hashes including the brief) plus:
- `scenarios[]`: `{id, label, kind: "historical"|"alternative", assumptions[], parameters, limitations[], exploration: true, summary}`; `summary` is a neutral one-line description of the setting, not a result claim.
- `points[]`: one point per (place, date, scenario) for the places that have sourced coordinates in `timeline.csv`, each with `scenario`, `side`, and `strength: {low: p10, high: p90, unit: "men"}` plus `p50` in an optional `median` field, `source` ids, `confidence: "low"`, `status: "candidate"`.
Update `docs/data-format.md` to document the optional `scenarios` and per-point `scenario` fields and `median`; the PEIRA site's schema depends on these names.

## Tests
Determinism (two runs identical bytes) · same seed same result, different seed different result · `S0` with all parameters at baseline reproduces the baseline sampling · p10 ≤ p50 ≤ p90 everywhere · every scenario has non-empty `assumptions` and `limitations` and `exploration` true · every id in `source` exists in the Sources table · multiplier/delay parameters stay within the brief's ranges · the committed export equals a fresh export.

## CI and docs
The existing `reproduce.yml` must run the new export and `git diff --exit-code exports/`. Update the README with the scenario analysis, the assumptions, and the limitations, in plain words.

## Verification (quoted output)
`uv run pytest` · `uv run export` (and the scenarios export) then `git diff --exit-code` clean · a fresh clone in a temp dir reproduces both exports · CI green. Report per scenario: number of points, the parameters used, and the headline numbers **as ranges**, with the sentence "exploration under stated assumptions".
