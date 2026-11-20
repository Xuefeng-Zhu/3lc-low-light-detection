# D01 results

D01 increased the classification loss weight from 0.50 in C01 to 0.65. It retained C01's CutMix probability of 0.10, the E01 training labels, and the original validation table. The plugin completed all 30 epochs in 231.77 minutes and selected epoch 29. All four model provenance checks passed. [Settings](../../configs/D01-experiment.json) · [Provenance](provenance.json)

| Selected-checkpoint validation | E01 | C01 | D01 | D01 change vs. C01 |
| --- | ---: | ---: | ---: | ---: |
| mAP@0.5 | 0.696076 | 0.704608 | 0.696100 | -0.008508 |
| mAP@0.5:0.95 | 0.444086 | 0.450919 | 0.444525 | -0.006393 |
| Chair AP50 | 0.573601 | 0.570571 | 0.550435 | -0.020136 |
| Table AP50 | 0.560161 | 0.573478 | 0.548176 | -0.025302 |
| Precision | 0.757583 | 0.794588 | 0.767215 | -0.027373 |
| Recall | 0.599035 | 0.607953 | 0.614646 | +0.006692 |

All three runs evaluated the same 733 images and 2,725 ground-truth boxes. D01 came close to E01 on native AP and fell below C01 on both AP measures. Training AP50 and AP50–95 peaked at 0.69557 and 0.44416, respectively, at epoch 29. [Per-class metrics](final-validation-per-class.csv) · [Epoch metrics](epoch-results.csv) · [Native curves](training-curves.png)

| Paired COCO AP50 | E01 | C01 | D01 |
| --- | ---: | ---: | ---: |
| 293-image common holdout | 0.624649 | 0.631170 | 0.616498 |
| Full original validation, 733 images | 0.651052 | 0.656948 | 0.647282 |

D01 trailed both references on aggregate, Chair, and Table COCO AP50 in both cohorts. The evaluator used saved predictions with confidence ≥ 0.10 and maxDets 100. The 293 images were included in the original validation set used to select all three checkpoints. [Common holdout](common-holdout-scores.json) · [Full validation COCO](full-validation-coco-scores.json)

Within D01, lowering the saved-prediction cutoff from 0.10 to 0.001 increased correct small-object matches at IoU ≥ 0.50 from 102 to 215 of 302. Correct matches across all sizes rose from 1,945 to 2,522 of 2,725, while valid detections increased from 4,113 to 57,751. The audit recorded 266 clipped zero-area predictions at 0.001, none at 0.10, and 28 saved rows at the detection cap. [Confidence sweep](validation-confidence-audit.csv)

D01 had no official test prediction or Kaggle submission.
