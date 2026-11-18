# W03 results

W03 tested Chair/Table sampling weights on the participant-reviewed E01 training labels. It used weight 1.5 for 1,299 rows and weight 1.0 for 4,611 rows, with E01's 30-epoch settings and the original validation table. The native plugin finished in 226.34 minutes and selected epoch 30. All four model provenance checks passed. [Revision audit and settings](../../configs/W03-experiment.json) · [Provenance](provenance.json)

| Selected-checkpoint validation | E01 | W01 | W03 | Δ vs E01 | Δ vs W01 |
| --- | ---: | ---: | ---: | ---: | ---: |
| mAP@0.5 | 0.696076 | 0.696537 | 0.699040 | +0.002964 | +0.002503 |
| mAP@0.5:0.95 | 0.444086 | 0.444703 | 0.440814 | -0.003272 | -0.003889 |
| Chair AP50 | 0.573601 | 0.568895 | 0.567472 | -0.006129 | -0.001423 |
| Table AP50 | 0.560161 | 0.580744 | 0.587240 | +0.027079 | +0.006496 |
| Precision | 0.757583 | 0.776315 | 0.741111 | -0.016472 | -0.035204 |
| Recall | 0.599035 | 0.607841 | 0.622905 | +0.023870 | +0.015064 |

All three runs evaluated the same 733 validation images and 2,725 boxes. At confidence 0.10 and IoU 0.50, W03 matched 102 of 302 small boxes, compared with 94 for E01 and 97 for W01. Medium matches were 689 of 1,002 for W03, 690 for E01, and 694 for W01. Large matches were 1,160 of 1,421 for W03, 1,171 for E01, and 1,172 for W01. [Per-class metrics](final-validation-per-class.csv) · [Size audit](validation-size-audit.csv)

Epoch 30 reached 0.69940 mAP@0.5 and 0.44097 mAP@0.5:0.95 in the training history. [Epoch metrics](epoch-results.csv) · [Native curves](training-curves.png)

The official plugin exported [submission.csv](submission.csv) at confidence 0.001. It contains 715 rows and 49,418 predicted boxes and passed all five format checks. Kaggle scoring is pending participant submission. The daily submission quota was unavailable until 4:00 p.m. PST on November 18, 2026.
