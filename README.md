# PEIRA Essay 001: Leipzig research export

This repository contains the candidate research inputs and reproducible JSON
export for PEIRA Essay 001, *The Battle of Leipzig (1813): Strategy, Chaos,
and the Fate of an Empire*. The PEIRA site copies the versioned export and
renders it; this repository contains no site code.

## Status

Nothing in the research inputs or export is verified history yet. Records
remain `candidate` unless the owner explicitly verifies them.

## Reproduce

```sh
uv sync --frozen
uv run pytest
uv run export
```

The output format is documented in [docs/data-format.md](docs/data-format.md).

## Sources and provenance

The input files were copied from PEIRA commit `0a4b6d62c0f04796dcddd431abfbd0489b3788fe`.
See [data/input/research.md](data/input/research.md) for cited sources and
the candidate-data warnings. The MIT license is an assumption for the owner
to confirm; facts are compiled from the cited sources.

PEIRA site: <https://github.com/Boombaybay12334/PEIRA>
