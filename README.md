# 3LC Low-Light Detection Challenge

Private working repository for the [Kaggle competition](https://www.kaggle.com/competitions/the-3lc-low-light-detection-challenge). The objective is to improve the measured score within the competition rules; no top-rank result is claimed.

The participant submitted E00, E11, and W01 on **November 17, 2026** Pacific time. W01 reached **0.63189** and ranked **90th** on the public leaderboard when verified. [Kaggle submission history](https://www.kaggle.com/competitions/the-3lc-low-light-detection-challenge/submissions)

| Result | E00 | E11 | W01 |
| --- | ---: | ---: | ---: |
| Completed epochs | 10 | 30 | 30 |
| Final checkpoint validation mAP@0.5 | 0.633096 | 0.693278 | **0.696537** |
| Final checkpoint validation mAP@0.5:0.95 | 0.401513 | 0.441266 | **0.444703** |
| Kaggle public score | 0.56515 | 0.62263 | **0.63189** |
| Validation / test images | 733 / 715 | 733 / 715 | 733 / 715 |
| Training job duration, including final evaluation | 121.04 minutes | 244.26 minutes | 254.59 minutes |
| Official provenance / CSV checks | 4/4 and 5/5 | 4/4 and 5/5 | 4/4 and 5/5 |

The public score covers the competition's public test subset. The private score is not available. Validation and Kaggle scores use different data and metric settings and are not interchangeable.

## Reproduce the workflow

Use Python 3.11+ and a persistent machine with a supported GPU, then follow [setup](docs/SETUP.md). The scripts start the two local 3LC services; training and prediction happen through the **official Kaggle Competition plugin in 3LC Hub**. The plugin downloads the starter kit and its pinned initial checkpoint. There is no separate training or prediction implementation in this repository.

1. Import and validate the starter kit with the plugin.
2. Use [E00 settings](configs/E00-baseline.json) to reproduce the baseline from the official initialization.
3. Keep train and validation table revision identifiers in [experiments.csv](experiments.csv).
4. Generate and validate predictions with the plugin, then submit the chosen CSV on Kaggle.
5. Compare measured validation results before spending further daily submissions.

E10 stalled during epoch 5 after four completed epochs. E11 completed the 30-epoch retry with workers set to 0 and `warmup_bias_lr=0.0`. A host reboot interrupted the 50-epoch E13 experiment after 12 completed epochs. W01 increased sampling weight for images with a Chair or Table label and improved local AP50 by 0.33 percentage points. W02 is testing whether a 50-epoch schedule improves the weighted run further. [Settings and experiment protocol](docs/EXPERIMENTS.md)

## Saved evidence

- [Baseline results](results/E00/RESULTS.md)
- [E11 results and audit](results/E11/RESULTS.md), [submitted prediction CSV](results/E11/submission.csv), [provenance](results/E11/provenance.json), and [Kaggle score evidence](results/E11/kaggle-score.jpg)
- [E13 interruption record](results/E13/status.json) and [partial epoch metrics](results/E13/epoch-results.csv)
- [W01 results](results/W01/RESULTS.md), [submitted prediction CSV](results/W01/submission.csv), [provenance](results/W01/provenance.json), and [Kaggle score evidence](results/W01/kaggle-score.jpg)
- [W02 training configuration](configs/W02-experiment.json)
- [Per-class validation metrics](results/E00/final-validation-per-class.csv), [epoch metrics](results/E00/epoch-results.csv), and [native training curves](results/E00/training-curves.png)
- [Provenance, settings and SHA256 hashes](results/E00/provenance.json)
- [Unmodified submitted CSV](results/E00/submission.csv) and [Kaggle score evidence](results/E00/kaggle-baseline-score.jpg)
- [Aggregate supplied-label inventory](results/E00/data-summary.md)

Filesystem prefixes in the repository's metadata copies are normalized to `${THREE_LC_ROOT}` and `${KAGGLE_PLUGIN_ROOT}`. These are documented placeholders; the native Run records on the training machine were not edited. The submitted CSV is byte-identical to the plugin export.

## Competition boundaries

All experiments use YOLOv11n, 640-pixel images, and the official SHA256-pinned COCO initialization. Each run starts from that checkpoint again. Training and prediction use the official plugin; no ensembles, test-time augmentation, external data, or automated pseudo-labeling are used.

Annotation proposals must come from our own plugin Runs or built-in 3LC tools. The participant must visually review and accept label edits in the Dashboard; external AI must not generate annotations or substitute for that review. No labels were edited for E00. [Rules](https://www.kaggle.com/competitions/the-3lc-low-light-detection-challenge/rules) · [Host clarification](https://www.kaggle.com/competitions/the-3lc-low-light-detection-challenge/discussion/744551)

## Project export and attribution

The final native `exdark-competition` project export must still be created as a **separate prize-deliverable artifact**. It is not included in this repository snapshot. Before the competition's prize-deliverable deadline, export the final project and complete the required approach summary with the selected Run and team details. The repository currently has no collaborator invitations configured.

Source images derive from ExDark; acquire them through the official plugin and retain its bundled license and attribution. This repository does not redistribute raw images, model weights, or the installed 3LC/Ultralytics packages. Upstream tools retain their own licenses, including Ultralytics' AGPL-3.0/commercial terms.
