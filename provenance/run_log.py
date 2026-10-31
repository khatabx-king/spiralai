"""
SpiralAI provenance logging.

Writes append-only JSONL records so scientific-design runs can be
audited, compared, benchmarked, and replayed.

All current SpiralAI numerical results are theoretical simulations,
not experimentally validated device performance.
"""

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


MODEL_NAME = "meta-models/muse-spark-open-1026"
EVIDENCE_TYPE = "THEORETICAL_SIMULATION"


def new_run_id() -> str:
    """Create a unique run identifier."""

    timestamp = datetime.now(timezone.utc).strftime(
        "%Y%m%dT%H%M%S"
    )

    suffix = uuid.uuid4().hex[:8]

    return f"{timestamp}Z-{suffix}"


def build_run_record(
    *,
    objective: str,
    target_wh_kg: float,
    final_status: str,
    iterations: int,
    minimum_strain_percent: float | None = None,
    verified_energy_wh_kg: float | None = None,
    history: list[dict] | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict:
    """
    Build one provenance record without writing it to disk.
    """

    return {
        "schema_version": "1.0",
        "run_id": new_run_id(),
        "timestamp_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "model": MODEL_NAME,
        "objective": objective,
        "target_Wh_kg": float(target_wh_kg),
        "final_status": final_status,
        "iterations": int(iterations),
        "minimum_strain_percent": (
            minimum_strain_percent
        ),
        "verified_energy_Wh_kg": (
            verified_energy_wh_kg
        ),
        "evidence_type": EVIDENCE_TYPE,
        "experimental_validation": False,
        "history": history or [],
        "metadata": metadata or {},
        "scientific_disclaimer": (
            "Theoretical/simulated screening result. "
            "Higher-fidelity simulation and experimental "
            "validation are required before practical claims."
        ),
    }


def append_jsonl_record(
    record: dict,
    path: str | Path,
) -> Path:
    """
    Append exactly one JSON object as one JSONL line.
    """

    output_path = Path(path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_path.open(
        "a",
        encoding="utf-8",
    ) as handle:
        json.dump(
            record,
            handle,
            ensure_ascii=False,
            sort_keys=True,
        )

        handle.write("\n")

    return output_path


def read_jsonl_records(
    path: str | Path,
) -> list[dict]:
    """
    Load all valid non-empty JSONL records.
    """

    input_path = Path(path)

    if not input_path.exists():
        return []

    records = []

    with input_path.open(
        "r",
        encoding="utf-8",
    ) as handle:
        for line in handle:
            line = line.strip()

            if not line:
                continue

            records.append(
                json.loads(line)
            )

    return records