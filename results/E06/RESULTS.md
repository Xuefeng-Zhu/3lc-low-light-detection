# E06 results

E06 added seven participant-reviewed boxes to E01’s training labels and retained E01’s validation table and 30-epoch optimization settings. The native plugin finished in 228.61 minutes and selected epoch 28. All four model provenance checks passed. [Revision verification](verification.json) · [Settings](../../configs/E06-experiment.json) · [Provenance](provenance.json)

| Selected-checkpoint validation | E01 | E06 | Change |
| --- | ---: | ---: | ---: |
| mAP@0.5 | 0.696076 | 0.693486 | −0.002590 |
| mAP@0.5:0.95 | 0.444086 | 0.440994 | −0.003092 |
| Chair AP50 | 0.573601 | 0.549261 | −0.024339 |
| Table AP50 | 0.560161 | 0.543324 | −0.016837 |
| Precision | 0.757583 | 0.760225 | +0.002642 |
| Recall | 0.599035 | 0.604350 | +0.005314 |

Both runs evaluated the same 733 images and 2,725 ground-truth boxes. [Per-class metrics](final-validation-per-class.csv)

In the training history, mAP@0.5 peaked at 0.69689 in epoch 29, and mAP@0.5:0.95 peaked at 0.44103 in epoch 28. [Epoch metrics](epoch-results.csv) · [Native curves](training-curves.png)

On the matched 293-image COCO holdout, E06 reached **0.627131 AP50** versus **0.624649** for E01, an increase of 0.002482, using saved predictions with confidence ≥0.10 and maxDets 100. Both checkpoints were selected on the full original validation set, which includes the common holdout. [E06 holdout scores](common-holdout-scores.json) · [E01 reference scores](../R01/reference-scores.json)

On all 733 original validation images, COCO AP50 fell from 0.651052 to 0.649446. [Full validation COCO scores](full-validation-coco-scores.json)

## Confidence sweep

On the same E06 validation outputs, lowering the cutoff from 0.10 to 0.001 increased correct small-box matches from **96 to 222 of 302** and overall matches from 1,942 to 2,524 of 2,725. Retained predictions rose from 4,064 to 61,859. The lower cutoff includes 78 clipped zero-area detections, which contribute to counts and cannot match a positive-area box. With COCO maxDets 100, AP50 rose from **0.649446 to 0.691548**. These are two cutoffs applied to one run's saved validation predictions. [Confidence sweep](validation-confidence-audit.csv) · [COCO at 0.001](full-validation-low-confidence-coco.json)

The official plugin generated a [prediction CSV](submission.csv) at confidence 0.0001. It has 715 rows and 162,875 detections, and passed all five format checks. Kaggle scored the participant submission **0.62775 public AP50** on November 21, 2026 Pacific time, below C01 and L02. [Prediction provenance](provenance.json) · [Kaggle score evidence](kaggle-score.jpg)
