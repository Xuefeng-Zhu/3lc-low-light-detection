# C01 results

C01 used E01's participant-reviewed labels, original validation table, and 30-epoch settings. CutMix probability increased from 0 to 0.10 for the first 20 epochs. CutMix was off for the final 10 epochs. The native plugin finished in 235.67 minutes and selected epoch 28. All four model provenance checks passed. [Settings](../../configs/C01-experiment.json) · [Provenance](provenance.json)

| Selected-checkpoint validation | E01 | C01 | Change |
| --- | ---: | ---: | ---: |
| mAP@0.5 | 0.696076 | 0.704608 | +0.008533 |
| mAP@0.5:0.95 | 0.444086 | 0.450919 | +0.006832 |
| Chair AP50 | 0.573601 | 0.570571 | −0.003029 |
| Table AP50 | 0.560161 | 0.573478 | +0.013316 |
| Precision | 0.757583 | 0.794588 | +0.037005 |
| Recall | 0.599035 | 0.607953 | +0.008918 |

Both runs evaluated the same 733 images and 2,725 ground-truth boxes. At confidence 0.10 and IoU 0.50, matches went from 94 to 99 of 302 small boxes, 690 to 679 of 1,002 medium boxes, and 1,171 to 1,171 of 1,421 large boxes. [Per-class metrics](final-validation-per-class.csv) · [Size audit](validation-size-audit.csv)

In the training history, mAP@0.5 peaked at 0.70462 in epoch 28, and mAP@0.5:0.95 peaked at 0.45066 in epoch 28. [Epoch metrics](epoch-results.csv) · [Native curves](training-curves.png)

On the matched 293-image COCO holdout, C01 reached **0.631170 AP50** versus **0.624649** for E01, an increase of 0.006520, using saved predictions with confidence ≥0.10 and maxDets 100. Both checkpoints were selected on the full original validation set, which includes the common holdout. [C01 holdout scores](common-holdout-scores.json) · [E01 reference scores](../R01/reference-scores.json)

On all 733 original validation images, COCO AP50 rose from 0.651052 to 0.656948. [Full validation COCO scores](full-validation-coco-scores.json)

The official plugin exported [submission.csv](submission.csv) at confidence 0.0001. It contains 715 rows and 159,923 predicted boxes. All five native format checks passed. The submission file is ready. Participant submission is pending the daily quota reset.
