import json
from pathlib import Path

from leipzig.export import build_scenarios_export, write_scenarios_export
from leipzig.scenarios import DRAWS, SEED, build_scenario_points

ROOT = Path(__file__).resolve().parents[1]
EXPORT_PATH = ROOT / "exports/leipzig-scenarios.v1.json"


def test_scenario_export_is_byte_identical(tmp_path):
    first = tmp_path / "first.json"
    second = tmp_path / "second.json"
    write_scenarios_export(first)
    write_scenarios_export(second)
    assert first.read_bytes() == second.read_bytes()


def test_same_seed_matches_and_different_seed_changes():
    timeline = list(__import__("csv").DictReader((ROOT / "data/input/timeline.csv").open()))
    figures = list(__import__("csv").DictReader((ROOT / "data/input/figures.csv").open()))
    assert build_scenario_points(timeline, figures, seed=SEED) == build_scenario_points(
        timeline, figures, seed=SEED
    )
    assert build_scenario_points(timeline, figures, seed=SEED) != build_scenario_points(
        timeline, figures, seed=SEED + 1
    )


def test_scenarios_have_valid_parameters_and_percentiles():
    exported = build_scenarios_export()
    assert len(exported["scenarios"]) == 3
    assert all(
        scenario["assumptions"]
        and scenario["limitations"]
        and scenario["exploration"] is True
        for scenario in exported["scenarios"]
    )
    assert exported["scenarios"][0]["parameters"]["french_cavalry_multiplier"] == 1.0
    assert exported["scenarios"][0]["parameters"]["northern_army_delay_days"] == 0
    assert 1.0 <= exported["scenarios"][1]["parameters"]["french_cavalry_multiplier"] <= 1.5
    assert exported["scenarios"][2]["parameters"]["northern_army_delay_days"] in (0, 1, 2)
    assert all(
        point["strength"]["low"] <= point["median"] <= point["strength"]["high"]
        and point["status"] == "candidate"
        for point in exported["points"]
    )


def test_all_scenario_sources_exist_and_point_count_is_stable():
    source_ids = set()
    in_table = False
    for line in (ROOT / "data/input/research.md").read_text().splitlines():
        if line.startswith("| id |"):
            in_table = True
            continue
        if in_table and not line.startswith("|"):
            break
        if in_table and not line.startswith("|---"):
            source_ids.add(line.strip("|").split("|")[0].strip())
    exported = build_scenarios_export()
    assert len(exported["points"]) == 24
    assert all(set(point["source"]) <= source_ids for point in exported["points"])


def test_committed_scenario_export_matches_fresh_export(tmp_path):
    fresh = tmp_path / "fresh.json"
    write_scenarios_export(fresh)
    assert fresh.read_bytes() == EXPORT_PATH.read_bytes()


def test_export_has_expected_seed_and_draw_count():
    exported = json.loads(EXPORT_PATH.read_text())
    assert exported["seed"] == SEED
    assert all(scenario["parameters"]["draws"] == DRAWS for scenario in exported["scenarios"])
