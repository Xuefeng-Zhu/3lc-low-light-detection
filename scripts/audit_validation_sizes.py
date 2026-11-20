#!/usr/bin/env python3
"""Compare size-stratified validation matches from saved 3LC Run metrics.

Read only local numerical data. Print an aggregate CSV to stdout. These match
rates use the saved predictions at confidence >= 0.10. They are not AP50.
"""

import argparse
from collections import Counter
import csv
import json
from pathlib import Path
import sys

import numpy as np
import pyarrow.parquet as pq

from export_run_metrics import CLASSES


COORDINATES = ("x_min", "y_min", "x_max", "y_max")
SIZE_BANDS = ("under_32", "32_to_under_96", "96_or_larger")


def metadata(directory):
    return json.loads((directory / "object.3lc.json").read_text())


def load_validation(run_dir, minimum_confidence=0.1, *, require_original=False):
    """Read saved rows with the legacy size-audit checks or confidence-sweep checks."""
    run = metadata(run_dir)
    if run["status"] != 1:
        raise ValueError("Only completed Runs have final validation metrics.")
    parameters = run["constants"]["parameters"]
    collection_floor = parameters["3LC/conf_thres"]
    if parameters["imgsz"] != 640:
        raise ValueError("Comparable audits require a 640 px training resolution.")
    if require_original:
        if not 0 <= collection_floor <= 1 or np.float32(collection_floor) > np.float32(minimum_confidence):
            raise ValueError(f"Collection floor {collection_floor} does not cover cutoff {minimum_confidence}.")
    elif collection_floor != minimum_confidence:
        raise ValueError("Comparable size audits require collection confidence 0.10.")
    val_dir = (run_dir / parameters["3LC/val_url"]).resolve()
    if require_original:
        original = run_dir.parent.parent / "datasets" / "exdark_val" / "tables" / "initial"
        train_dir = (run_dir / parameters["3LC/train_url"]).resolve()
        if val_dir != original.resolve() or train_dir == val_dir:
            raise ValueError("Expected the original validation table and a distinct training table.")
    val_meta = metadata(val_dir)
    row_schema = val_meta["schema"]["values"]["rows"]["values"]
    bbox_schema = row_schema["bbs"]["values"]["instances_additional_data"]["values"]
    label_map = bbox_schema["label"]["value"]["map"]
    class_names = tuple(label_map[f"{index}.0"]["internal_name"] for index in range(12))
    if class_names != CLASSES[:-1] or len(label_map) != 12 or val_meta["row_count"] != 733:
        raise ValueError("Unexpected validation classes or row count.")
    (val_file,) = val_dir.glob("*.parquet")
    truth = pq.read_table(val_file, columns=["bbs"])["bbs"].to_pylist()

    if len(truth) != 733:
        raise ValueError("Unexpected number of validation rows.")
    if require_original and sum(len(group["instances"] or []) for group in truth) != 2725:
        raise ValueError("Expected 2,725 original validation boxes.")
    return truth, load_saved_validation_predictions(run_dir, run, val_dir, len(truth))


def load_saved_validation_predictions(run_dir, run, val_dir, row_count):
    predictions = []
    for entry in run["metrics"]:
        if entry["stream_name"] != "default_stream":
            continue
        metrics_dir = run_dir / entry["url"]
        metric_meta = metadata(metrics_dir)
        schema = metric_meta["schema"]["values"]["rows"]["values"]
        input_map = schema["input_table_id"]["value"]["map"]
        if len(input_map) != 1 or (metrics_dir / input_map["0.0"]["url"]).resolve() != val_dir:
            continue
        phase_map = schema["Training Phase"]["value"]["map"]
        if phase_map["1.0"]["internal_name"] != "After":
            raise ValueError("Unrecognized final validation phase.")
        parquet = metrics_dir / metric_meta["input_url"]
        columns = ["example_id", "bbs_predicted", "Training Phase", "epoch"]
        if "input_table_id" in pq.ParquetFile(parquet).schema_arrow.names:
            columns.append("input_table_id")
        rows = pq.read_table(parquet, columns=columns, filters=[("Training Phase", "=", 1)]).to_pylist()
        if any(row.get("input_table_id", 0) != 0 for row in rows):
            raise ValueError("Unexpected input table ID in final validation predictions.")
        predictions.extend(rows)
    if sorted(row["example_id"] for row in predictions) != list(range(row_count)):
        raise ValueError("Predictions must reference each validation row exactly once.")
    if len({row["epoch"] for row in predictions}) != 1:
        raise ValueError("Final validation chunks must refer to the same epoch.")
    return predictions


def unpack_boxes(group):
    instances = group["instances"] or []
    info = group["instances_additional_data"] or {}
    labels = np.array(info.get("label") or [], dtype=int)
    if len(instances) != len(labels) or not ((0 <= labels) & (labels < 12)).all():
        raise ValueError("Unexpected box or class layout.")
    if any(len(instance["bbs_2d"]) != 1 for instance in instances):
        raise ValueError("Expected exactly one rectangle per instance.")
    boxes = np.array(
        [[instance["bbs_2d"][0][axis] for axis in COORDINATES] for instance in instances],
        dtype=float,
    ).reshape(-1, 4)
    lengths = boxes[:, 2:] - boxes[:, :2]
    if not np.isfinite(boxes).all() or not (lengths > 0).all():
        raise ValueError("Nonfinite or invalid box coordinates.")
    return boxes, labels, lengths.prod(axis=1), info


def validation_geometry(expected, proposed):
    dimensions = np.array([expected["x_max"], expected["y_max"]], dtype=float)
    if not (dimensions > 0).all() or not np.allclose(dimensions, [proposed["x_max"], proposed["y_max"]]):
        raise ValueError("Validation and prediction image dimensions disagree.")
    boxes, labels, areas, _ = unpack_boxes(expected)
    candidates, categories, predicted_areas, info = unpack_boxes(proposed)
    bands = np.digitize(np.sqrt(areas) * 640 / dimensions.max(), (32, 96))
    predicted_bands = np.digitize(np.sqrt(predicted_areas) * 640 / dimensions.max(), (32, 96))
    sides = np.minimum(boxes[:, None, 2:], candidates[None, :, 2:]) - np.maximum(
        boxes[:, None, :2], candidates[None, :, :2]
    )
    intersection = np.maximum(sides, 0).prod(axis=2)
    overlaps = intersection / (areas[:, None] + predicted_areas[None, :] - intersection)
    return labels, bands, categories, predicted_bands, info.get("confidence") or [], overlaps


def claim_matches(labels, categories, scores, overlaps):
    claimed = np.zeros(len(labels), dtype=bool)
    for index in np.argsort(-scores, kind="stable"):
        iou = overlaps[:, index]
        eligible = np.flatnonzero(~claimed & (labels == categories[index]) & (iou >= 0.5))
        if len(eligible):
            claimed[eligible[np.argmax(iou[eligible])]] = True
    return claimed


def count_matches(truth, predictions):
    labeled, matched, any_class = Counter(), Counter(), Counter()
    for row in predictions:
        expected = truth[row["example_id"]]
        proposed = row["bbs_predicted"]
        labels, bands, categories, _, confidence, overlaps = validation_geometry(expected, proposed)
        scores = np.array(confidence, dtype=float)
        if len(scores) != len(categories) or not ((scores >= 0.1 - 1e-6) & (scores <= 1)).all():
            raise ValueError("Missing or invalid prediction confidences.")
        labeled.update(zip(labels, bands))
        has_overlap = (overlaps >= 0.5).any(axis=1)
        any_class.update(zip(labels[has_overlap], bands[has_overlap]))
        claimed = claim_matches(labels, categories, scores, overlaps)
        matched.update(zip(labels[claimed], bands[claimed]))
    return labeled, matched, any_class


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path, help="Completed native Run directory")
    args = parser.parse_args()
    try:
        counts = count_matches(*load_validation(args.run_dir.resolve()))
    except (KeyError, OSError, TypeError, ValueError) as exc:
        parser.exit(2, f"Audit refused: {exc}\n")
    writer = csv.writer(sys.stdout, lineterminator="\n")
    writer.writerow(["class", "size_band_px", "ground_truth", "same_class_matched", "any_class_overlap"])
    for band_index, band in enumerate(SIZE_BANDS):
        for category, name in enumerate(CLASSES[:-1]):
            writer.writerow([name, band, *(counter[category, band_index] for counter in counts)])
        writer.writerow(["all", band, *(sum(counter[c, band_index] for c in range(12)) for counter in counts)])


if __name__ == "__main__":
    main()
