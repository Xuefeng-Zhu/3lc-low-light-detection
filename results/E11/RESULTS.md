# E11 results

E11 completed 30 epochs with batch 8 on an NVIDIA T500 using the original training and validation tables. The official 3LC plugin v1.2.15 recorded all four provenance checks for the COCO-pretrained YOLOv11n starting weights and fixed 640-pixel resolution. Training and final evaluation took 244.26 minutes. [Configuration](../../configs/E11-experiment.json) · [Provenance](provenance.json)

| Final checkpoint validation | E00 | E11 | Change |
| --- | ---: | ---: | ---: |
| mAP@0.5 | 0.633096 | 0.693278 | +0.060183 |
| mAP@0.5:0.95 | 0.401513 | 0.441266 | +0.039753 |
| Precision | 0.704511 | 0.765510 | +0.060999 |
| Recall | 0.567799 | 0.607782 | +0.039984 |

The native final evaluation used the saved epoch-29 checkpoint on 733 validation images with 2,725 ground-truth objects. The epoch-history AP50 rose from 0.68622 at epoch 25 to 0.69338 at epoch 29, then fell to 0.69208 at epoch 30. AP50–95 also peaked at epoch 29, so only one epoch passed without improving checkpoint fitness before the run hit its limit. [Epoch metrics](epoch-results.csv) · [Native curves](training-curves.png)

All 12 classes gained AP50. Chair and Table remained the lowest at 0.55170 and 0.57506. The fixed-confidence size audit found mixed results on localization across object sizes. [Per-class metrics](final-validation-per-class.csv) · [Size audit](validation-size-audit.csv)

| Object size | E00 matches | E11 matches |
| --- | ---: | ---: |
| Small | 103 / 302 | 94 / 302 |
| Medium | 642 / 1,002 | 678 / 1,002 |
| Large | 1,134 / 1,421 | 1,170 / 1,421 |

The official plugin exported [submission.csv](submission.csv) at confidence 0.001 from the saved checkpoint. It contains 715 rows and 49,334 boxes and passed all five format checks. The participant submitted it on November 17, 2026. Kaggle returned **0.62263** public AP50, up **0.05748** from E00, and displayed public rank **106** when verified. [Kaggle score evidence](kaggle-score.jpg)
