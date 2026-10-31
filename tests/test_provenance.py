import json

from provenance.run_log import (
    MODEL_NAME,
    append_jsonl_record,
    build_run_record,
    read_jsonl_records,
)


def test_run_record_contains_required_provenance():
    record = build_run_record(
        objective="minimum_strain",
        target_wh_kg=50.0,
        final_status="MINIMUM_STRAIN_FOUND",
        iterations=10,
        minimum_strain_percent=7.0312,
        verified_energy_wh_kg=50.0331,
    )

    assert record["model"] == MODEL_NAME
    assert record["target_Wh_kg"] == 50.0
    assert record["final_status"] == "MINIMUM_STRAIN_FOUND"
    assert record["evidence_type"] == "THEORETICAL_SIMULATION"
    assert record["experimental_validation"] is False
    assert record["run_id"]
    assert record["timestamp_utc"]


def test_run_ids_are_unique():
    first = build_run_record(
        objective="minimum_strain",
        target_wh_kg=50,
        final_status="MINIMUM_STRAIN_FOUND",
        iterations=10,
    )

    second = build_run_record(
        objective="minimum_strain",
        target_wh_kg=50,
        final_status="MINIMUM_STRAIN_FOUND",
        iterations=10,
    )

    assert first["run_id"] != second["run_id"]


def test_jsonl_round_trip(tmp_path):
    path = tmp_path / "runs.jsonl"

    record = build_run_record(
        objective="minimum_strain",
        target_wh_kg=50,
        final_status="MINIMUM_STRAIN_FOUND",
        iterations=10,
        minimum_strain_percent=7.0312,
        verified_energy_wh_kg=50.0331,
    )

    append_jsonl_record(
        record,
        path,
    )

    loaded = read_jsonl_records(path)

    assert len(loaded) == 1
    assert loaded[0]["run_id"] == record["run_id"]
    assert (
        loaded[0]["verified_energy_Wh_kg"]
        == 50.0331
    )


def test_jsonl_is_one_record_per_line(tmp_path):
    path = tmp_path / "runs.jsonl"

    for target in [10, 25, 50]:
        record = build_run_record(
            objective="minimum_strain",
            target_wh_kg=target,
            final_status="TEST",
            iterations=1,
        )

        append_jsonl_record(
            record,
            path,
        )

    lines = path.read_text(
        encoding="utf-8"
    ).splitlines()

    assert len(lines) == 3

    for line in lines:
        parsed = json.loads(line)
        assert "run_id" in parsed


def test_missing_log_file_returns_empty_list(tmp_path):
    missing = tmp_path / "does_not_exist.jsonl"

    assert read_jsonl_records(missing) == []