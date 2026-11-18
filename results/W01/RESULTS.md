# W01 results

W01 retained E11's training settings and original validation table. It used the verified Weight-only revision for training and enabled sampling with replacement. The native plugin completed 30 epochs and selected epoch 30. The GPU training job, including final evaluation, took 254.59 minutes. [Configuration](../../configs/W01-experiment.json) · [Provenance](provenance.json)

| Selected-checkpoint validation | E11 | W01 | Change |
| --- | ---: | ---: | ---: |
| mAP@0.5 | 0.693278 | 0.696537 | +0.003259 |
| mAP@0.5:0.95 | 0.441266 | 0.444703 | +0.003437 |
| Chair AP50 | 0.551696 | 0.568895 | +0.017199 |
| Table AP50 | 0.575057 | 0.580744 | +0.005687 |
| Precision | 0.765510 | 0.776315 | +0.010805 |
| Recall | 0.607782 | 0.607841 | +0.000059 |

The comparison uses the same 733 validation images and 2,725 ground-truth boxes. Eight classes improved in AP50. The largest decreases were Car and Bicycle. At fixed confidence 0.10 and IoU 0.50, small-object matches increased from 94 to 97 of 302 and medium-object matches increased from 678 to 694 of 1,002. [Per-class metrics](final-validation-per-class.csv) · [Size audit](validation-size-audit.csv)

The last training epoch reached 0.69639 AP50 and 0.44439 AP50–95. The table above gives the separate final evaluation of its saved checkpoint. [Epoch metrics](epoch-results.csv) · [Native curves](training-curves.png)

The official plugin exported [submission.csv](submission.csv) at confidence 0.001. It contains 715 rows and 47,878 predicted boxes and passed all five format checks. The participant's final submission action and the public score are pending.
