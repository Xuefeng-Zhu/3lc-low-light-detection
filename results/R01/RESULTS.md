# R01 results

R01 replaced 440 unreviewed E04 training images without a supplied small box with 440 images from the original validation split. It kept all 19 reviewed training images and all 549 original training images containing small boxes. The 293 remaining original-validation images formed the disjoint holdout. The native plugin finished in 220.31 minutes and selected epoch 30. All four model provenance checks passed. [Split manifest](split-manifest.json) · [Settings](../../configs/R01-experiment.json) · [Provenance](provenance.json)

## Matched COCO holdout

All runs were scored from saved predictions on the same 293 images and 1,207 supplied boxes, using confidence ≥0.10 and COCO maxDets 100. Earlier checkpoints used the 733-image original validation split for selection, including these 293 images. R01 used this holdout directly. [Common holdout scores](common-holdout-scores.json) · [Preserved reference scores](reference-scores.json)

| Run | COCO AP50 | Chair AP50 | Table AP50 |
| --- | ---: | ---: | ---: |
| E01 | 0.624649 | 0.539349 | 0.530018 |
| W03 | 0.616526 | 0.499487 | 0.501300 |
| E03 | 0.621273 | 0.494753 | 0.543757 |
| E04 | 0.614679 | 0.541559 | 0.510382 |
| R01 | 0.622201 | 0.521014 | 0.504881 |

R01 changed COCO AP50 by +0.007522 compared with E04 and −0.002449 compared with E01.

## Native 3LC validation

The selected checkpoint reached **0.676654 AP50** and **0.427170 AP50–95** on R01's 293-image holdout. These values use the native validator. Earlier native results were measured on all 733 original validation images. The fixed-threshold size audit uses confidence 0.10 and IoU 0.50. [Per-class metrics](final-validation-per-class.csv) · [Size audit](common-holdout-size-audit.csv)

| Size | Ground truth | E04 matches | E01 matches | W03 matches | R01 matches |
| --- | ---: | ---: | ---: | ---: | ---: |
| Small | 123 | 40 | 42 | 42 | 43 |
| Medium | 462 | 311 | 307 | 304 | 304 |
| Large | 622 | 496 | 500 | 488 | 493 |

In the training history, AP50 peaked at 0.67744 in epoch 29. AP50–95 peaked at 0.42682 in epoch 30. [Epoch metrics](epoch-results.csv) · [Native curves](training-curves.png)

The official plugin exported the selected checkpoint's predictions at confidence 0.001. The CSV contains 715 rows and 49,462 predicted boxes and passed all five format checks. [Official CSV](submission.csv)

## Kaggle public score

R01 scored **0.61772**, 1.96 percentage points below E01's **0.63733**. On the shared validation images, R01 matched one more small object, three fewer medium objects, and seven fewer large objects than E01. Its largest per-class AP50 declines were Motorbike (−3.47 points), Dog (−3.32), Bottle (−3.00), and Table (−2.51). Kaggle publishes the aggregate score, so class-level causes of the public decrease remain unknown. [Official score](kaggle-score.jpg) · [Matched validation scores](common-holdout-scores.json)
