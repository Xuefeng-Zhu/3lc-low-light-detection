# W04 results

W04 retained W03's 30-epoch settings and original validation table. Its weight-only child revision multiplied the sampling weights by 1.25 for 549 training images with at least one supplied box whose equivalent square side is strictly under 32 pixels after fitting the image to 640 pixels. The native plugin finished in 234.10 minutes and selected epoch 29. All four model provenance checks passed. [Settings](../../configs/W04-experiment.json) · [Provenance](provenance.json)

| Selected-checkpoint validation | W03 | E01 | W04 | Δ vs W03 | Δ vs E01 |
| --- | ---: | ---: | ---: | ---: | ---: |
| mAP@0.5 | 0.699040 | 0.696076 | 0.688968 | −0.010072 | −0.007108 |
| mAP@0.5:0.95 | 0.440814 | 0.444086 | 0.439822 | −0.000992 | −0.004264 |
| Chair AP50 | 0.567472 | 0.573601 | 0.544613 | −0.022859 | −0.028988 |
| Table AP50 | 0.587240 | 0.560161 | 0.557182 | −0.030058 | −0.002979 |
| Precision | 0.741111 | 0.757583 | 0.740040 | −0.001070 | −0.017543 |
| Recall | 0.622905 | 0.599035 | 0.616379 | −0.006526 | +0.017344 |

All three runs evaluated the same 733 images and 2,725 ground-truth boxes. The size audit uses confidence 0.10 and IoU 0.50. [Per-class metrics](final-validation-per-class.csv) · [Size audit](validation-size-audit.csv)

| Size | Ground truth | W03 matches | E01 matches | W04 matches |
| --- | ---: | ---: | ---: | ---: |
| Small | 302 | 102 | 94 | 107 |
| Medium | 1,002 | 689 | 690 | 667 |
| Large | 1,421 | 1,160 | 1,171 | 1,163 |

In the training history, mAP@0.5 peaked at 0.69152 in epoch 26, and mAP@0.5:0.95 peaked at 0.43973 in epoch 29. [Epoch metrics](epoch-results.csv) · [Native curves](training-curves.png)

No Kaggle prediction or submission was made.
