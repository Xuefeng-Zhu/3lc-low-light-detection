# L01 results

L01 used E01's participant-reviewed labels, original validation table, and 30-epoch settings. The initial AdamW learning rate decreased from 0.000625 to 0.00045. The native plugin finished in 229.72 minutes and selected epoch 27. All four model provenance checks passed. [Settings](../../configs/L01-experiment.json) · [Provenance](provenance.json)

| Selected-checkpoint validation | E01 | L01 | Change |
| --- | ---: | ---: | ---: |
| mAP@0.5 | 0.696076 | 0.698857 | +0.002781 |
| mAP@0.5:0.95 | 0.444086 | 0.449118 | +0.005031 |
| Chair AP50 | 0.573601 | 0.548041 | −0.025560 |
| Table AP50 | 0.560161 | 0.572110 | +0.011949 |
| Precision | 0.757583 | 0.774508 | +0.016925 |
| Recall | 0.599035 | 0.605394 | +0.006359 |

Both runs evaluated the same 733 images and 2,725 ground-truth boxes. At confidence 0.10 and IoU 0.50, matches went from 94 to 96 of 302 small boxes, 690 to 692 of 1,002 medium boxes, and 1,171 to 1,156 of 1,421 large boxes. [Per-class metrics](final-validation-per-class.csv) · [Size audit](validation-size-audit.csv)

In the training history, mAP@0.5 peaked at 0.70203 in epoch 30, and mAP@0.5:0.95 peaked at 0.44918 in epoch 27. [Epoch metrics](epoch-results.csv) · [Native curves](training-curves.png)

On the matched 293-image COCO holdout, L01 reached **0.618771 AP50** versus **0.624649** for E01, a decrease of 0.005879, using saved predictions with confidence ≥0.10 and maxDets 100. Both checkpoints were selected on the full original validation set, which includes the common holdout. [L01 holdout scores](common-holdout-scores.json) · [E01 reference scores](../R01/reference-scores.json)

On all 733 original validation images, COCO AP50 rose from 0.651052 to 0.655107. On the other 440 images, it rose from 0.671228 to 0.682150. [COCO cohort scores](cohort-scores.json)

The official plugin exported at confidence 0.001. The file contains 715 rows and 48,542 predicted boxes and passed all five format checks. The participant submitted on November 19, 2026. Kaggle returned **0.63453** public AP50, 0.28 percentage points below E01 at the same inference threshold. [Official CSV](submission.csv) · [Kaggle score](kaggle-score.jpg)
