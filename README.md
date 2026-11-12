# PEIRA Essay 001: Leipzig research export

This repository contains the candidate research inputs and reproducible JSON
export for PEIRA Essay 001, *The Battle of Leipzig (1813): Strategy, Chaos,
and the Fate of an Empire*. The PEIRA site copies the versioned export and
renders it; this repository contains no site code.

For a full description of the repo's current state, see **[docs/STATE.md](docs/STATE.md)**.

## Status

Nothing in the research inputs or export is verified history yet. All 17
figures and all 18 timeline rows remain `candidate` unless the owner
explicitly verifies them.

An unmerged branch (`origin/docs/cavalry-and-north-rows`) contains a scenario
model (`src/leipzig/scenarios.py`) and a second export
(`exports/leipzig-scenarios.v1.json`). It is not on `main`. See the Known
Issues section of STATE.md for a plausibility audit before merging.

## Reproduce

```sh
uv sync --frozen
uv run pytest
uv run export
git diff --exit-code exports/
```

The output format is documented in [docs/data-format.md](docs/data-format.md).

## Sources and provenance

The input files were copied from PEIRA commit `0a4b6d62c0f04796dcddd431abfbd0489b3788fe`.
See [data/input/research.md](data/input/research.md) for cited sources and
the candidate-data warnings. The MIT license is an assumption for the owner
to confirm; facts are compiled from the cited sources.

PEIRA site: <https://github.com/Boombaybay12334/PEIRA>
