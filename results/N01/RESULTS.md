# N01 results

N01 reduced the nominal batch size setting from 64 to 32 while keeping the actual batch at 8, CutMix probability at 0.10, the E01 training labels, and the original validation table. The plugin completed 30 epochs in 234.32 minutes and selected epoch 27. All four model provenance checks passed. [Settings](../../configs/N01-experiment.json) · [Provenance](provenance.json)

| Selected-checkpoint validation | E01 | C01 | N01 | N01 change vs. C01 |
| --- | ---: | ---: | ---: | ---: |
| mAP@0.5 | 0.696076 | 0.704608 | 0.685669 | -0.018939 |
| mAP@0.5:0.95 | 0.444086 | 0.450919 | 0.436557 | -0.014361 |
| Chair AP50 | 0.573601 | 0.570571 | 0.556742 | -0.013829 |
| Table AP50 | 0.560161 | 0.573478 | 0.549429 | -0.024049 |
| Precision | 0.757583 | 0.794588 | 0.765407 | -0.029181 |
| Recall | 0.599035 | 0.607953 | 0.592285 | -0.015668 |

All three runs evaluated 733 images and 2,725 ground-truth boxes. N01 fell below both references on aggregate native AP. Training AP50 peaked at 0.68659 in epoch 30, while AP50–95 peaked at 0.43653 in epoch 27. [Per-class metrics](final-validation-per-class.csv) · [Epoch metrics](epoch-results.csv) · [Native curves](training-curves.png)

| Paired COCO AP50 | E01 | C01 | N01 |
| --- | ---: | ---: | ---: |
| 293-image common holdout | 0.624649 | 0.631170 | 0.618954 |
| Full original validation, 733 images | 0.651052 | 0.656948 | 0.639329 |

N01 also trailed both references on Chair and Table COCO AP50 in both cohorts. The evaluator used saved predictions with confidence ≥ 0.10 and maxDets 100. The 293-image holdout is a subset of the original validation set used to select all three checkpoints. [Common holdout](common-holdout-scores.json) · [Full validation COCO](full-validation-coco-scores.json)

Within N01, lowering the analysis cutoff from 0.10 to 0.001 increased correct small-object matches at IoU ≥ 0.50 from 105 to 219 of 302 and all-size matches from 1,942 to 2,519 of 2,725. Valid detections rose from 4,200 to 65,371. The audit recorded 121 clipped zero-area detections at 0.001, none at 0.10, and 44 saved rows at the detection cap. [Confidence sweep](validation-confidence-audit.csv)

N01 had no official test prediction or Kaggle submission.
