# E04 results

E04 added two participant-reviewed Table boxes to E03's training annotations and retained E03's 30-epoch settings and original validation table. The native plugin finished in 230.81 minutes and selected epoch 28. All four model provenance checks passed. [Settings](../../configs/E04-experiment.json) · [Provenance](provenance.json)

| Selected-checkpoint validation | E03 | E01 | E04 | Δ vs E03 | Δ vs E01 |
| --- | ---: | ---: | ---: | ---: | ---: |
| mAP@0.5 | 0.695916 | 0.696076 | 0.690343 | −0.005573 | −0.005733 |
| mAP@0.5:0.95 | 0.443849 | 0.444086 | 0.440268 | −0.003580 | −0.003818 |
| Chair AP50 | 0.541800 | 0.573601 | 0.567427 | +0.025627 | −0.006173 |
| Table AP50 | 0.582711 | 0.560161 | 0.542802 | −0.039908 | −0.017359 |
| Precision | 0.743275 | 0.757583 | 0.737624 | −0.005651 | −0.019959 |
| Recall | 0.623651 | 0.599035 | 0.614158 | −0.009493 | +0.015123 |

All three runs evaluated the same 733 images and 2,725 ground-truth boxes. The size audit uses confidence 0.10 and IoU 0.50. [Per-class metrics](final-validation-per-class.csv) · [Size audit](validation-size-audit.csv)

| Size | Ground truth | E03 matches | E01 matches | E04 matches |
| --- | ---: | ---: | ---: | ---: |
| Small | 302 | 105 | 94 | 105 |
| Medium | 1,002 | 683 | 690 | 694 |
| Large | 1,421 | 1,156 | 1,171 | 1,160 |

In the training history, mAP@0.5 peaked at 0.69156 in epoch 30, and mAP@0.5:0.95 peaked at 0.44011 in epoch 28. [Epoch metrics](epoch-results.csv) · [Native curves](training-curves.png)

No Kaggle prediction or submission was made.
