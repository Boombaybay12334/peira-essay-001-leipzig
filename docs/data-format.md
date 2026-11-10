# Export format

`exports/leipzig-points.v1.json` uses schema version 1 for the PEIRA site.
The format keeps dates, places, figures, source identifiers, uncertainty, and
candidate verification status explicit so downstream rendering does not turn
research leads into verified facts.

## Top-level fields

| Field | Type | Meaning |
|---|---|---|
| `schemaVersion` | integer | Format version, always `1`. |
| `essay` | string | Essay identifier, `leipzig-1813`. |
| `kind` | string | Export kind, `points`. |
| `seed` | integer | Fixed seed used for reproducible analysis. |
| `inputs` | object | SHA-256 digest for each input file. |
| `points` | array | Dated place events with coordinates. |
| `figures` | array | Candidate disputed figures and ranges. |
| `omitted` | array | Input events omitted from `points` and the reason. |

## Point fields

Each `points` record has `id`, `time`, `label`, `place`, `lat`, `lon`, `unit`,
`side`, `strength`, `source`, `confidence`, and `status`. `strength` is either
`null` or an object with `low`, `high`, and `unit`. `source` is an array of
source IDs. `confidence` is `low`, `medium`, or `high`; `status` is `candidate`
or `verified`.

## Figure fields

Each `figures` record has `id`, `figure`, `side`, `low`, `high`, `unit`,
`sources`, `single_source`, `note`, and `status`. Ranges preserve uncertainty;
a single-source value may have equal `low` and `high` values only when
`single_source` is true.

## Omitted fields

Each `omitted` record has `id` and `reason`. Events without a source-backed
coordinate remain omitted rather than receiving an inferred location.
