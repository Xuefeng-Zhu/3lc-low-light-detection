#!/usr/bin/env python3
"""Compare native saved validation predictions on an identical held-out subset."""

import argparse
from collections import Counter
from contextlib import redirect_stdout
from io import StringIO
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit

import numpy as np
from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval
import tlc

from audit_validation_sizes import CLASSES, load_saved_validation_predictions, metadata, unpack_boxes


def image_paths(table, table_dir):
    paths = []
    for value in table.get_column_as_pyarrow_array("image").to_pylist():
        url = urlsplit(value)
        if url.scheme not in ("", "file") or url.netloc not in ("", "localhost"):
            raise ValueError("Expected a local image reference")
        paths.append((table_dir / unquote(url.path)).resolve(strict=True))
    if len(paths) != len(set(paths)):
        raise ValueError("An image occurs more than once in a split")
    return paths


def coco_boxes(boxes):
    return np.hstack((boxes[:, :2], boxes[:, 2:] - boxes[:, :2])).tolist()


def holdout_reference(initial_dir, holdout_dir):
    initial = tlc.Table.from_url(str(initial_dir))
    original = dict(zip(
        image_paths(initial, initial_dir),
        initial.get_column_as_pyarrow_array("bbs").to_pylist(),
        strict=True,
    ))
    holdout = tlc.Table.from_url(str(holdout_dir))
    image_ids = {}
    images, annotations = [], []
    support = Counter()
    for index, (path, group) in enumerate(zip(
        image_paths(holdout, holdout_dir),
        holdout.get_column_as_pyarrow_array("bbs").to_pylist(),
        strict=True,
    ), start=1):
        if path not in original or group != original[path]:
            raise ValueError("The holdout must preserve the original validation image and boxes")
        image_ids[path] = index
        images.append({"id": index, "width": int(group["x_max"]), "height": int(group["y_max"])})
        boxes, labels, areas, _ = unpack_boxes(group)
        for bbox, label, area in zip(coco_boxes(boxes), labels.tolist(), areas.tolist(), strict=True):
            support[label] += 1
            annotations.append({
                "id": len(annotations) + 1, "image_id": index, "category_id": label + 1,
                "bbox": bbox, "area": area, "iscrowd": 0,
            })
    if len(support) != len(CLASSES) - 1:
        raise ValueError("The holdout must contain original annotations from all 12 classes")
    return image_ids, support, {
        "info": {},
        "images": images,
        "categories": [{"id": index, "name": label} for index, label in enumerate(CLASSES[:-1], 1)],
        "annotations": annotations,
    }


def run_detections(run_dir, image_ids, images):
    run = metadata(run_dir)
    params = run["constants"]["parameters"]
    if (run["status"], params["imgsz"], params["3LC/conf_thres"], params["3LC/max_det"]) != (1, 640, 0.1, 300):
        raise ValueError(f"{run_dir.name} must be complete with 640px, confidence 0.10 and max detections 300")
    training_dir = (run_dir / params["3LC/train_url"]).resolve()
    training = tlc.Table.from_url(str(training_dir))
    if image_ids.keys() & set(image_paths(training, training_dir)):
        raise ValueError(f"{run_dir.name} trained on an image in the holdout")
    validation_dir = (run_dir / params["3LC/val_url"]).resolve()
    validation = tlc.Table.from_url(str(validation_dir))
    validation_paths = image_paths(validation, validation_dir)
    if not image_ids.keys() <= set(validation_paths):
        raise ValueError(f"{run_dir.name} does not cover the entire holdout")
    rows = load_saved_validation_predictions(run_dir, run, validation_dir, len(validation_paths))
    detections = []
    for row in rows:
        path = validation_paths[row["example_id"]]
        if path not in image_ids:
            continue
        image_id = image_ids[path]
        expected = images[image_id - 1]
        predicted = row["bbs_predicted"]
        if (predicted["x_max"], predicted["y_max"]) != (expected["width"], expected["height"]):
            raise ValueError("Prediction and annotation image dimensions differ")
        boxes, labels, _, info = unpack_boxes(predicted)
        scores = info.get("confidence") or []
        if not all(0.10 - 1e-6 <= score <= 1 for score in scores):
            raise ValueError("Invalid or mismatched saved prediction confidence")
        for bbox, label, score in zip(coco_boxes(boxes), labels.tolist(), scores, strict=True):
            detections.append({
                "image_id": image_id, "category_id": label + 1, "score": score, "bbox": bbox,
            })
    return detections


def score(reference, detections):
    with redirect_stdout(StringIO()):
        truth = COCO()
        truth.dataset = reference
        truth.createIndex()
        if detections:
            predicted = truth.loadRes(detections)
        else:
            predicted = COCO()
            predicted.dataset = {**reference, "annotations": []}
            predicted.createIndex()
        evaluator = COCOeval(truth, predicted, "bbox")
        evaluator.params.iouThrs = np.array([0.5])
        evaluator.params.maxDets = [1, 10, 100]
        evaluator.evaluate()
        evaluator.accumulate()
    precision = evaluator.eval["precision"][0, :, :, 0, -1]
    return float(precision[precision >= 0].mean()), {
        name: float(values[values >= 0].mean())
        for name, values in zip(CLASSES[:-1], precision.T, strict=True)
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("initial", type=Path, help="Original validation table")
    parser.add_argument("holdout", type=Path, help="Subset of the original validation table")
    parser.add_argument("runs", type=Path, nargs="+", help="Completed native Run directories")
    args = parser.parse_args()
    image_ids, support, reference = holdout_reference(args.initial.resolve(), args.holdout.resolve())
    results = []
    for run_dir in args.runs:
        detections = run_detections(run_dir.resolve(), image_ids, reference["images"])
        ap50, by_class = score(reference, detections)
        results.append({
            "run": run_dir.name, "AP50": ap50, "AP50_by_class": by_class, "predictions": len(detections),
        })
    print(json.dumps({
        "metric": "COCO AP50 at saved confidence >= 0.10 and maxDets=100",
        "holdout": args.holdout.name,
        "images": len(image_ids),
        "annotations": {name: support[index] for index, name in enumerate(CLASSES[:-1])},
        "results": results,
    }, indent=2))


if __name__ == "__main__":
    main()
