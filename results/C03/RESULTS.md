# C03 results

C03 reduced CutMix probability from 0.10 in C01 to 0.05, using the same E01 labels and original validation table. The plugin completed 30 epochs in 233.06 minutes and selected epoch 29. All four model provenance checks passed. [Settings](../../configs/C03-experiment.json) · [Provenance](provenance.json)

| Selected-checkpoint validation | E01 | C03 | C01 | C02 |
| --- | ---: | ---: | ---: | ---: |
| mAP@0.5 | 0.696076 | 0.695148 | 0.704608 | 0.695730 |
| mAP@0.5:0.95 | 0.444086 | 0.442003 | 0.450919 | 0.441346 |
| Chair AP50 | 0.573601 | 0.539201 | 0.570571 | 0.551771 |
| Table AP50 | 0.560161 | 0.565871 | 0.573478 | 0.528589 |
| Precision | 0.757583 | 0.748491 | 0.794588 | 0.749668 |
| Recall | 0.599035 | 0.622813 | 0.607953 | 0.620385 |

All four runs evaluated 733 images and 2,725 ground-truth boxes. C03 trailed E01 and C01 on native AP50 and AP50–95. Compared with C02 at CutMix 0.20, C03 had slightly lower AP50 and higher AP50–95. Both live training AP metrics peaked at epoch 29 (0.69503 AP50 and 0.44190 AP50–95). [Per-class metrics](final-validation-per-class.csv) · [Epoch metrics](epoch-results.csv) · [Native curves](training-curves.png)

| Paired COCO AP50 | E01 | C03 | C01 | C02 |
| --- | ---: | ---: | ---: | ---: |
| 293-image common holdout | 0.624649 | 0.616515 | 0.631170 | 0.616634 |
| Full original validation, 733 images | 0.651052 | 0.648221 | 0.656948 | 0.650345 |

At saved confidence ≥ 0.10 and maxDets 100, C01 at CutMix 0.10 led on both cohorts. C03's COCO AP50 was below E01 and C02 on both. The 293-image holdout is a subset of the original validation set used to select all four checkpoints. [Common holdout](common-holdout-scores.json) · [Full validation COCO](full-validation-coco-scores.json)

Lowering C03's analysis cutoff from 0.10 to 0.001 increased correct small-object matches at IoU ≥ 0.50 from 97 to 219 of 302 and all-size matches from 1,947 to 2,517 of 2,725. Valid detections rose from 4,078 to 60,510. The audit recorded 42 clipped zero-area predictions at 0.001, none at 0.10, and 31 saved rows at the detection cap. [Confidence sweep](validation-confidence-audit.csv)

C03 had no official test prediction or Kaggle submission.
