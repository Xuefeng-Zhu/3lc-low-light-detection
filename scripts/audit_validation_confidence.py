#!/usr/bin/env python3
"""Sweep confidence cutoffs on original validation predictions saved by 3LC.

Output CSV to stdout. Match and coverage metrics count ground-truth boxes by
their class and size. Retained detections use predicted class and size.
Cap counts describe the saved rows before applying the sweep cutoffs.
Zero-area prediction counts are reported globally at each cutoff.
"""

import argparse
from collections import Counter
import csv
from pathlib import Path
import sys

import numpy as np

from audit_validation_sizes import (
    SIZE_BANDS,
    claim_matches,
    load_validation,
    metadata,
    validation_geometry,
)
from export_run_metrics import CLASSES


def count_cutoffs(truth, predictions, cutoffs, collection_floor, native_cap, collection_cap):
    ground_truth = Counter()
    sweep = [Counter() for _ in cutoffs]
    cap_rows = Counter()
    for row in predictions:
        expected = truth[row["example_id"]]
        labels, bands, categories, predicted_bands, confidence, overlaps, zero_area = validation_geometry(
            expected, row["bbs_predicted"]
        )
        scores = np.asarray(confidence, dtype=np.float32)
        if len(scores) != len(categories) or not ((scores >= collection_floor) & (scores <= 1)).all():
            raise ValueError("Missing or invalid prediction confidences.")
        if len(scores) > min(native_cap, collection_cap):
            raise ValueError("A saved row exceeds the advertised detection cap.")
        cap_rows["native"] += len(scores) == native_cap
        cap_rows["collection"] += len(scores) == collection_cap
        ground_truth.update(zip(labels, bands))

        for index, cutoff in enumerate(cutoffs):
            retained = scores >= cutoff
            matches = claim_matches(labels, categories[retained], scores[retained], overlaps[:, retained])
            coverage = (overlaps[:, retained] >= 0.30).any(axis=1)
            if index == 0:
                high_matches, high_coverage = matches, coverage
            counts = sweep[index]
            counts["retained_zero_area"] += np.count_nonzero(retained & zero_area)
            for name, classes, size_bands in (
                ("retained", categories[retained], predicted_bands[retained]),
                ("matches", labels[matches], bands[matches]),
                ("coverage", labels[coverage], bands[coverage]),
                ("recovered_matches", labels[matches & ~high_matches], bands[matches & ~high_matches]),
                ("recovered_coverage", labels[coverage & ~high_coverage], bands[coverage & ~high_coverage]),
            ):
                counts.update((name, category, band) for category, band in zip(classes, size_bands))
    return ground_truth, sweep, cap_rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path, help="Completed native Run directory")
    parser.add_argument(
        "--thresholds", nargs="+", type=float, default=[0.1, 0.05, 0.01, 0.001],
        help="Confidence cutoffs, compared with the highest supplied cutoff",
    )
    args = parser.parse_args()
    if any(not 0 <= cutoff <= 1 for cutoff in args.thresholds):
        parser.error("Confidence cutoffs must be finite and in [0, 1].")
    thresholds = sorted(args.thresholds, reverse=True)
    cutoffs = np.asarray(thresholds, dtype=np.float32)
    if len(set(cutoffs)) != len(cutoffs):
        parser.error("Confidence cutoffs must be distinct at float32 precision.")

    run_dir = args.run_dir.resolve()
    try:
        truth, predictions = load_validation(run_dir, thresholds[-1], require_original=True)
        parameters = metadata(run_dir)["constants"]["parameters"]
        native_cap, collection_cap = parameters["max_det"], parameters["3LC/max_det"]
        if any(not isinstance(cap, int) or isinstance(cap, bool) or cap < 1 for cap in (native_cap, collection_cap)):
            raise ValueError("Invalid native or collection detection cap.")
        ground_truth, sweep, cap_rows = count_cutoffs(
            truth, predictions, cutoffs, np.float32(parameters["3LC/conf_thres"]), native_cap, collection_cap
        )
    except (KeyError, OSError, TypeError, ValueError) as exc:
        parser.exit(2, f"Audit refused: {exc}\n")

    writer = csv.writer(sys.stdout, lineterminator="\n")
    writer.writerow([
        "confidence", "reference_confidence", "class", "size_band_px", "ground_truth",
        "retained_detections", "same_class_matched_iou50", "any_class_overlap_iou30",
        "recovered_same_class_matches", "recovered_any_class_overlaps",
        "saved_rows_at_native_cap", "saved_rows_at_collection_cap", "retained_zero_area",
    ])
    for cutoff, counts in zip(thresholds, sweep):
        for category, name in enumerate(CLASSES):
            categories = range(len(CLASSES) - 1) if name == "all" else (category,)
            for band, size in enumerate((*SIZE_BANDS, "all")):
                bands = range(len(SIZE_BANDS)) if size == "all" else (band,)
                keys = [(c, b) for c in categories for b in bands]
                all_rows = name == size == "all"
                writer.writerow([
                    cutoff, thresholds[0], name, size, sum(ground_truth[key] for key in keys),
                    *(sum(counts[metric, *key] for key in keys) for metric in (
                        "retained", "matches", "coverage", "recovered_matches", "recovered_coverage"
                    )),
                    cap_rows["native"] if all_rows else "",
                    cap_rows["collection"] if all_rows else "",
                    counts["retained_zero_area"] if all_rows else "",
                ])


if __name__ == "__main__":
    main()
