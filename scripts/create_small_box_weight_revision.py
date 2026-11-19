#!/usr/bin/env python3
"""Create a native training-table revision with higher weights on small-box rows."""

import argparse
from collections import Counter
import json
from pathlib import Path

import numpy as np
import tlc
from tlc._core.objects.tables.from_table.edited_table import EditedTable

from audit_validation_sizes import unpack_boxes


IMAGE_SIZE = 640
SMALL_SIDE = 32
WEIGHT_MULTIPLIER = 1.25


def weight_edits(box_groups, stored_weights):
    indices_by_weight = {}
    expected_weights = stored_weights.copy()
    for index, (group, stored_weight) in enumerate(zip(box_groups, stored_weights, strict=True)):
        _, _, areas, _ = unpack_boxes(group)
        long_side = max(group["x_max"], group["y_max"])
        if long_side <= 0:
            raise ValueError(f"Invalid image size in row {index}")
        if (np.sqrt(areas) * IMAGE_SIZE / long_side < SMALL_SIDE).any():
            weight = 1.0 if stored_weight is None else stored_weight
            new_weight = weight * WEIGHT_MULTIPLIER
            indices_by_weight.setdefault(new_weight, []).append(index)
            expected_weights[index] = new_weight

    runs_and_values = []
    for weight, indices in sorted(indices_by_weight.items()):
        runs_and_values.extend([EditedTable.indices_to_run(indices), weight])
    if not runs_and_values:
        raise ValueError("The source table has no small-box rows")
    edits = {"weight": {"runs_and_values": runs_and_values}}
    return edits, expected_weights, {weight: len(indices) for weight, indices in indices_by_weight.items()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("parent", type=Path, help="Local training-table revision directory")
    parser.add_argument("name", help="Name of the new sibling-directory revision")
    parser.add_argument("--apply", action="store_true", help="Save the revision and verify its stored rows")
    args = parser.parse_args()
    parent_path = args.parent.resolve()
    if args.name in {"", ".", ".."} or Path(args.name).name != args.name:
        parser.error("name must be one directory name")
    child_path = parent_path.with_name(args.name)
    parent = tlc.Table.from_url(str(parent_path))
    if parent.weights_column_name != "weight":
        parser.error("the source revision needs the native Weight column")
    images = parent.get_column_as_pyarrow_array("image")
    annotations = parent.get_column_as_pyarrow_array("bbs")
    stored_weights = parent.get_column_as_pyarrow_array("weight").to_pylist()
    edits, expected_weights, updated = weight_edits(annotations.to_pylist(), stored_weights)
    if args.apply:
        native_path = child_path / "object.3lc.json"
        if not child_path.exists():
            child = EditedTable(
                url=tlc.Url(str(child_path)),
                input_table_url=parent,
                edits=edits,
                description="Multiply existing weights by 1.25 for images with a supplied box under 32 px at 640 px.",
            )
            child.ensure_fully_defined()
            if not native_path.is_file():
                child.write_to_url()
        native = json.loads(native_path.read_text())
        if native["edits"] != edits or (child_path / native["input_table_url"]).resolve() != parent_path:
            raise RuntimeError("The saved native revision failed the lineage and column checks")
        saved = tlc.Table.from_url(str(child_path))
        if (
            len(saved) != len(parent)
            or saved.rows_schema.to_minimal_dict(include_all=False)
            != parent.rows_schema.to_minimal_dict(include_all=False)
            or not saved.get_column_as_pyarrow_array("image").equals(images)
            or not saved.get_column_as_pyarrow_array("bbs").equals(annotations)
            or saved.get_column_as_pyarrow_array("weight").to_pylist() != expected_weights
        ):
            raise RuntimeError("The saved native revision failed the row and column checks")
    print(json.dumps({
        "revision": args.name,
        "parent": parent_path.name,
        "applied": args.apply,
        "row_count": len(parent),
        "changed_rows_by_weight": updated,
        "effective_weights": dict(Counter(1.0 if weight is None else weight for weight in expected_weights)),
    }, indent=2))


if __name__ == "__main__":
    main()
