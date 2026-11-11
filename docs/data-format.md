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
| `scenarios` | array, optional | Scenario definitions for an exploration export. |
| `figures` | array | Candidate disputed figures and ranges. |
| `omitted` | array | Input events omitted from `points` and the reason. |

## Point fields

Each `points` record has `id`, `time`, `label`, `place`, `lat`, `lon`, `unit`,
`side`, `strength`, `source`, `confidence`, and `status`. Scenario points also
have `scenario`, and may have `median`. `strength` is either `null` or an
object with `low`, `high`, and `unit`; `median` is the p50 value when present.
`source` is an array of source IDs. `confidence` is `low`, `medium`, or `high`;
`status` is `candidate` or `verified`.

## Scenario fields

Scenario exports keep `kind: "points"` and add an optional `scenarios` array.
Each scenario has `id`, `label`, `kind`, `assumptions`, `parameters`,
`limitations`, `exploration: true`, and a neutral `summary`. A point's
`scenario` contains the scenario ID. Scenario strengths use p10 and p90 in
`strength.low` and `strength.high`, with p50 in `median`; optional `cavalry`
uses the same range shape.

## Figure fields

Each `figures` record has `id`, `figure`, `side`, `low`, `high`, `unit`,
`sources`, `single_source`, `note`, and `status`. Ranges preserve uncertainty;
a single-source value may have equal `low` and `high` values only when
`single_source` is true.

## Omitted fields

Each `omitted` record has `id` and `reason`. Events without a source-backed
coordinate remain omitted rather than receiving an inferred location.
