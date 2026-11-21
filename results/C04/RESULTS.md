# C04 results

C04 repeated C01 with seed 1 in place of seed 0. It retained CutMix at 0.10, E01 training labels, the original validation table, and the saved-prediction confidence cutoff of 0.10. The plugin completed 30 epochs in 229.59 minutes and selected epoch 29. All four model provenance checks passed. [Settings](../../configs/C04-experiment.json) · [Provenance](provenance.json)

| Selected-checkpoint validation | E01 | C01 | L02 | C04 |
| --- | ---: | ---: | ---: | ---: |
| mAP@0.5 | 0.696076 | 0.704608 | 0.706529 | 0.693492 |
| mAP@0.5:0.95 | 0.444086 | 0.450919 | 0.453166 | 0.444268 |
| Chair AP50 | 0.573601 | 0.570571 | 0.575191 | 0.553479 |
| Table AP50 | 0.560161 | 0.573478 | 0.574721 | 0.545080 |
| Precision | 0.757583 | 0.794588 | 0.762563 | 0.737642 |
| Recall | 0.599035 | 0.607953 | 0.619262 | 0.605913 |

All four runs evaluated the same 733 images and 2,725 ground-truth boxes. C04 trailed C01 and L02 on native AP50 and AP50–95. C04 was below E01 on native AP50 and marginally above it on AP50–95. The live AP50 and AP50–95 metrics peaked at epoch 29 (0.69344 and 0.44452). [Per-class metrics](final-validation-per-class.csv) · [Epoch metrics](epoch-results.csv) · [Native curves](training-curves.png)

| Paired COCO AP50 | E01 | C01 | L02 | C04 |
| --- | ---: | ---: | ---: | ---: |
| 293-image common holdout | 0.624649 | 0.631170 | 0.627379 | 0.619253 |
| Full original validation, 733 images | 0.651052 | 0.656948 | 0.655979 | 0.647474 |

C04 trailed all three references on both matched COCO cohorts at saved confidence ≥ 0.10 and maxDets 100. The 293-image cohort is a subset of the full validation set used to select all four checkpoints. The single seed change shows that C01's lead did not reproduce under seed 1. [Common holdout](common-holdout-scores.json) · [Full validation COCO](full-validation-coco-scores.json)

| Same-class matches at IoU ≥ 0.50 | Ground truth | C01 | C04 |
| --- | ---: | ---: | ---: |
| Under 32 px | 302 | 99 | 103 |
| 32 to under 96 px | 1002 | 679 | 689 |
| 96 px and larger | 1421 | 1171 | 1154 |

[Size audit](validation-size-audit.csv)

C04 had no official test prediction or Kaggle submission.
