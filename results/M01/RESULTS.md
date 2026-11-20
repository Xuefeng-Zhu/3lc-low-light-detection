# M01 results

M01 used E01's participant-reviewed labels, original validation table, and 30-epoch settings. The mosaic probability decreased from 1.0 to 0.5 for the first 20 epochs. Mosaic was off for the final 10 epochs in both runs. The native plugin finished in 226.65 minutes and selected epoch 28. All four model provenance checks passed. [Settings](../../configs/M01-experiment.json) · [Provenance](provenance.json)

| Selected-checkpoint validation | E01 | M01 | Change |
| --- | ---: | ---: | ---: |
| mAP@0.5 | 0.696076 | 0.693846 | −0.002230 |
| mAP@0.5:0.95 | 0.444086 | 0.442931 | −0.001155 |
| Chair AP50 | 0.573601 | 0.557009 | −0.016591 |
| Table AP50 | 0.560161 | 0.554916 | −0.005245 |
| Precision | 0.757583 | 0.733047 | −0.024536 |
| Recall | 0.599035 | 0.612105 | +0.013070 |

Both runs evaluated the same 733 images and 2,725 ground-truth boxes. At confidence 0.10 and IoU 0.50, matches went from 94 to 101 of 302 small boxes, 690 to 688 of 1,002 medium boxes, and 1,171 to 1,160 of 1,421 large boxes. [Per-class metrics](final-validation-per-class.csv) · [Size audit](validation-size-audit.csv)

In the training history, mAP@0.5 peaked at 0.69399 in epoch 28, and mAP@0.5:0.95 peaked at 0.44305 in epoch 28. [Epoch metrics](epoch-results.csv) · [Native curves](training-curves.png)

On the matched 293-image COCO holdout, M01 reached **0.614276 AP50** versus **0.624649** for E01, a decrease of 0.010374, using saved predictions with confidence ≥0.10 and maxDets 100. Both checkpoints were selected on the full original validation set, which includes the common holdout. [M01 holdout scores](common-holdout-scores.json) · [E01 reference scores](../R01/reference-scores.json)

No Kaggle prediction or submission was made.
