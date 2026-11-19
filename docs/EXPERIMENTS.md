# Experiment protocol

E00 used original train and validation revisions, 10 epochs, batch 4, seed 0, and the official plugin. It achieved final validation AP50 0.633096 and Kaggle public score 0.56515.

E00's `epochs=10` and `close_mosaic=10` disabled mosaic before epoch 1. E10 evaluated a 30-epoch cosine schedule with AdamW, batch 8, workers 2 and mosaic for the first 20 epochs. The run stalled during epoch 5 after four completed epochs. The participant approved restarting the Kaggle worker. [E10 settings and recovery record](../configs/E10-experiment.json)

E11 retried with workers set to 0 and `warmup_bias_lr=0.0` and completed all 30 epochs. Its selected checkpoint reached 0.693278 validation AP50, with gains in all 12 classes. On Kaggle, it improved public AP50 from 0.56515 to 0.62263. The changed parameters were tested together. [E11 configuration](../configs/E11-experiment.json) · [Results](../results/E11/RESULTS.md)

E13 used the same official starting weights and initial train and validation revisions, with a 50-epoch cosine schedule and mosaic for the first 20 epochs. A host reboot interrupted the run in epoch 13. Its best epoch-history AP50 was 0.58645 at epoch 12. The competition plugin starts every new run from the pinned weights and rejects checkpoint resume. [E13 configuration](../configs/E13-experiment.json) · [Interruption record](../results/E13/status.json)

For label-quality experiments, use the native Dashboard workflows to present model-derived candidates to the participant. The participant reviews each change and commits a descriptively named training-table revision. Preserve the original validation revision for comparable measurements. Compare otherwise identical runs before and after each batch of changes; each run still starts from the pinned official initialization.

The participant saved E01 as a direct child of `exdark_train/initial`. Its 14 changed training rows contain 13 pure box additions and one People-to-Table replacement. All 14 accepted rectangles match E11's native predictions. The participant rechecked the replacement in example 5580. E01 completed E11's exact 30-epoch schedule, original validation table and unweighted sampling. Its selected checkpoint scored 0.696076 validation AP50. Public AP50 improved from 0.62263 for E11 to 0.63733 for E01. [E01 revision audit and configuration](../configs/E01-experiment.json) · [Results](../results/E01/RESULTS.md)

The participant saved E03 as a direct child of `exdark_train/E01_reviewed_chair_table`. The 3LC SDK resolved and compared all 5,910 rows. Three rows each contain one Chair box geometry edit. The ordered labels, images, effective weights, and schema match E01. With the same training settings, final validation AP50 remained close to E01 at 0.695916. Chair AP50 fell by 3.18 percentage points and Table AP50 rose by 2.25 percentage points. [E03 revision audit and configuration](../configs/E03-experiment.json) · [Results](../results/E03/RESULTS.md)

W01 uses `exdark_train/Modified1297Values`, which sets Weight to 1.5 for exactly 1,297 training images with a supplied Chair or Table label. The other 4,613 have weight 1.0. The SDK verified all rows, schema, image references, and boxes against `initial`. W01 selected that exact revision and `exdark_val/initial` with **Use latest revision** off and **Use sampling weights** on. This activates sampling with replacement. Compare overall and per-class AP50 against E11, the matched training configuration. [W01 configuration](../configs/W01-experiment.json)

W01 finished with 0.696537 validation AP50, up 0.003259 from E11. Chair gained 0.017199 and Table gained 0.005687. Kaggle public AP50 improved from 0.62263 to 0.63189. W02 extended the weighted run to a 50-epoch cosine schedule with the same first 20 mosaic epochs and a patience of eight. It completed all 50 epochs and reached 0.692656 validation AP50. [W01 results](../results/W01/RESULTS.md) · [W02 results](../results/W02/RESULTS.md)

W03 applies W01's Weight rule to E01's reviewed labels through a new native child revision. The 3LC SDK confirmed the original order, image references, box records and schema across all 5,910 rows. The new revision assigns 1.5 to 1,299 Chair or Table images and keeps the effective 1.0 default on the other 4,611. E01 is the control for the effect of weighting reviewed labels. [W03 configuration](../configs/W03-experiment.json)

W03 reached 0.699040 validation AP50, 0.30 percentage points above E01. Validation AP50–95 fell by 0.33 percentage points. Table AP50 rose by 2.71 percentage points and Chair AP50 fell by 0.61 percentage points relative to E01. Kaggle public AP50 fell from 0.63733 on E01 to 0.62555 on W03. The plugin exported 715 predictions and passed all five CSV checks. [W03 results](../results/W03/RESULTS.md)

At saved confidence ≥ 0.10, 533 of E01's 770 unmatched validation objects and 523 of W03's 774 had no prediction of any class with IoU ≥ 0.30. Same-class one-to-one matches at IoU ≥ 0.50 covered 94 of 302 small objects for E01 and 102 for W03, compared with 1,171 and 1,160 of 1,421 large objects. The audit identifies which validation errors account for most missed matches. The public split has independent images and hidden labels. [E01 size audit](../results/E01/validation-size-audit.csv) · [W03 size audit](../results/W03/validation-size-audit.csv)

W04 derives from W03's exact training revision. It multiplies each weight by 1.25 if the image has at least one supplied box whose equivalent square side is below 32 pixels when the image is fitted to 640 pixels. The 3LC SDK verified 549 weight edits and identical image and annotation columns across all 5,910 rows. Expected sampling share across the affected rows increases from 9.45% to 11.54%. The competition host permits changes to the Weight column in this workflow. [W04 revision and settings](../configs/W04-experiment.json) · [Host clarification](https://www.kaggle.com/competitions/the-3lc-low-light-detection-challenge/discussion/744551)

With the project environment and 3LC SDK 3.4.2, prepare the same native weight revision. Omit `--apply` to preview the counts. The command verifies an existing revision of the same name against the expected edits.

```bash
source scripts/env.sh
"$VIRTUAL_ENV/bin/python" -B scripts/create_small_box_weight_revision.py \
    "$TLC_PROJECT_ROOT_URL/exdark-competition/datasets/exdark_train/tables/E01_weighted_chair_table" \
    W04_weighted_small_objects --apply
```

S01 uses E01 as the control because E01 has the highest measured public AP50. The sole training parameter change narrows random affine scaling from 0.50–1.50× to 0.80–1.20×. S01 matched 103 of 302 small validation objects at confidence 0.10 and IoU ≥ 0.50, up from 94 for E01. It matched fewer medium and large objects. Final validation AP50 fell by 1.26 percentage points to 0.683487. [S01 configuration](../configs/S01-experiment.json) · [Results](../results/S01/RESULTS.md)

H01 kept E01's data and training settings and changed `hsv_v` from 0.40 to 0.20. Final validation AP50 fell by 0.45 percentage points to 0.691531. Its small-object matches fell from 94 to 91 of 302 at confidence 0.10 and IoU ≥ 0.50. [H01 configuration](../configs/H01-experiment.json) · [Results](../results/H01/RESULTS.md)

Append completed and active experiments to `experiments.csv`, including native Run URL, revisions, requested/effective settings, duration, final-checkpoint validation metrics, exact submission path and Kaggle score when measured. Leave unknown fields blank. Never equate maximum epoch AP50 with the best checkpoint's final evaluation: the installed Ultralytics version selects `best.pt` by mAP50–95.

Predictions in the Dashboard were collected at confidence 0.1 for E00. Native final validation and the submitted CSV use confidence 0.001. Export max_det is 300; the competition uses its separate COCOeval AP50 specification with maxDets 100. Always label which metric and data split a score describes.

The validation size audit measures one-to-one same-class matches at IoU ≥ 0.50 and a collected confidence threshold of 0.10. Size is the equivalent square side after scaling to fit 640 pixels. E11 matched more medium and large objects, and fewer small objects, than E00. Use final native AP50 for checkpoint comparisons. [E00 box-size breakdown](../results/E00/validation-size-audit.csv) · [E11 box-size breakdown](../results/E11/validation-size-audit.csv)

Run the same audit with the configured local Python and a completed native Run directory:

```bash
source scripts/env.sh
"$VIRTUAL_ENV/bin/python" -B scripts/audit_validation_sizes.py \
    "$TLC_PROJECT_ROOT_URL/exdark-competition/runs/E00_baseline_e10_b4_initial"
```
