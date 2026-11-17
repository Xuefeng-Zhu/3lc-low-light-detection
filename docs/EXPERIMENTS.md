# Experiment protocol

E00 is the only completed experiment in this repository snapshot. It used original train and validation revisions, 10 epochs, batch 4, seed 0, and the official plugin. It achieved final validation AP50 0.633096 and Kaggle public score 0.56515. No label edits were made.

The baseline's validation AP50 increased through every epoch, and its validation losses were still falling at the end. With `epochs=10` and `close_mosaic=10`, mosaic was disabled before epoch 1. E10 was launched on November 17, 2026 through the official plugin with 30 epochs, batch 8, workers 2, AdamW at lr0=0.000625, cosine scheduling and close_mosaic=10. It uses the original train and validation revisions and fresh official initialization. Its native job is `d49f9ba8877943f9bd70c7d0a5a7d8c4`; see [the settings snapshot](../configs/E10-experiment.json). E10 completed four epochs at effective batch 8, then stalled during epoch 5. The targeted Kaggle worker was restarted with participant approval; native files and partial metrics remain, and E10 is interrupted rather than completed. [E11](../configs/E11-experiment.json) is the fresh retry with workers=0 and warmup_bias_lr=0.0. Its final performance and whether it avoids the stall are still unverified. A combined configuration experiment does not isolate the effect of each parameter.

For label-quality experiments, use the native Dashboard workflows to present model-derived candidates to the participant. The participant reviews each change and commits a descriptively named training-table revision. Preserve the original validation revision for comparable measurements. Compare otherwise identical runs before and after each batch of changes; each run still starts from the pinned official initialization.

Append completed and active experiments to `experiments.csv`, including native Run URL, revisions, requested/effective settings, duration, final-checkpoint validation metrics, exact submission path and Kaggle score when measured. Leave unknown fields blank. Never equate maximum epoch AP50 with the best checkpoint's final evaluation: the installed Ultralytics version selects `best.pt` by mAP50–95.

Predictions in the Dashboard were collected at confidence 0.1 for E00. Native final validation and the submitted CSV use confidence 0.001. Export max_det is 300; the competition uses its separate COCOeval AP50 specification with maxDets 100. Always label which metric and data split a score describes.

E00 matched 103 of 302 small validation objects and 1,134 of 1,421 large objects among its saved predictions. Medium chairs matched 35 of 87 and medium tables matched 6 of 25. Compare E11's matches on the original validation revision to see where the longer run improves detection. These rates use a one-to-one match at IoU ≥ 0.50 and collection confidence ≥ 0.10. Size is the equivalent square side after scaling to fit 640 pixels. Use the native final AP50 for checkpoint comparisons. [E00 box-size breakdown](../results/E00/validation-size-audit.csv)

Run the same audit with the configured local Python and a completed native Run directory:

```bash
source scripts/env.sh
"$VIRTUAL_ENV/bin/python" -B scripts/audit_validation_sizes.py \
    "$TLC_PROJECT_ROOT_URL/exdark-competition/runs/E00_baseline_e10_b4_initial"
```
