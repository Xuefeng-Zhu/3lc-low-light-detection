# 3LC Low-Light Detection Challenge

Private working repository for the [Kaggle competition](https://www.kaggle.com/competitions/the-3lc-low-light-detection-challenge). The objective is to improve the measured score within the competition rules; no top-rank result is claimed.

The original-label baseline **E00** completed 10 epochs on an NVIDIA T500 GPU and was submitted by the participant on **November 17, 2026**.

| Result | Value |
| --- | ---: |
| Final checkpoint validation mAP@0.5 | 0.633096 |
| Final checkpoint validation mAP@0.5:0.95 | 0.401513 |
| Kaggle public score | **0.56515** |
| Validation / test images | 733 / 715 |
| Training job duration, including final evaluation | 121.04 minutes |
| Official provenance / CSV checks | 4/4 / 5/5 passed |

The public score covers the competition's public test subset. The private score is not available. Validation and Kaggle scores use different data and metric settings and are not interchangeable.

## Reproduce the workflow

Use Python 3.11+ and a persistent machine with a supported GPU, then follow [setup](docs/SETUP.md). The scripts start the two local 3LC services; training and prediction happen through the **official Kaggle Competition plugin in 3LC Hub**. The plugin downloads the starter kit and its pinned initial checkpoint. There is no separate training or prediction implementation in this repository.

1. Import and validate the starter kit with the plugin.
2. Use [E00 settings](configs/E00-baseline.json) to reproduce the baseline from the official initialization.
3. Keep train and validation table revision identifiers in [experiments.csv](experiments.csv).
4. Generate and validate predictions with the plugin, then submit the chosen CSV on Kaggle.
5. Compare measured validation results before spending further daily submissions.

E00's validation curve was still improving at epoch 10, and its `close_mosaic=10` setting disabled mosaic from the first epoch. **E10 was interrupted after stalling during epoch 5**, with four completed epochs and a last epoch mAP@0.5 of 0.44835. Its [settings and recovery record](configs/E10-experiment.json) and [partial epoch metrics](results/E10/epoch-results.csv) are preserved. Only the Kaggle worker was restarted; a subsequent CUDA calculation passed. **E11 is now running** from fresh official initialization, using 30 epochs, batch 8, workers 0, and explicit `warmup_bias_lr=0.0`. [E11 configuration](configs/E11-experiment.json). These are precautionary changes, not a confirmed stall fix or measured improvement. Neither E10 nor E11 has final-checkpoint metrics. See [experiment protocol](docs/EXPERIMENTS.md).

## Saved evidence

- [Baseline results](results/E00/RESULTS.md)
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
