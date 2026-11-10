---
name: peira-research-repo
description: Scaffold and run PEIRA's per-essay research repository — uv-pinned Python environment, deterministic export to the PEIRA module JSON format (schemaVersion 1), tests for reproducibility and source integrity, README, and a reproduce workflow. Use for P-016 and for any research-export or data-format work.
---

# Essay 001 research repo (P-016)

Goal: a **public repo with README, pinned environment, seeded run, and one exported JSON file in the module format** (acceptance criteria of P-016), reproducible from a clean checkout (DR-03).

## Layout
```
README.md  LICENSE  .gitignore  .python-version  pyproject.toml  uv.lock
data/input/research.md      # copied from the PEIRA repo (provenance: commit SHA in README)
data/input/figures.csv      # same
data/input/timeline.csv     # transcribed ONCE from research.md's timeline section (see below)
src/leipzig/export.py       # the export; CLI entry `export`
exports/leipzig-points.v1.json
docs/data-format.md         # documents schemaVersion 1 (DR-01)
tests/test_export.py
.github/workflows/reproduce.yml
```

## Environment
- `uv init`-style project; **stdlib only** unless a dependency is truly needed. Add `pytest` as a dev dependency.
- Pin Python in `.python-version`; commit `uv.lock`; all commands use `uv sync --frozen` and `uv run`.
- Script entry in `pyproject.toml` so `uv run export` works.

## Inputs
- `figures.csv` and `research.md` are copied verbatim; the README states the PEIRA commit they came from and that **all rows are candidate**.
- `timeline.csv` columns: `id,date,label,place,lat,lon,coord_source,source_ids,confidence,status`. Transcribe events from the timeline section of `research.md`. **lat/lon only if a page you fetched this session states the coordinates of that place** (e.g. an encyclopedia entry for the village); record that URL in `coord_source`. No coordinates → leave lat/lon empty; that event goes in the export's `omitted` list with the reason.
- `status` is `candidate` unless the owner has already marked it otherwise in the inputs.

## Export format — schemaVersion 1 (`exports/leipzig-points.v1.json`)
Top level: `schemaVersion` (1), `essay` ("leipzig-1813"), `kind` ("points"), `seed` (integer, fixed constant in code), `inputs` (sha256 of each input file), `points`, `figures`, `omitted`.

`points[]` (one dated place event; matches SRS MOD-01/MOD-02): `id`, `time` (ISO date, or datetime only if a source gives a time), `label`, `place`, `lat`, `lon`, `unit` (string or null), `side` (string or null), `strength` (`{low, high, unit}` or null), `source` (array of source ids), `confidence` (`low`|`medium`|`high`), `status` (`candidate`|`verified`).
`figures[]`: `id`, `figure`, `side`, `low`, `high`, `unit`, `sources` (array), `single_source` (bool), `note`, `status`.
`omitted[]`: `{id, reason}`.

Write this table into `docs/data-format.md` with a short rationale; the PEIRA site's P-017 will validate files against it, so keep field names exactly as above. Do not put example numbers in the doc that look like real data.

## Determinism (DR-03)
- Set `random.seed(SEED)` at start even if nothing random is used yet (Sprint 3's scenario analysis will).
- `json.dumps(obj, sort_keys=True, indent=2, ensure_ascii=False)` + trailing newline; sort `points` by (`time`, `id`), `figures` by `id`. **No timestamps.**
- Running the export twice must give identical bytes.

## Tests (`uv run pytest`)
1. Export twice into temp dirs → byte-identical.
2. Every figure has a non-empty source list, numeric `low` ≤ `high`.
3. Every source id used in `points`/`figures` exists in the Sources table of `research.md` (parse the table; fail naming the missing id).
4. lat in [-90, 90], lon in [-180, 180] for every point; every point has at least one source.
5. `schemaVersion == 1` and required keys present.
6. The committed `exports/leipzig-points.v1.json` equals a fresh export.

## Workflow (`.github/workflows/reproduce.yml`)
On push and pull request: set up uv and Python from `.python-version`, `uv sync --frozen`, `uv run pytest`, `uv run export`, then `git diff --exit-code exports/` so CI proves the committed file reproduces. Pin action versions to current majors (look them up). Minimal permissions (`contents: read`).

## README must contain
What this repo is · the candidate-data warning · how to reproduce (`uv sync --frozen`, `uv run pytest`, `uv run export`) · data format link · source/licence note (code MIT — *an assumption for the owner to confirm*; facts are compiled from cited sources, see `research.md`) · provenance of inputs · link back to the PEIRA site.

## Verification you run, with quoted output
`uv run pytest` passes · `uv run export` then `git diff --exit-code` is clean · a **fresh clone into a temp dir** reproduces the file (`git clone … && uv sync --frozen && uv run export && git diff --exit-code`) · CI run URL green. Report counts: points exported, points omitted (and why), figures, single-source figures.
