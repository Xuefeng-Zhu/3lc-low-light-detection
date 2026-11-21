# L02 results

L02 lowered the initial learning rate from 0.000625 in C01 to 0.00045 and retained CutMix at 0.10. It used the E01 training labels and original validation table. The plugin completed 30 epochs in 232.45 minutes and selected epoch 30. All four model provenance checks passed. [Settings](../../configs/L02-experiment.json) · [Provenance](provenance.json)

| Selected-checkpoint validation | E01 | L01 | C01 | L02 |
| --- | ---: | ---: | ---: | ---: |
| mAP@0.5 | 0.696076 | 0.698857 | 0.704608 | 0.706529 |
| mAP@0.5:0.95 | 0.444086 | 0.449118 | 0.450919 | 0.453166 |
| Chair AP50 | 0.573601 | 0.548041 | 0.570571 | 0.575191 |
| Table AP50 | 0.560161 | 0.572110 | 0.573478 | 0.574721 |
| Precision | 0.757583 | 0.774508 | 0.794588 | 0.762563 |
| Recall | 0.599035 | 0.605394 | 0.607953 | 0.619262 |

All four runs evaluated the same 733 images and 2,725 ground-truth boxes. L02 led on both native AP measures. Training AP50 peaked at 0.70745 in epoch 29 and AP50–95 peaked at 0.45303 in epoch 30. [Per-class metrics](final-validation-per-class.csv) · [Epoch metrics](epoch-results.csv) · [Native curves](training-curves.png)

| Paired COCO AP50 | E01 | L01 | C01 | L02 |
| --- | ---: | ---: | ---: | ---: |
| 293-image common holdout | 0.624649 | 0.618771 | 0.631170 | 0.627379 |
| Full original validation, 733 images | 0.651052 | 0.655107 | 0.656948 | 0.655979 |

C01 led both paired COCO cohorts at saved confidence ≥ 0.10 and maxDets 100. L02 beat E01 and L01 on both. The 293-image cohort is a subset of the full validation set used to select all four checkpoints. [Common holdout](common-holdout-scores.json) · [Full validation COCO](full-validation-coco-scores.json)

Lowering L02's analysis cutoff from 0.10 to 0.001 increased correct small-object matches at IoU ≥ 0.50 from 98 to 217 of 302. Across all sizes, correct matches rose from 1,956 to 2,510 of 2,725, and valid detections rose from 4,122 to 60,699. The audit recorded 143 clipped zero-area predictions at 0.001, none at 0.10, and 39 saved rows at the detection cap. [Confidence sweep](validation-confidence-audit.csv)

The official plugin exported 715 test rows and 184,830 boxes at confidence 0.0001. All five format checks passed. The validated file is attached on Kaggle with the Submit button enabled. Participant submission is pending. [Submission CSV](submission.csv) · [Prediction provenance](provenance.json)
