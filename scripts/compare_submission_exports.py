"""Check whether an official lower-threshold export only appends detections."""

import argparse
import csv
import json
from pathlib import Path

COLUMNS = ["id", "image_id", "prediction_string"]


def read_export(path):
    images = []
    detections = []
    with path.open(newline="") as source:
        records = csv.DictReader(source)
        if records.fieldnames != COLUMNS:
            raise ValueError(f"Unexpected submission columns in {path.name}")
        for row in records:
            values = [] if row["prediction_string"] == "no box" else row["prediction_string"].split()
            if len(values) % 6:
                raise ValueError(f"Invalid detection encoding in {path.name}")
            images.append((row["id"], row["image_id"]))
            detections.append([tuple(values[start:start + 6]) for start in range(0, len(values), 6)])
    if len(images) != 715 or len(set(images)) != 715:
        raise ValueError(f"Expected 715 unique image rows in {path.name}")
    return images, detections


def compare(original, lower):
    images, first = read_export(original)
    other_images, second = read_export(lower)
    if images != other_images:
        raise ValueError("The official exports have different image keys or order")

    altered_images = 0
    added_scores = []
    first_scores = [float(box[1]) for row in first for box in row]
    for first_row, second_row in zip(first, second, strict=True):
        if second_row[:len(first_row)] != first_row:
            altered_images += 1
            continue
        added_scores.extend(float(box[1]) for box in second_row[len(first_row):])
    min_first = min(first_scores)
    equal_score_additions = sum(score == min_first for score in added_scores)
    higher_score_additions = sum(score > min_first for score in added_scores)
    return {
        "images": len(images),
        "old_predictions": len(first_scores),
        "new_predictions": sum(map(len, second)),
        "image_rows_with_changed_existing_predictions": altered_images,
        "appended_predictions_in_unchanged_rows": len(added_scores),
        "lowest_original_score": min_first,
        "highest_appended_score": max(added_scores, default=None),
        "appended_predictions_at_lowest_original_score": equal_score_additions,
        "appended_predictions_above_lowest_original_score": higher_score_additions,
        "strict_low_score_extension": altered_images == 0 and equal_score_additions == 0 and higher_score_additions == 0,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("original", type=Path)
    parser.add_argument("lower_threshold", type=Path)
    args = parser.parse_args()
    print(json.dumps(compare(args.original, args.lower_threshold), indent=2))
