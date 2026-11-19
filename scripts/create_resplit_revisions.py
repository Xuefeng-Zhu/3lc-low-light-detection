#!/usr/bin/env python3
"""Preview or save the deterministic R01 ExDark re-split."""

import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import tempfile

import numpy as np
import pyarrow as pa
import tlc

from audit_validation_sizes import CLASSES, unpack_boxes


TRAIN_CHAIN = ("E04_reviewed_missing_chair_table", "E03_reviewed_chair_boxes",
               "E01_reviewed_chair_table", "initial")
SALT = "R01|2026-11-19"
COLUMNS = ["image", "bbs", "weight"]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def metadata(path):
    return json.loads((path / "object.3lc.json").read_text())


def reference(owner, url):
    return Path(tlc.Url(url).to_absolute(tlc.Url(str(owner))).to_str()).resolve()


def expand_runs(runs):
    indices = set()
    for run in runs:
        start = None
        for value in run:
            if value < 0:
                require(start is not None and start < -value, "Invalid native row range")
                indices.update(range(start + 1, -value + 1))
                start = None
            else:
                indices.add(value)
                start = value
    return indices


def reviewed_rows(train_directory):
    rows = set()
    for revision, parent in zip(TRAIN_CHAIN[:-1], TRAIN_CHAIN[1:], strict=True):
        path = train_directory / revision
        obj = metadata(path)
        require(obj["type"] == "EditedTable" and obj["row_count"] == 5910,
                f"Unexpected source revision {revision}")
        require(reference(path, obj["input_table_url"]) == train_directory / parent,
                f"Unexpected parent of {revision}")
        require(set(obj["edits"]) == {"bbs"}, f"Unexpected edit column in {revision}")
        rows.update(expand_runs(obj["edits"]["bbs"]["runs_and_values"][::2]))
    require(len(rows) == 19 and all(0 <= row < 5910 for row in rows), "Unexpected reviewed row set")
    return rows


def load_rows(path, count):
    table = tlc.Table.from_url(str(path))
    require(len(table) == count and table.columns == COLUMNS, f"Unexpected shape of {path.name}")
    image, bbs, weight = (table.get_column_as_pyarrow_array(column) for column in COLUMNS)
    images = [reference(path, url) for url in image.to_pylist()]
    require(len(set(images)) == len({image.name for image in images}) == count,
            f"Duplicate canonical images or filenames in {path.name}")
    require(all(image.is_file() for image in images), f"Missing image source for {path.name}")
    return table, images, bbs, weight


def small_rows(boxes):
    eligible = set()
    for index, group in enumerate(boxes.to_pylist()):
        _, _, areas, _ = unpack_boxes(group)
        long_side = max(group["x_max"], group["y_max"])
        require(np.isfinite(long_side) and long_side > 0, "Invalid supplied image dimensions")
        if (np.sqrt(areas) * 640 / long_side < 32).any():
            eligible.add(index)
    return eligible


def select(indices, images, group, count):
    def sort_key(index):
        filename = images[index].name
        return hashlib.sha256(f"{SALT}|{group}|{filename}".encode()).digest(), filename

    require(len(indices) >= count, f"Not enough eligible images for {group}")
    return set(sorted(indices, key=sort_key)[:count])


def ordered_take(source, indices):
    _, images, boxes, weights = source
    arrow_indices = pa.array(indices, type=pa.int64())
    return [images[i] for i in indices], boxes.take(arrow_indices), weights.take(arrow_indices)


def with_image_origins(array):
    groups = array.to_pylist()
    for group in groups:
        for field in ("x_min", "y_min"):
            if group[field] is None:
                group[field] = 0.0
    return groups


def effective_weights(array):
    return [1.0 if value is None else value for value in array.to_pylist()]


def verify_revision(path, parents, expected, schema, deleted=None):
    obj = metadata(path)
    if deleted is None:
        require(obj["type"] == "JoinedTable", f"{path.name} is not a native JoinedTable")
        sources = obj["input_table_urls"]
        # JoinedTable supplies its own top-level description for the row schema.
        schema = {**schema, "description": "A property containing the table rows within this JoinedTable"}
    else:
        require(obj["type"] == "EditedTable", f"{path.name} is not a native EditedTable")
        sources = [obj["input_table_url"]]
        require(len(obj["edits"]) == 1, f"{path.name} has extra edits")
        key, edit = next(iter(obj["edits"].items()))
        require(key == tlc.constants.SHOULD_DELETE, f"{path.name} has an unexpected edit column")
        runs = edit["runs_and_values"]
        require(len(runs) % 2 == 0 and all(value is True for value in runs[1::2])
                and expand_runs(runs[::2]) == deleted, f"{path.name} has different deleted row IDs")
    require([reference(path, url) for url in sources] == parents, f"Incorrect lineage for {path.name}")
    table, images, boxes, weights = load_rows(path, len(expected[0]))
    require(table.rows_schema.to_minimal_dict(include_all=False) == schema, f"Schema changed in {path.name}")
    if deleted is None:
        # Joining materializes the schema defaults and may rename Arrow list fields.
        boxes_match = with_image_origins(boxes) == with_image_origins(expected[1])
        weights_match = effective_weights(weights) == effective_weights(expected[2])
    else:
        boxes_match = boxes.equals(expected[1])
        weights_match = weights.equals(expected[2])
    require(images == expected[0] and boxes_match and weights_match,
            f"Ordered images, annotations or weights differ in {path.name}")
    return table


def check_existing(path, verify):
    if path.exists() or path.is_symlink():
        require(not path.is_symlink() and (path / "object.3lc.json").is_file(),
                f"Existing output is not a complete native revision at {path}")
        return verify()
    return None


def write_manifest(path, manifest):
    if path.exists():
        require(json.loads(path.read_text()) == manifest, "Existing manifest does not match R01")
        return
    with tempfile.NamedTemporaryFile(mode="w", dir=path.parent, delete=False) as handle:
        temporary = Path(handle.name)
        json.dump(manifest, handle, indent=2)
        handle.write("\n")
    try:
        os.link(temporary, path)
    except FileExistsError:
        require(json.loads(path.read_text()) == manifest, "Concurrent manifest does not match R01")
    finally:
        temporary.unlink()


def run(project, apply, manifest_path):
    train_dir = project / "datasets/exdark_train/tables"
    val_dir = project / "datasets/exdark_val/tables"
    train_path, val_path = train_dir / TRAIN_CHAIN[0], val_dir / "initial"
    train = load_rows(train_path, 5910)
    val = load_rows(val_path, 733)
    schema = train[0].rows_schema.to_minimal_dict(include_all=False)
    require(schema == val[0].rows_schema.to_minimal_dict(include_all=False), "Source schemas differ")
    require(not set(train[1]).intersection(val[1]), "Training and validation source images overlap")
    require(train[3].null_count == len(train[1]) and val[3].null_count == len(val[1]),
            "Source stored weights differ from expected defaults")

    reviewed = reviewed_rows(train_dir)
    train_small, val_small = small_rows(train[2]), small_rows(val[2])
    require(len(train_small) == 549 and len(val_small) == 131, "Unexpected small-bearing source counts")
    train_ids, val_ids = set(range(5910)), set(range(733))
    pruned = select(train_ids - (reviewed | train_small), train[1], "train-prune", 440)
    donors = select(val_small, val[1], "val-donor-small", 79) | select(val_ids - val_small, val[1], "val-donor-other", 361)
    retained, holdout = sorted(train_ids - pruned), sorted(val_ids - donors)
    donor_ids = sorted(donors)
    parts = [
        (train_dir / "R01_train_retained", train, train_path, retained, pruned),
        (val_dir / "R01_val_donor", val, val_path, donor_ids, val_ids - donors),
        (val_dir / "R01_holdout", val, val_path, holdout, donors),
    ]
    expected = [ordered_take(source, keep) for _, source, _, keep, _ in parts]
    holdout_support = Counter(
        label
        for group in expected[2][1].to_pylist()
        for label in group["instances_additional_data"]["label"]
    )
    require(set(holdout_support) == set(range(len(CLASSES) - 1)), "A class is absent from the holdout")
    joined_path = train_dir / "R01_rebalanced_train"
    joined_parents = [parts[0][0], parts[1][0]]
    joined = (expected[0][0] + expected[1][0],
              pa.concat_arrays([expected[0][1], expected[1][1]]),
              pa.concat_arrays([expected[0][2], expected[1][2]]))
    require(len(joined[0]) == len(set(joined[0])) == 5910 and len(holdout) == 293
            and not set(joined[0]).intersection(expected[2][0]), "Incorrect split membership")
    manifest = {
        "experiment": "R01",
        "salt": SALT,
        "original_train_revision": TRAIN_CHAIN[0],
        "original_val_revision": "initial",
        "rebalanced_train_revision": joined_path.name,
        "holdout_revision": parts[2][0].name,
        "holdout_row_ids": holdout,
        "donor_row_ids": donor_ids,
        "train_pruned_row_ids": sorted(pruned),
        "joined_defaults": {
            "unrecorded_image_origin": [0.0, 0.0],
            "unrecorded_sampling_weight": 1.0,
        },
        "holdout_instances_by_class": {
            name: holdout_support[index] for index, name in enumerate(CLASSES[:-1])
        },
        "aggregates": {
            "original_train_rows": 5910, "original_val_rows": 733,
            "train_retained_rows": len(retained), "donor_rows": len(donor_ids),
            "rebalanced_train_rows": len(joined[0]), "holdout_rows": len(holdout),
            "reviewed_train_rows_retained": len(reviewed), "small_train_rows_retained": len(train_small),
            "small_original_val_rows": len(val_small), "small_donor_rows": len(donors & val_small),
            "small_holdout_rows": len(set(holdout) & val_small),
        },
    }
    if apply:
        require(manifest_path.parent.is_dir() and not manifest_path.is_symlink(),
                "Manifest must be a regular file path with an existing parent directory")
        if manifest_path.exists():
            require(json.loads(manifest_path.read_text()) == manifest, "Existing manifest does not match R01")
    # Check every existing output before creating any missing output.
    existing = []
    for (path, _, parent, _, removed), rows in zip(parts, expected, strict=True):
        existing.append(check_existing(path, lambda: verify_revision(path, [parent], rows, schema, removed)))
    existing_join = check_existing(joined_path, lambda: verify_revision(joined_path, joined_parents, joined, schema))
    if apply:
        for index, ((path, source, parent, _, removed), rows) in enumerate(zip(parts, expected, strict=True)):
            if existing[index] is None:
                table = source[0].delete_rows(sorted(removed), table_url=str(path), description=f"R01 {path.name}")
                require(reference(project, table.url.to_str()) == path, f"SDK selected a different revision path for {path.name}")
                existing[index] = verify_revision(path, [parent], rows, schema, removed)
        if existing_join is None:
            tlc.Table.join_tables(existing[:2], table_url=str(joined_path), if_exists="raise",
                                  add_weight_column=False,
                                  description="R01 retained original training rows and original validation donors.")
            verify_revision(joined_path, joined_parents, joined, schema)
        write_manifest(manifest_path, manifest)
    return manifest["aggregates"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path, help="Local exdark-competition project directory")
    parser.add_argument("--apply", action="store_true", help="Save and verify the native revisions")
    parser.add_argument("--manifest", type=Path, help="New JSON manifest path (required with --apply)")
    args = parser.parse_args()
    if args.apply and args.manifest is None:
        parser.error("--apply requires --manifest")
    try:
        metrics = run(args.project.resolve(), args.apply, args.manifest.absolute() if args.manifest else None)
    except (KeyError, OSError, TypeError, ValueError, RuntimeError) as error:
        parser.exit(2, f"R01 refused: {error}\n")
    print(json.dumps({"applied": args.apply, **metrics}, indent=2))


if __name__ == "__main__":
    main()
