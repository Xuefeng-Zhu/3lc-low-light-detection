"""Measure AP50 sensitivity to errors in existing validation predictions."""

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path

import numpy as np

from audit_validation_sizes import SIZE_BANDS, load_validation, unpack_boxes
from evaluate_common_holdout import CLASSES, coco_boxes, score


def original_matches(overlaps, same_class, confidence):
    claimed_boxes, claimed_predictions = set(), set()
    for prediction in np.argsort(-confidence, kind="stable"):
        eligible = np.flatnonzero(same_class[:, prediction] & (overlaps[:, prediction] >= 0.50))
        for box in sorted(eligible, key=lambda index: -overlaps[index, prediction]):
            if box not in claimed_boxes:
                claimed_boxes.add(box)
                claimed_predictions.add(prediction)
                break
    return claimed_boxes, claimed_predictions


def correct_predictions(base, truth_boxes, labels, overlaps, confidence, eligible, boxes, predictions):
    pairs = [(box, prediction) for box in boxes for prediction in predictions if eligible[box, prediction]]
    pairs.sort(key=lambda pair: (-overlaps[pair], -confidence[pair[1]], *pair))
    claimed_boxes, claimed_predictions = set(), set()
    adjusted = [prediction.copy() for prediction in base]
    for box, prediction in pairs:
        if box in claimed_boxes or prediction in claimed_predictions:
            continue
        adjusted[prediction]["category_id"] = int(labels[box]) + 1
        if overlaps[box, prediction] < 0.50:
            adjusted[prediction]["bbox"] = truth_boxes[box]
        claimed_boxes.add(box)
        claimed_predictions.add(prediction)
    return adjusted, claimed_boxes


def summarize_counts(counter):
    return {
        "total": sum(counter.values()),
        "by_size": {
            name: sum(counter[category, size] for category in range(len(CLASSES) - 1))
            for size, name in enumerate(SIZE_BANDS)
        },
        "by_class": {
            name: sum(counter[category, size] for size in range(len(SIZE_BANDS)))
            for category, name in enumerate(CLASSES[:-1])
        },
    }


def audit(run_dir):
    truth, prediction_rows = load_validation(run_dir)
    predictions = {row["example_id"]: row["bbs_predicted"] for row in prediction_rows}
    reference = {
        "info": {},
        "images": [],
        "annotations": [],
        "categories": [{"id": index, "name": name} for index, name in enumerate(CLASSES[:-1], 1)],
    }
    variants = defaultdict(list)
    counts = defaultdict(Counter)
    for index, group in enumerate(truth):
        image_id = index + 1
        predicted = predictions[index]
        width, height = group["x_max"], group["y_max"]
        if (width, height) != (predicted["x_max"], predicted["y_max"]):
            raise ValueError("Validation and prediction image dimensions disagree")
        reference["images"].append({"id": image_id, "width": int(width), "height": int(height)})
        boxes, labels, areas, _ = unpack_boxes(group)
        candidates, categories, candidate_areas, info = unpack_boxes(predicted)
        confidence = np.asarray(info.get("confidence") or [], dtype=float)
        if not ((confidence >= 0.10 - 1e-6) & (confidence <= 1)).all():
            raise ValueError("Invalid saved prediction confidence")
        truth_boxes = coco_boxes(boxes)
        sizes = np.digitize(np.sqrt(areas) * 640 / max(width, height), (32, 96))
        for box, label, area in zip(truth_boxes, labels.tolist(), areas.tolist(), strict=True):
            reference["annotations"].append({
                "id": len(reference["annotations"]) + 1,
                "image_id": image_id, "category_id": label + 1, "bbox": box, "area": area, "iscrowd": 0,
            })
        base = [
            {"image_id": image_id, "category_id": category + 1, "score": conf, "bbox": box}
            for box, category, conf in zip(coco_boxes(candidates), categories.tolist(), confidence.tolist(), strict=True)
        ]
        sides = np.minimum(boxes[:, None, 2:], candidates[None, :, 2:]) - np.maximum(
            boxes[:, None, :2], candidates[None, :, :2]
        )
        intersection = np.maximum(sides, 0).prod(axis=2)
        overlaps = intersection / (areas[:, None] + candidate_areas[None, :] - intersection)
        same_class = labels[:, None] == categories[None, :]
        claimed_boxes, claimed_predictions = original_matches(overlaps, same_class, confidence)
        boxes_left = sorted(set(range(len(boxes))) - claimed_boxes)
        predictions_left = sorted(set(range(len(candidates))) - claimed_predictions)
        counts["unmatched"].update((int(labels[box]), int(sizes[box])) for box in boxes_left)
        variants["baseline"].extend(base)

        wrong_class = ~same_class & (overlaps >= 0.50)
        inaccurate_box = same_class & (overlaps >= 0.30) & (overlaps < 0.50)
        for name, eligible in [
            ("correct_class", wrong_class),
            ("correct_box", inaccurate_box),
            ("correct_class_and_box", wrong_class | inaccurate_box),
        ]:
            adjusted, repaired = correct_predictions(
                base, truth_boxes, labels, overlaps, confidence, eligible, boxes_left, predictions_left
            )
            variants[name].extend(adjusted)
            counts[name].update((int(labels[box]), int(sizes[box])) for box in repaired)

        missing = [box for box in boxes_left if overlaps[box].max(initial=0) < 0.30]
        counts["no_saved_candidate"].update((int(labels[box]), int(sizes[box])) for box in missing)
        for conf in (0.10, 0.50, 1.00):
            variants[f"add_missing_at_{conf:.2f}"].extend(base + [
                {
                    "image_id": image_id, "category_id": int(labels[box]) + 1,
                    "score": conf, "bbox": truth_boxes[box],
                }
                for box in missing
            ])
        variants["remove_unmatched_predictions"].extend(base[index] for index in sorted(claimed_predictions))

    baseline, baseline_classes = score(reference, [item.copy() for item in variants["baseline"]])
    summary = {}
    for name, detections in variants.items():
        ap50, classes = score(reference, [item.copy() for item in detections])
        summary[name] = {
            "predictions": len(detections),
            "AP50": ap50,
            "AP50_difference": ap50 - baseline,
            "AP50_difference_by_class": {name: value - baseline_classes[name] for name, value in classes.items()},
        }
    return {
        "run": run_dir.name,
        "metric": "COCO AP50 at saved confidence >= 0.10 and maxDets=100",
        "images": len(truth),
        "ground_truth_boxes": len(reference["annotations"]),
        "object_counts": {name: summarize_counts(count) for name, count in counts.items()},
        "scenarios": summary,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path, help="Completed native Run with the original 733-image validation table")
    args = parser.parse_args()
    print(json.dumps(audit(args.run_dir.resolve()), indent=2))


if __name__ == "__main__":
    main()
