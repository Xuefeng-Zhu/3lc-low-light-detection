#!/usr/bin/env python3
"""Export final ExDark validation metrics using read-only 3LC SDK methods.

Run with the configured 3LC environment and its Python interpreter. The SDK
may validate the existing login online. Only the explicitly supplied CSV is
written; it must not exist. No images, model weights, or annotation rows are
loaded. This exporter supports the competition's 12 classes plus ``all``.

The native per_class_metrics column ``mAP`` is AP50. ``Training Phase=After``
identifies final best-checkpoint evaluation, not the maximum over epochs.
"""

from __future__ import annotations

import argparse
import csv
import io
import math
from pathlib import Path
import sys
from typing import Any


CLASSES = (
    "Bicycle", "Boat", "Bottle", "Bus", "Car", "Cat", "Chair", "Cup",
    "Dog", "Motorbike", "People", "Table", "all",
)
FIELDS = (
    "class_id", "class", "AP50", "AP50_95", "precision", "recall",
    "num_images", "num_instances", "epoch", "training_phase", "run_url",
    "metrics_table_url", "validation_table_url",
)
REQUIRED_COLUMNS = {
    "label", "mAP", "mAP50-95", "precision", "recall", "num_images",
    "num_instances", "epoch", "Training Phase", "input_table_id",
}


class ExportError(Exception):
    """Incomplete, unsupported, or ambiguous source metrics."""


def integer(value: Any, field: str) -> int:
    try:
        number = float(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ExportError(f"Missing or nonnumeric {field}.") from exc
    if not math.isfinite(number) or not number.is_integer() or number < 0:
        raise ExportError(f"Invalid nonnegative integer for {field}.")
    return int(number)


def metric(value: Any, field: str) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ExportError(f"Missing or nonnumeric {field}.") from exc
    if not math.isfinite(number) or not 0 <= number <= 1:
        raise ExportError(f"Invalid metric outside [0, 1] for {field}.")
    return number


def validate_final_rows(
    records: list[dict[str, Any]],
    class_map: dict[int, str] | None,
    *,
    run_url: str,
    metrics_table_url: str,
    validation_table_url: str,
) -> list[dict[str, Any]]:
    """Validate an entire final pass; copy values without filling missing data."""
    if class_map != dict(enumerate(CLASSES)):
        raise ExportError("Expected exactly the 12 competition classes plus 'all'.")
    if len(records) != len(CLASSES):
        raise ExportError("Final validation must contain exactly 13 rows.")

    result: dict[int, dict[str, Any]] = {}
    epochs: set[int] = set()
    for row in records:
        if not REQUIRED_COLUMNS.issubset(row):
            raise ExportError("Final validation rows have missing columns.")
        label = integer(row["label"], "label")
        if label not in range(len(CLASSES)) or label in result:
            raise ExportError("Missing, repeated, or unexpected final class IDs.")
        if integer(row["Training Phase"], "Training Phase") != 1:
            raise ExportError("Final rows must all have Training Phase=After (1).")
        if integer(row["input_table_id"], "input_table_id") != 0:
            raise ExportError("Expected a single referenced validation table (ID 0).")
        epoch = integer(row["epoch"], "epoch")
        if epoch == 0:
            raise ExportError("Final validation has no completed training epoch.")
        epochs.add(epoch)
        result[label] = {
            "class_id": label,
            "class": CLASSES[label],
            "AP50": metric(row["mAP"], "mAP/AP50"),
            "AP50_95": metric(row["mAP50-95"], "mAP50-95"),
            "precision": metric(row["precision"], "precision"),
            "recall": metric(row["recall"], "recall"),
            "num_images": integer(row["num_images"], "num_images"),
            "num_instances": integer(row["num_instances"], "num_instances"),
            "epoch": epoch,
            "training_phase": "After",
            "run_url": run_url,
            "metrics_table_url": metrics_table_url,
            "validation_table_url": validation_table_url,
        }
    if len(epochs) != 1 or set(result) != set(range(len(CLASSES))):
        raise ExportError("Final rows do not describe one complete evaluation pass.")
    classes = [result[i] for i in range(12)]
    aggregate = result[12]
    if not aggregate["num_images"]:
        raise ExportError("Final validation contains no images.")
    if sum(row["num_instances"] for row in classes) != aggregate["num_instances"]:
        raise ExportError("Class instance counts disagree with the native 'all' row.")
    if any(
        row["num_images"] > aggregate["num_images"]
        or row["num_images"] > row["num_instances"]
        for row in classes
    ):
        raise ExportError("Final validation image/instance counts are inconsistent.")
    return [result[i] for i in range(len(CLASSES))]


def collect_final_validation(run_url: str) -> list[dict[str, Any]]:
    """Read only completed Run metadata and its per-class numerical tables."""
    import tlc
    from tlc.constants import RUN_STATUS_COMPLETED

    run = tlc.Run.from_url(run_url)
    if run.status != RUN_STATUS_COMPLETED:
        raise ExportError("Run is not completed; no CSV was written.")
    parameters = (run.constants or {}).get("parameters", {})
    val_url = parameters.get("3LC/val_url")
    if not isinstance(val_url, str) or not val_url:
        raise ExportError("Run has no recorded 3LC/val_url; split is ambiguous.")
    expected_val = tlc.Url(val_url).to_absolute(run.url)
    train_url = parameters.get("3LC/train_url")
    if train_url and tlc.Url(train_url).to_absolute(run.url) == expected_val:
        raise ExportError("Recorded training and validation tables are identical.")

    candidates: list[list[dict[str, Any]]] = []
    for info in run.metrics:
        if info.get("stream_name") != "per_class_metrics":
            continue
        reference = info.get("url")
        if not reference:
            raise ExportError("A per-class metrics reference has no URL.")
        table = tlc.Table.from_url(tlc.Url(reference).to_absolute(run.url))
        foreign = table.get_foreign_table_url()
        if foreign is None:
            raise ExportError("A per-class table has no unique input-table reference.")
        if foreign.to_absolute(table.url) != expected_val:
            continue
        if not REQUIRED_COLUMNS.issubset(table.columns):
            raise ExportError("A validation metrics table has missing columns.")
        if (table.get_simple_value_map("Training Phase") or {}).get(1) != "After":
            raise ExportError("Unrecognized Training Phase schema.")
        # This stream contains only numerical class summaries, not annotations.
        records = table.to_pandas().to_dict("records")
        after = [
            row for row in records
            if integer(row["Training Phase"], "Training Phase") == 1
        ]
        if after:
            candidates.append(validate_final_rows(
                after,
                table.get_simple_value_map("label"),
                run_url=run.url.to_str(),
                metrics_table_url=table.url.to_str(),
                validation_table_url=expected_val.to_str(),
            ))
    if len(candidates) != 1:
        raise ExportError(
            f"Expected one complete final validation pass; found {len(candidates)}. "
            "No epoch fallback or averaging is performed."
        )
    return candidates[0]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-url", required=True, help="Existing 3LC Run URL or directory")
    parser.add_argument("--output", required=True, type=Path, help="New CSV path; parent must exist")
    args = parser.parse_args(argv)
    output = args.output.expanduser().absolute()
    try:
        if output.suffix.lower() != ".csv":
            raise ExportError("Output must have a .csv extension.")
        if output.exists() or output.is_symlink():
            raise ExportError("Output already exists; refusing to overwrite it.")
        if not output.parent.is_dir():
            raise ExportError("Output parent directory does not exist.")
        rows = collect_final_validation(args.run_url)
        text = io.StringIO(newline="")
        writer = csv.DictWriter(text, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
        # Exclusive creation also prevents a race from overwriting any file.
        with output.open("x", encoding="utf-8", newline="") as handle:
            handle.write(text.getvalue())
        print(f"Exported 13 final validation rows to {output}")
        return 0
    except (ExportError, OSError) as exc:
        print(f"Export refused: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:
        # Avoid printing SDK objects, credentials, or native logs in a traceback.
        print(f"Export refused: SDK read failed ({type(exc).__name__}).", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
