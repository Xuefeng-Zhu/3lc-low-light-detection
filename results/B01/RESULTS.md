# B01 results

B01 used E01's participant-reviewed labels, original validation table, and 30-epoch settings. The box regression loss gain increased from 7.5 to 9.0. The native plugin finished in 229.11 minutes and selected epoch 29. All four model provenance checks passed. [Settings](../../configs/B01-experiment.json) · [Provenance](provenance.json)

| Selected-checkpoint validation | E01 | B01 | Change |
| --- | ---: | ---: | ---: |
| mAP@0.5 | 0.696076 | 0.692545 | −0.003531 |
| mAP@0.5:0.95 | 0.444086 | 0.443667 | −0.000419 |
| Chair AP50 | 0.573601 | 0.554676 | −0.018925 |
| Table AP50 | 0.560161 | 0.567742 | +0.007581 |
| Precision | 0.757583 | 0.752545 | −0.005038 |
| Recall | 0.599035 | 0.603628 | +0.004593 |

Both runs evaluated the same 733 images and 2,725 ground-truth boxes. At confidence 0.10 and IoU 0.50, matches went from 94 to 102 of 302 small boxes, 690 to 687 of 1,002 medium boxes, and 1,171 to 1,151 of 1,421 large boxes. [Per-class metrics](final-validation-per-class.csv) · [Size audit](validation-size-audit.csv)

In the training history, mAP@0.5 peaked at 0.69352 in epoch 30, and mAP@0.5:0.95 peaked at 0.44350 in epoch 29. [Epoch metrics](epoch-results.csv) · [Native curves](training-curves.png)

On the matched 293-image COCO holdout, B01 reached **0.605253 AP50** versus **0.624649** for E01 (-0.019397), using saved predictions with confidence ≥0.10 and maxDets 100. Both checkpoints were selected on the full original validation set, which includes the common holdout. [B01 holdout scores](common-holdout-scores.json) · [E01 reference scores](../R01/reference-scores.json)

At confidence 0.10 and IoU 0.75, B01 matched 44 small, 431 medium, and 941 large boxes. E01 matched 40 small, 411 medium, and 950 large boxes. [IoU 0.75 audit](validation-size-iou75-comparison.csv)

No Kaggle prediction or submission was made.
