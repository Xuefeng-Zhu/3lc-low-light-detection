# E03 results

E03 used a child of E01's training table with three participant-reviewed Chair box geometry edits. E03 retained E01's 30-epoch settings and original validation table. The native plugin finished in 232.34 minutes and selected epoch 30. All four model provenance checks passed. [Settings](../../configs/E03-experiment.json) · [Provenance](provenance.json)

| Selected-checkpoint validation | E01 | E03 | Change |
| --- | ---: | ---: | ---: |
| mAP@0.5 | 0.696076 | 0.695916 | −0.000160 |
| mAP@0.5:0.95 | 0.444086 | 0.443849 | −0.000237 |
| Chair AP50 | 0.573601 | 0.541800 | −0.031800 |
| Table AP50 | 0.560161 | 0.582711 | +0.022549 |
| Precision | 0.757583 | 0.743275 | −0.014308 |
| Recall | 0.599035 | 0.623651 | +0.024616 |

Both runs evaluated the same 733 images and 2,725 ground-truth boxes. At confidence 0.10 and IoU 0.50, matches went from 94 to 105 of 302 small boxes, 690 to 683 of 1,002 medium boxes, and 1,171 to 1,156 of 1,421 large boxes. [Per-class metrics](final-validation-per-class.csv) · [Size audit](validation-size-audit.csv)

In the training history, mAP@0.5 peaked at 0.69701 in epoch 27, and mAP@0.5:0.95 peaked at 0.44457 in epoch 30. [Epoch metrics](epoch-results.csv) · [Native curves](training-curves.png)

No Kaggle prediction or submission was made.
