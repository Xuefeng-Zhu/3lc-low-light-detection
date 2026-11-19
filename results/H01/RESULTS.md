# H01 results

H01 used E01's participant-reviewed labels, original validation table, and 30-epoch settings. The augmentation change reduced the HSV value gain from 0.40 to 0.20. The native plugin finished in 229.29 minutes and selected epoch 28. All four model provenance checks passed. [Settings](../../configs/H01-experiment.json) · [Provenance](provenance.json)

| Selected-checkpoint validation | E01 | H01 | Change |
| --- | ---: | ---: | ---: |
| mAP@0.5 | 0.696076 | 0.691531 | −0.004545 |
| mAP@0.5:0.95 | 0.444086 | 0.443270 | −0.000816 |
| Chair AP50 | 0.573601 | 0.553584 | −0.020016 |
| Table AP50 | 0.560161 | 0.528076 | −0.032086 |
| Precision | 0.757583 | 0.708421 | −0.049162 |
| Recall | 0.599035 | 0.629860 | +0.030825 |

Both runs evaluated the same 733 images and 2,725 ground-truth boxes. At confidence 0.10 and IoU 0.50, matches went from 94 to 91 of 302 small boxes, 690 to 688 of 1,002 medium boxes, and 1,171 to 1,163 of 1,421 large boxes. [Per-class metrics](final-validation-per-class.csv) · [Size audit](validation-size-audit.csv)

In the training history, mAP@0.5 peaked at 0.69160 in epoch 28, and mAP@0.5:0.95 peaked at 0.44326 in epoch 28. [Epoch metrics](epoch-results.csv) · [Native curves](training-curves.png)

No Kaggle prediction or submission was made.
