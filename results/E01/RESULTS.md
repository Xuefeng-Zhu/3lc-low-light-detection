# E01 results

E01 evaluated the participant's reviewed training labels using the same 30-epoch settings and original validation revision as E11. The native plugin finished in 227.64 minutes and selected epoch 29. All four provenance checks passed. [Revision audit and settings](../../configs/E01-experiment.json) · [Provenance](provenance.json)

| Final checkpoint validation | E11 | E01 | Change |
| --- | ---: | ---: | ---: |
| mAP@0.5 | 0.693278 | 0.696076 | +0.002797 |
| mAP@0.5:0.95 | 0.441266 | 0.444086 | +0.002820 |
| Chair AP50 | 0.551696 | 0.573601 | +0.021904 |
| Table AP50 | 0.575057 | 0.560161 | −0.014895 |
| Precision | 0.765510 | 0.757583 | −0.007927 |
| Recall | 0.607782 | 0.599035 | −0.008747 |

All results use the same 733 validation images and 2,725 ground-truth boxes. Compared with W01, E01's aggregate AP50 was 0.000461 lower and its AP50–95 was 0.000617 lower. E01 measures one run's response to 13 box additions and one replacement on 14 training rows. [Per-class metrics](final-validation-per-class.csv) · [Epoch metrics](epoch-results.csv)

The plugin exported [submission.csv](submission.csv) from the selected checkpoint with a confidence cutoff of 0.001. It contains 715 rows and 48,316 predicted boxes. All five format checks passed. The participant's submission and Kaggle public score are pending.
