from pathlib import Path

from leipzig.export import build_export, write_export

ROOT = Path(__file__).resolve().parents[1]
EXPORT_PATH = ROOT / "exports" / "leipzig-points.v1.json"
REQUIRED_TOP_LEVEL = {"schemaVersion", "essay", "kind", "seed", "inputs", "points", "figures", "omitted"}


def test_export_is_byte_identical(tmp_path):
    first = tmp_path / "first.json"
    second = tmp_path / "second.json"
    write_export(first)
    write_export(second)
    assert first.read_bytes() == second.read_bytes()


def test_every_figure_has_sources_and_valid_range():
    for figure in build_export()["figures"]:
        assert figure["sources"]
        assert isinstance(figure["low"], (int, float))
        assert isinstance(figure["high"], (int, float))
        assert figure["low"] <= figure["high"]


def test_all_source_ids_exist_in_research():
    source_ids = set()
    in_table = False
    for line in (ROOT / "data/input/research.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("| id |"):
            in_table = True
            continue
        if in_table and not line.startswith("|"):
            break
        if in_table and not line.startswith("|---"):
            source_ids.add(line.strip("|").split("|")[0].strip())
    exported = build_export()
    used = {source for point in exported["points"] for source in point["source"]}
    used.update(source for figure in exported["figures"] for source in figure["sources"])
    assert used <= source_ids, f"Missing source IDs: {sorted(used - source_ids)}"


def test_point_coordinates_and_sources_are_valid():
    for point in build_export()["points"]:
        assert -90 <= point["lat"] <= 90
        assert -180 <= point["lon"] <= 180
        assert point["source"]


def test_schema_and_required_keys():
    exported = build_export()
    assert exported["schemaVersion"] == 1
    assert REQUIRED_TOP_LEVEL <= exported.keys()
    point_keys = {
        "id", "time", "label", "place", "lat", "lon", "unit", "side",
        "strength", "source", "confidence", "status",
    }
    figure_keys = {
        "id", "figure", "side", "low", "high", "unit", "sources",
        "single_source", "note", "status",
    }
    assert all(point_keys <= point.keys() for point in exported["points"])
    assert all(figure_keys <= figure.keys() for figure in exported["figures"])
    assert all({"id", "reason"} <= item.keys() for item in exported["omitted"])


def test_committed_export_matches_fresh_export(tmp_path):
    fresh = tmp_path / "fresh.json"
    write_export(fresh)
    assert fresh.read_bytes() == EXPORT_PATH.read_bytes()
