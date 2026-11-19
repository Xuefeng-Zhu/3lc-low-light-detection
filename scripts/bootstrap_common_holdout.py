"""Estimate paired COCO AP50 differences by resampling whole validation images."""

import argparse
from collections import defaultdict
from contextlib import redirect_stdout
from io import StringIO
from itertools import combinations
import json
from pathlib import Path

import numpy as np
from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval

from evaluate_common_holdout import holdout_reference, run_detections, score


def match_by_image(reference, detections):
    with redirect_stdout(StringIO()):
        truth = COCO()
        truth.dataset = reference
        truth.createIndex()
        predicted = truth.loadRes(detections)
        evaluator = COCOeval(truth, predicted, "bbox")
        evaluator.params.iouThrs = np.array([0.5])
        evaluator.params.maxDets = [1, 10, 100]
        evaluator.evaluate()
    n = len(evaluator.params.imgIds)
    area_ranges = len(evaluator.params.areaRng)
    results = np.asarray(evaluator.evalImgs, dtype=object).reshape(-1, area_ranges, n)[:, 0, :]
    classes = []
    for group in results:
        support = [0 if row is None else np.count_nonzero(~row["gtIgnore"].astype(bool))
                   for row in group]
        scores = [np.array([]) if row is None else np.asarray(row["dtScores"])[~row["dtIgnore"][0]]
                  for row in group]
        matched = [np.array([], dtype=bool) if row is None
                   else row["dtMatches"][0][~row["dtIgnore"][0]].astype(bool) for row in group]
        classes.append((np.asarray(support), scores, matched))
    return classes


def sampled_ap50(matches, sample):
    thresholds = np.linspace(0, 1, 101)
    by_class = []
    for support, scores, matched in matches:
        count = support[sample].sum()
        if count == 0:
            continue
        selected_scores = np.concatenate([scores[index] for index in sample])
        selected_matched = np.concatenate([matched[index] for index in sample])
        order = np.argsort(-selected_scores, kind="stable")
        true_positives = np.cumsum(selected_matched[order])
        recall = true_positives / count
        precision = true_positives / (np.arange(1, len(order) + 1) + np.spacing(1))
        envelope = np.maximum.accumulate(precision[::-1])[::-1]
        indices = np.searchsorted(recall, thresholds)
        by_class.append(np.append(envelope, 0)[indices].mean())
    return float(np.mean(by_class))


def direct_resample_score(reference, detections, sample):
    source_images = reference["images"]
    annotations_by_image = defaultdict(list)
    detections_by_image = defaultdict(list)
    for annotation in reference["annotations"]:
        annotations_by_image[annotation["image_id"]].append(annotation)
    for detection in detections:
        detections_by_image[detection["image_id"]].append(detection)
    images, annotations, resampled_detections = [], [], []
    for new_id, index in enumerate(sample, 1):
        source = source_images[index]
        images.append({**source, "id": new_id})
        for annotation in annotations_by_image[source["id"]]:
            annotations.append({**annotation, "id": len(annotations) + 1, "image_id": new_id})
        for detection in detections_by_image[source["id"]]:
            resampled_detections.append({**detection, "image_id": new_id})
    return score({**reference, "images": images, "annotations": annotations}, resampled_detections)[0]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("initial", type=Path)
    parser.add_argument("holdout", type=Path)
    parser.add_argument("runs", type=Path, nargs="+")
    parser.add_argument("--draws", type=int, default=2000)
    args = parser.parse_args()
    if len(args.runs) < 2 or args.draws < 1:
        parser.error("Provide at least two runs and at least one bootstrap draw")
    image_ids, _, reference = holdout_reference(args.initial.resolve(), args.holdout.resolve())
    n = len(image_ids)
    seed = 20261119
    generator = np.random.default_rng(seed)
    draws = np.sort(generator.integers(n, size=(args.draws, n)), axis=1)
    observed = {}
    bootstrap = {}
    for run in args.runs:
        detections = run_detections(run.resolve(), image_ids, reference["images"])
        matches = match_by_image(reference, detections)
        observed[run.name] = score(reference, detections)[0]
        for sample, expected in [
            (np.arange(n), observed[run.name]),
            (draws[0], direct_resample_score(reference, detections, draws[0])),
        ]:
            if not np.isclose(sampled_ap50(matches, sample), expected, atol=1e-12, rtol=0):
                raise ValueError(f"Resampled AP50 disagrees with pycocotools for {run.name}")
        bootstrap[run.name] = np.asarray([sampled_ap50(matches, draw) for draw in draws])
    comparisons = []
    for control, trial in combinations(observed, 2):
        delta = bootstrap[trial] - bootstrap[control]
        comparisons.append({
            "trial": trial,
            "control": control,
            "AP50_difference": observed[trial] - observed[control],
            "paired_percentile_95_interval": np.quantile(delta, [0.025, 0.975]).tolist(),
            "fraction_positive": float(np.mean(delta > 0)),
        })
    print(json.dumps({
        "metric": "COCO AP50 at saved confidence >= 0.10 and maxDets=100",
        "holdout": args.holdout.name,
        "images": n,
        "paired_image_bootstrap_draws": args.draws,
        "numpy_random_seed": seed,
        "verified_against_full_coco_evaluation_for": ["original sample", "first bootstrapped sample"],
        "observed_AP50": observed,
        "comparisons": comparisons,
    }, indent=2))


if __name__ == "__main__":
    main()
