"""Deterministic scenario exploration for the Leipzig research export."""

from __future__ import annotations

import random
from collections.abc import Mapping, Sequence

SEED = 1601
DRAWS = 1_000
LOSS_SHARES = {
    "1813-10-16": 0.35,
    "1813-10-17": 0.05,
    "1813-10-18": 0.45,
    "1813-10-19": 0.15,
}
SCENARIOS = (
    {
        "id": "S0",
        "label": "historical (baseline)",
        "kind": "historical",
        "french_cavalry_multiplier": 1.0,
        "northern_army_delay_days": 0,
        "summary": "Baseline bookkeeping using the documented arrival timing.",
    },
    {
        "id": "S1",
        "label": "cavalry parity",
        "kind": "alternative",
        "french_cavalry_multiplier": (1.0, 1.5),
        "northern_army_delay_days": 0,
        "summary": "Bookkeeping with a smaller French cavalry shortfall.",
    },
    {
        "id": "S2",
        "label": "delayed northern army",
        "kind": "alternative",
        "french_cavalry_multiplier": 1.0,
        "northern_army_delay_days": (0, 1, 2),
        "summary": "Bookkeeping with a later arrival for the Army of the North.",
    },
)

ASSUMPTIONS = [
    "Author assumption: daily shares of total losses are 0.35 on 16 October, 0.05 on 17 October, 0.45 on 18 October, and 0.15 on 19 October.",
    "Author assumption: the fixed seed is 1601 and each scenario uses 1,000 draws.",
]
LIMITATIONS = [
    "This is an exploration, not a simulation of fighting; it has no terrain, morale, leadership, or timing within a day.",
    "Ranges come from disagreeing candidate sources, and the candidate rows are unverified.",
    "Daily loss shares and scenario parameters are the author's assumptions.",
    "Results show relative strength under assumptions, not what would have happened.",
]


def _uniform(rng: random.Random, row: Mapping[str, str]) -> float:
    low = float(row["low"])
    high = float(row["high"])
    return rng.uniform(low, high)


def _figure(figures: Sequence[Mapping[str, str]], text: str) -> Mapping[str, str]:
    for row in figures:
        if row["figure"] == text:
            return row
    raise ValueError(f"Missing required figure row: {text}")


def _round(value: float) -> float:
    return round(value, 3)


def _percentiles(values: list[float]) -> dict[str, float]:
    ordered = sorted(values)

    def percentile(fraction: float) -> float:
        index = (len(ordered) - 1) * fraction
        lower = int(index)
        upper = min(lower + 1, len(ordered) - 1)
        weight = index - lower
        return _round(ordered[lower] + (ordered[upper] - ordered[lower]) * weight)

    return {"p10": percentile(0.10), "p50": percentile(0.50), "p90": percentile(0.90)}


def _parameter_value(
    rng: random.Random, value: float | tuple[float, ...]
) -> float:
    if isinstance(value, tuple):
        return rng.uniform(value[0], value[-1])
    return value


def _delay_value(rng: random.Random, value: int | tuple[int, ...]) -> int:
    if isinstance(value, tuple):
        return rng.choice(value)
    return value


def build_scenario_points(
    timeline: Sequence[Mapping[str, str]],
    figures: Sequence[Mapping[str, str]],
    *,
    seed: int = SEED,
    draws: int = DRAWS,
) -> tuple[list[dict], list[dict]]:
    dates = sorted(LOSS_SHARES)
    places = [
        row for row in timeline if row["date"] in dates and row["lat"] and row["lon"]
    ]
    if not places:
        raise ValueError("No source-backed coordinates exist for the scenario dates")

    french_start = _figure(figures, "Forces concentrated near Leipzig before the battle")
    coalition_start = _figure(figures, "Forces approaching Leipzig")
    french_losses = _figure(figures, "French casualties during the battle")
    coalition_losses = _figure(figures, "Coalition casualties")
    french_cavalry = _figure(figures, "French cavalry at Leipzig")
    coalition_cavalry = _figure(figures, "Coalition cavalry at Leipzig")
    coalition_arrival = _figure(figures, "Allied reinforcements arriving on 17 October")
    french_arrival = _figure(figures, "French reinforcements arriving on 17 October")
    northern_army = _figure(figures, "Army of the North at Leipzig")

    source_ids = {
        item["figure"]: [source.strip() for source in item["source_ids"].split(";")]
        for item in (
            french_start,
            coalition_start,
            french_losses,
            coalition_losses,
            french_cavalry,
            coalition_cavalry,
            coalition_arrival,
            french_arrival,
            northern_army,
        )
    }
    rng = random.Random(seed)
    scenario_points: list[dict] = []
    scenario_meta: list[dict] = []
    for definition in SCENARIOS:
        multiplier = _parameter_value(rng, definition["french_cavalry_multiplier"])
        delay = _delay_value(rng, definition["northern_army_delay_days"])
        sampled: dict[str, list[dict[str, list[float]]]] = {}
        for date in dates:
            for side in ("French", "Coalition"):
                sampled[f"{date}:{side}"] = {
                    "strength": [],
                    "cavalry": [],
                }
        for _ in range(draws):
            starts = {
                "French": _uniform(rng, french_start),
                "Coalition": _uniform(rng, coalition_start),
            }
            losses = {
                "French": _uniform(rng, french_losses),
                "Coalition": _uniform(rng, coalition_losses),
            }
            cavalry = {
                "French": _uniform(rng, french_cavalry) * multiplier,
                "Coalition": _uniform(rng, coalition_cavalry),
            }
            northern = _uniform(rng, northern_army)
            french_reinforcements = _uniform(rng, french_arrival)
            coalition_reinforcements = _uniform(rng, coalition_arrival)
            for day_index, date in enumerate(dates):
                cumulative_share = sum(LOSS_SHARES[item] for item in dates[: day_index + 1])
                arrival_day = 1
                northern_day = arrival_day + delay
                for side in ("French", "Coalition"):
                    arrivals = 0.0
                    if side == "French" and day_index >= arrival_day:
                        arrivals = french_reinforcements
                    if side == "Coalition" and day_index >= arrival_day:
                        arrivals = coalition_reinforcements - northern
                        if day_index >= northern_day:
                            arrivals += northern
                    key = f"{date}:{side}"
                    sampled[key]["strength"].append(
                        starts[side] - cumulative_share * losses[side] + arrivals
                    )
                    sampled[key]["cavalry"].append(
                        cavalry[side] - cumulative_share * losses[side] + arrivals
                    )
        for place in places:
            date = place["date"]
            for side in ("French", "Coalition"):
                key = f"{date}:{side}"
                strength = _percentiles(sampled[key]["strength"])
                cavalry_result = _percentiles(sampled[key]["cavalry"])
                scenario_points.append(
                    {
                        "id": f"{place['id']}-{definition['id']}-{side.lower()}",
                        "time": date,
                        "label": place["label"],
                        "place": place["place"],
                        "lat": float(place["lat"]),
                        "lon": float(place["lon"]),
                        "scenario": definition["id"],
                        "side": side,
                        "strength": {
                            "low": strength["p10"],
                            "high": strength["p90"],
                            "unit": "men",
                        },
                        "median": strength["p50"],
                        "cavalry": {
                            "low": cavalry_result["p10"],
                            "high": cavalry_result["p90"],
                            "unit": "men",
                        },
                        "source": sorted(
                            {
                                source
                                for figure_name in source_ids
                                for source in source_ids[figure_name]
                            }
                            | {
                                source.strip()
                                for source in place["source_ids"].split(";")
                            }
                            | {"HISTORYOFWAR-17OCT"}
                        ),
                        "confidence": "low",
                        "status": "candidate",
                    }
                )
        scenario_meta.append(
            {
                "id": definition["id"],
                "label": definition["label"],
                "kind": definition["kind"],
                "assumptions": ASSUMPTIONS
                + [
                    f"Author assumption: french_cavalry_multiplier={_round(multiplier)}.",
                    f"Author assumption: northern_army_delay_days={delay}.",
                ],
                "parameters": {
                    "french_cavalry_multiplier": _round(multiplier),
                    "northern_army_delay_days": delay,
                    "draws": draws,
                },
                "limitations": LIMITATIONS,
                "exploration": True,
                "summary": definition["summary"],
            }
        )
    scenario_points.sort(key=lambda item: (item["time"], item["scenario"], item["side"]))
    return scenario_meta, scenario_points
