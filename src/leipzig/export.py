"""Build the deterministic PEIRA Essay 001 JSON export."""

from __future__ import annotations

import csv
import hashlib
import json
import random
from pathlib import Path

from leipzig.scenarios import SEED, build_scenario_points

ROOT = Path(__file__).resolve().parents[2]
INPUT_DIR = ROOT / "data" / "input"
EXPORT_PATH = ROOT / "exports" / "leipzig-points.v1.json"
SCENARIO_EXPORT_PATH = ROOT / "exports" / "leipzig-scenarios.v1.json"


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _status(value: str) -> str:
    return "verified" if value.strip().lower().startswith("verified") else "candidate"


def _sources_from_research(text: str) -> set[str]:
    sources: set[str] = set()
    in_table = False
    for line in text.splitlines():
        if line.startswith("| id |"):
            in_table = True
            continue
        if in_table and not line.startswith("|"):
            break
        if in_table and line.startswith("|---"):
            continue
        if in_table:
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if cells and cells[0]:
                sources.add(cells[0])
    return sources


def build_export() -> dict:
    random.seed(SEED)
    timeline = _read_csv(INPUT_DIR / "timeline.csv")
    figures = _read_csv(INPUT_DIR / "figures.csv")
    sources = _sources_from_research((INPUT_DIR / "research.md").read_text(encoding="utf-8"))

    points = []
    omitted = []
    for row in timeline:
        if not row["lat"] or not row["lon"]:
            omitted.append(
                {
                    "id": row["id"],
                    "reason": "No source-backed coordinates were recorded for this event.",
                }
            )
            continue
        point_sources = [item.strip() for item in row["source_ids"].split(";") if item.strip()]
        if not point_sources or not set(point_sources).issubset(sources):
            raise ValueError(f"Unknown point source in {row['id']}")
        points.append(
            {
                "id": row["id"],
                "time": row["date"],
                "label": row["label"],
                "place": row["place"],
                "lat": float(row["lat"]),
                "lon": float(row["lon"]),
                "unit": None,
                "side": None,
                "strength": None,
                "source": point_sources,
                "confidence": row["confidence"],
                "status": _status(row["status"]),
            }
        )

    exported_figures = []
    for index, row in enumerate(figures, start=1):
        figure_sources = [item.strip() for item in row["source_ids"].split(";") if item.strip()]
        if not figure_sources or not set(figure_sources).issubset(sources):
            raise ValueError(f"Unknown figure source in row {index}")
        exported_figures.append(
            {
                "id": f"figure-{index:02d}",
                "figure": row["figure"],
                "side": row["side_category"],
                "low": float(row["low"]),
                "high": float(row["high"]),
                "unit": "people" if "artillery" not in row["figure"].lower() else "guns",
                "sources": figure_sources,
                "single_source": len(figure_sources) == 1,
                "note": row["note"],
                "status": _status(row["status"]),
            }
        )

    points.sort(key=lambda item: (item["time"], item["id"]))
    exported_figures.sort(key=lambda item: item["id"])
    omitted.sort(key=lambda item: item["id"])
    return {
        "schemaVersion": 1,
        "essay": "leipzig-1813",
        "kind": "points",
        "seed": SEED,
        "inputs": {
            "research.md": _digest(INPUT_DIR / "research.md"),
            "figures.csv": _digest(INPUT_DIR / "figures.csv"),
            "timeline.csv": _digest(INPUT_DIR / "timeline.csv"),
        },
        "points": points,
        "figures": exported_figures,
        "omitted": omitted,
    }


def write_export(path: Path = EXPORT_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(build_export(), sort_keys=True, indent=2, ensure_ascii=False)
    path.write_text(payload + "\n", encoding="utf-8")


def build_scenarios_export() -> dict:
    timeline = _read_csv(INPUT_DIR / "timeline.csv")
    figures = _read_csv(INPUT_DIR / "figures.csv")
    scenario_meta, points = build_scenario_points(timeline, figures)
    return {
        "schemaVersion": 1,
        "essay": "leipzig-1813",
        "kind": "points",
        "seed": SEED,
        "inputs": {
            "research.md": _digest(INPUT_DIR / "research.md"),
            "figures.csv": _digest(INPUT_DIR / "figures.csv"),
            "timeline.csv": _digest(INPUT_DIR / "timeline.csv"),
            "scenario-brief.md": _digest(ROOT / "docs" / "scenario-brief.md"),
        },
        "scenarios": scenario_meta,
        "points": points,
    }


def write_scenarios_export(path: Path = SCENARIO_EXPORT_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(build_scenarios_export(), sort_keys=True, indent=2, ensure_ascii=False)
    path.write_text(payload + "\n", encoding="utf-8")


def main() -> None:
    write_export()


def scenarios_main() -> None:
    write_scenarios_export()


if __name__ == "__main__":
    main()
