# C02 results

C02 increased CutMix probability from 0.10 in C01 to 0.20 for the first 20 epochs, using the same E01 training labels and original validation table. Both runs switched off CutMix for the final 10 epochs. The native plugin finished in 235.13 minutes and selected epoch 30. All four model provenance checks passed. [Settings](../../configs/C02-experiment.json) · [Provenance](provenance.json)

| Selected-checkpoint validation | E01 | C02 | Change |
| --- | ---: | ---: | ---: |
| mAP@0.5 | 0.696076 | 0.695730 | −0.000346 |
| mAP@0.5:0.95 | 0.444086 | 0.441346 | −0.002740 |
| Chair AP50 | 0.573601 | 0.551771 | −0.021830 |
| Table AP50 | 0.560161 | 0.528589 | −0.031573 |
| Precision | 0.757583 | 0.749668 | −0.007915 |
| Recall | 0.599035 | 0.620385 | +0.021349 |

Both runs evaluated the same 733 images and 2,725 ground-truth boxes. [Per-class metrics](final-validation-per-class.csv)

In the training history, mAP@0.5 peaked at 0.69537 in epoch 30, and mAP@0.5:0.95 peaked at 0.44145 in epoch 30. [Epoch metrics](epoch-results.csv) · [Native curves](training-curves.png)

On the matched 293-image COCO holdout, C02 reached **0.616634 AP50** versus **0.624649** for E01, a decrease of 0.008015, using saved predictions with confidence ≥0.10 and maxDets 100. Both checkpoints were selected on the full original validation set, which includes the common holdout. [C02 holdout scores](common-holdout-scores.json) · [E01 reference scores](../R01/reference-scores.json)

On all 733 original validation images, COCO AP50 fell from 0.651052 to 0.650345. [Full validation COCO scores](full-validation-coco-scores.json)

C01 scored 0.631170 on the same holdout and 0.656948 on full validation. Its native AP50 was 0.704608 and AP50–95 was 0.450919.

Within C02's saved validation predictions, lowering the analysis cutoff from 0.10 to 0.001 raised same-class matches at IoU 0.50 from 107 to 224 for small boxes and from 1,949 to 2,511 across all sizes. The raw lower-cutoff list includes 37 zero-area detections, which cannot match a supplied box. [Confidence sweep](validation-confidence-audit.csv)

No official test prediction or Kaggle submission was made.
