# 3LC Low-Light Detection Challenge

Private working repository for the [Kaggle competition](https://www.kaggle.com/competitions/the-3lc-low-light-detection-challenge). The objective is to improve the measured score within the competition rules; no top-rank result is claimed.

C01 is the project's best Kaggle submission at **0.63866 public AP50**, verified November 20, 2026 Pacific time. It adds 0.10 CutMix to E01's training settings and improves on E01-LC's 0.63844 at the same inference threshold of 0.0001. [Kaggle score evidence](results/C01/kaggle-score.jpg) · [Submission history](https://www.kaggle.com/competitions/the-3lc-low-light-detection-challenge/submissions)

| Result | E00 | E11 | W01 | W02 | E01 | W03 | S01 | E03 | H01 | W04 | E04 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Completed epochs | 10 | 30 | 30 | 50 | 30 | 30 | 30 | 30 | 30 | 30 | 30 |
| Final checkpoint validation mAP@0.5 | 0.633096 | 0.693278 | 0.696537 | 0.692656 | 0.696076 | **0.699040** | 0.683487 | 0.695916 | 0.691531 | 0.688968 | 0.690343 |
| Final checkpoint validation mAP@0.5:0.95 | 0.401513 | 0.441266 | **0.444703** | 0.439867 | 0.444086 | 0.440814 | 0.430991 | 0.443849 | 0.443270 | 0.439822 | 0.440268 |
| Kaggle public score | 0.56515 | 0.62263 | 0.63189 | — | **0.63733** | 0.62555 | — | — | — | — | — |
| Training job duration, including final evaluation | 121.04 min | 244.26 min | 254.59 min | 387.55 min | 227.64 min | 226.34 min | 240.90 min | 232.34 min | 229.29 min | 234.10 min | 230.81 min |

The public score covers the competition's public test subset. The private score is not available. Validation and Kaggle scores use different data and metric settings and are not interchangeable.

R01 used a disjoint 293-image holdout derived from the original validation set. On the common holdout, COCO AP50 at saved confidence ≥ 0.10 was **0.622201** for R01, **0.614679** for E04, and **0.624649** for E01. R01's 715-row prediction file passed the plugin's five format checks. [R01 results](results/R01/RESULTS.md)

## Reproduce the workflow

Use Python 3.11+ and a persistent machine with a supported GPU, then follow [setup](docs/SETUP.md). The scripts start the two local 3LC services; training and prediction happen through the **official Kaggle Competition plugin in 3LC Hub**. The plugin downloads the starter kit and its pinned initial checkpoint. There is no separate training or prediction implementation in this repository.

1. Import and validate the starter kit with the plugin.
2. Use [E00 settings](configs/E00-baseline.json) to reproduce the baseline from the official initialization.
3. Keep train and validation table revision identifiers in [experiments.csv](experiments.csv).
4. Generate and validate predictions with the plugin, then submit the chosen CSV on Kaggle.
5. Compare measured validation results before spending further daily submissions.

W01 increased sampling weight for images with a Chair or Table label and improved local AP50 by 0.33 percentage points over E11. W02's 50-epoch schedule scored 0.39 percentage points below W01. E01 kept E11's 30-epoch settings and changed the labels on 14 participant-reviewed images. Its local AP50 improved by 0.28 percentage points and its Kaggle public AP50 improved by 1.47 percentage points over E11. [Settings and experiment protocol](docs/EXPERIMENTS.md)

## Saved evidence

- [Baseline results](results/E00/RESULTS.md)
- [E11 results and audit](results/E11/RESULTS.md), [submitted prediction CSV](results/E11/submission.csv), [provenance](results/E11/provenance.json), and [Kaggle score evidence](results/E11/kaggle-score.jpg)
- [E13 interruption record](results/E13/status.json) and [partial epoch metrics](results/E13/epoch-results.csv)
- [W01 results](results/W01/RESULTS.md), [submitted prediction CSV](results/W01/submission.csv), [provenance](results/W01/provenance.json), and [Kaggle score evidence](results/W01/kaggle-score.jpg)
- [W02 results](results/W02/RESULTS.md) and [training configuration](configs/W02-experiment.json)
- [Participant-reviewed E01 results](results/E01/RESULTS.md), [submitted prediction CSV](results/E01/submission.csv), [provenance](results/E01/provenance.json), and [Kaggle score evidence](results/E01/kaggle-score.jpg)
- [W03 combined training results](results/W03/RESULTS.md), [submitted prediction CSV](results/W03/submission.csv), and [Kaggle score evidence](results/W03/kaggle-score.jpg)
- [S01 narrower-scale training results](results/S01/RESULTS.md) and [configuration](configs/S01-experiment.json)
- [E03 Chair geometry results](results/E03/RESULTS.md) and [participant revision audit](configs/E03-experiment.json)
- [H01 brightness augmentation results](results/H01/RESULTS.md) and [configuration](configs/H01-experiment.json)
- [W04 small-object sampling results](results/W04/RESULTS.md) and [configuration](configs/W04-experiment.json)
- [E04 Table addition results](results/E04/RESULTS.md) and [participant revision audit](configs/E04-experiment.json)
- [R01 re-split results](results/R01/RESULTS.md), [split manifest](results/R01/split-manifest.json), and [Kaggle score](results/R01/kaggle-score.jpg)
- [B01 box regression results](results/B01/RESULTS.md) and [configuration](configs/B01-experiment.json)
- [M01 partial-mosaic results](results/M01/RESULTS.md) and [configuration](configs/M01-experiment.json)
- [E01-LC prediction audit](results/E01/low-threshold-prediction.json), [submitted CSV](results/E01/submission-conf0001.csv), and [Kaggle score](results/E01/low-threshold-kaggle-score.jpg)
- [L01 learning-rate results](results/L01/RESULTS.md), [submitted CSV](results/L01/submission.csv), and [Kaggle score](results/L01/kaggle-score.jpg)
- [C01 CutMix results](results/C01/RESULTS.md), [configuration](configs/C01-experiment.json), and [submitted prediction CSV](results/C01/submission.csv)
- [E06 participant-review results](results/E06/RESULTS.md), [label audit](results/E06/verification.json), [confidence sweep](results/E06/validation-confidence-audit.csv), and [validated backup CSV](results/E06/submission.csv)
- [C02 higher-probability CutMix results](results/C02/RESULTS.md) and [configuration](configs/C02-experiment.json)
- [D01 classification-loss results](results/D01/RESULTS.md) and [configuration](configs/D01-experiment.json)
- [N01 gradient-accumulation results](results/N01/RESULTS.md) and [configuration](configs/N01-experiment.json)
- [C03 lower-probability CutMix results](results/C03/RESULTS.md) and [configuration](configs/C03-experiment.json)
- [L02 learning-rate results](results/L02/RESULTS.md), [configuration](configs/L02-experiment.json), and [validated prediction CSV](results/L02/submission.csv)
- [C04 repeat training configuration](configs/C04-experiment.json)
- [Per-class validation metrics](results/E00/final-validation-per-class.csv), [epoch metrics](results/E00/epoch-results.csv), and [native training curves](results/E00/training-curves.png)
- [Provenance, settings and SHA256 hashes](results/E00/provenance.json)
- [Unmodified submitted CSV](results/E00/submission.csv) and [Kaggle score evidence](results/E00/kaggle-baseline-score.jpg)
- [Aggregate supplied-label inventory](results/E00/data-summary.md)

Filesystem prefixes in the repository's metadata copies are normalized to `${THREE_LC_ROOT}` and `${KAGGLE_PLUGIN_ROOT}`. These are documented placeholders; the native Run records on the training machine were not edited. The submitted CSV is byte-identical to the plugin export.

## Competition boundaries

All experiments use YOLOv11n, 640-pixel images, and the official SHA256-pinned COCO initialization. Each run starts from that checkpoint again. Training and prediction use the official plugin; no ensembles, test-time augmentation, external data, or automated pseudo-labeling are used.

Annotation proposals come from our own plugin Runs and built-in 3LC tools. The participant visually reviews and accepts changes in the Dashboard. E01 is the first participant-saved label revision in this project. [Rules](https://www.kaggle.com/competitions/the-3lc-low-light-detection-challenge/rules) · [Host clarification](https://www.kaggle.com/competitions/the-3lc-low-light-detection-challenge/discussion/744551)

## Project export and attribution

The final native `exdark-competition` project export must still be created as a **separate prize-deliverable artifact**. It is not included in this repository snapshot. Before the competition's prize-deliverable deadline, export the final project and complete the required approach summary with the selected Run and team details. The repository currently has no collaborator invitations configured.

Source images derive from ExDark; acquire them through the official plugin and retain its bundled license and attribution. This repository does not redistribute raw images, model weights, or the installed 3LC/Ultralytics packages. Upstream tools retain their own licenses, including Ultralytics' AGPL-3.0/commercial terms.
