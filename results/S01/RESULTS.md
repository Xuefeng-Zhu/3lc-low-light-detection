# S01 results

S01 used E01's participant-reviewed labels, original validation table, and 30-epoch settings. The augmentation change reduced random affine scale from 0.50 to 0.20. The native plugin finished in 240.90 minutes and selected epoch 27. All four model provenance checks passed. [Settings](../../configs/S01-experiment.json) · [Provenance](provenance.json)

| Selected-checkpoint validation | E01 | S01 | Change |
| --- | ---: | ---: | ---: |
| mAP@0.5 | 0.696076 | 0.683487 | −0.012589 |
| mAP@0.5:0.95 | 0.444086 | 0.430991 | −0.013095 |
| Chair AP50 | 0.573601 | 0.547113 | −0.026487 |
| Table AP50 | 0.560161 | 0.528333 | −0.031829 |
| Precision | 0.757583 | 0.733660 | −0.023923 |
| Recall | 0.599035 | 0.611011 | +0.011975 |

Both runs evaluated the same 733 images and 2,725 ground-truth boxes. At confidence 0.10 and IoU 0.50, matches went from 94 to 103 of 302 small boxes, 690 to 659 of 1,002 medium boxes, and 1171 to 1149 of 1,421 large boxes. [Per-class metrics](final-validation-per-class.csv) · [Size audit](validation-size-audit.csv)

Epoch 27 reached 0.68345 mAP@0.5 and 0.43086 mAP@0.5:0.95 in the training history. [Epoch metrics](epoch-results.csv) · [Native curves](training-curves.png)

S01 stayed below E01 on both aggregate validation AP measures. No Kaggle prediction or submission was made.
