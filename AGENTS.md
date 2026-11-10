# AGENTS.md — peira-essay-001-leipzig

Research repository for PEIRA Essay 001, *The Battle of Leipzig (1813): Strategy, Chaos, and the Fate of an Empire*. It produces **versioned JSON exports** that the PEIRA site (`github.com/Boombaybay12334/PEIRA`) copies in and renders. This repo holds no site code.

Why it exists (PEIRA docs): ADR-008 — Python offline, exported versioned JSON, uv for environments, fixed seeds, pinned dependencies; DR-02 — every disputed figure stores a range and a source, never a bare number; DR-03 — analyses are reproducible from a clean checkout; DR-04 — the essay links to this public repo.

## Rules
1. **Nothing here is verified history yet.** `data/input/research.md` and `figures.csv` are *candidate* material compiled by an earlier agent run; only the owner can mark a row `verified`.
2. **Never invent a source, number, coordinate or date.** If a value isn't in the input files or on a page you fetched this session, leave it out and report the gap.
3. Every figure needs a source id and a low/high range. A single value is allowed only as `low = high` with `single_source` true.
4. Python via **uv** only. Pin everything (`.python-version`, `uv.lock`, `uv sync --frozen`). Stdlib first; add a dependency only if the task can't be done without it, and say why in the PR.
5. Deterministic output: sorted keys, stable ordering, no timestamps, seed recorded in the file. Re-running must produce **byte-identical** output.
6. Git: Conventional Commits, one ticket per branch, PRs with CI green before merge. The first scaffold commit may go straight to `main`.
7. Never commit secrets. Say what you did not verify.

## Stop and ask when
`uv` or `gh` is missing · an input file is missing · the data format needs a field the docs don't define · the same failure happens 3 times.
