# W02 results

W02 started from the pinned official YOLOv11n checkpoint and used the same weighted revision as W01. It completed a 50-epoch cosine schedule in 387.55 minutes, with mosaic active for the first 20 epochs. All four native provenance checks passed. [Configuration](../../configs/W02-experiment.json) · [Provenance](provenance.json)

| Final checkpoint validation | W01 | W02 | Change |
| --- | ---: | ---: | ---: |
| mAP@0.5 | 0.696537 | 0.692656 | −0.003881 |
| mAP@0.5:0.95 | 0.444703 | 0.439867 | −0.004836 |
| Precision | 0.776315 | 0.766581 | −0.009734 |
| Recall | 0.607841 | 0.598641 | −0.009200 |

Both checkpoints were evaluated against the same 733 validation images and 2,725 ground-truth boxes. W02's epoch-history AP50 peaked at 0.69329 in epoch 45. AP50–95 peaked in epoch 50, which selected the saved checkpoint. The largest class AP50 decline was Table, down 4.26 percentage points. [Per-class metrics](final-validation-per-class.csv) · [Epoch history](epoch-results.csv) · [Training curves](training-curves.png)

At confidence 0.10 and IoU 0.50, small-object matches increased from 97 to 103 of 302. Medium-object matches fell from 694 to 672 of 1,002 and large-object matches fell from 1,172 to 1,148 of 1,421. W01 remains the submission candidate with the highest measured validation AP50 and the verified Kaggle public score of 0.63189. [Size audit](validation-size-audit.csv) · [W01 submission record](../W01/RESULTS.md)
