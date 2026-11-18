# Experiment protocol

E00 used original train and validation revisions, 10 epochs, batch 4, seed 0, and the official plugin. It achieved final validation AP50 0.633096 and Kaggle public score 0.56515.

E00's `epochs=10` and `close_mosaic=10` disabled mosaic before epoch 1. E10 evaluated a 30-epoch cosine schedule with AdamW, batch 8, workers 2 and mosaic for the first 20 epochs. The run stalled during epoch 5 after four completed epochs. The participant approved restarting the Kaggle worker. [E10 settings and recovery record](../configs/E10-experiment.json)

E11 retried with workers set to 0 and `warmup_bias_lr=0.0` and completed all 30 epochs. Its selected checkpoint reached 0.693278 validation AP50, with gains in all 12 classes. On Kaggle, it improved public AP50 from 0.56515 to 0.62263. The changed parameters were tested together. [E11 configuration](../configs/E11-experiment.json) · [Results](../results/E11/RESULTS.md)

E13 used the same official starting weights and initial train and validation revisions, with a 50-epoch cosine schedule and mosaic for the first 20 epochs. A host reboot interrupted the run in epoch 13. Its best epoch-history AP50 was 0.58645 at epoch 12. The competition plugin starts every new run from the pinned weights and rejects checkpoint resume. [E13 configuration](../configs/E13-experiment.json) · [Interruption record](../results/E13/status.json)

For label-quality experiments, use the native Dashboard workflows to present model-derived candidates to the participant. The participant reviews each change and commits a descriptively named training-table revision. Preserve the original validation revision for comparable measurements. Compare otherwise identical runs before and after each batch of changes; each run still starts from the pinned official initialization.

W01 uses `exdark_train/Modified1297Values`, which sets Weight to 1.5 for exactly 1,297 training images with a supplied Chair or Table label. The other 4,613 have weight 1.0. The SDK verified all rows, schema, image references, and boxes against `initial`. W01 selected that exact revision and `exdark_val/initial` with **Use latest revision** off and **Use sampling weights** on. This activates sampling with replacement. Compare overall and per-class AP50 against E11, the matched training configuration. [W01 configuration](../configs/W01-experiment.json)

Append completed and active experiments to `experiments.csv`, including native Run URL, revisions, requested/effective settings, duration, final-checkpoint validation metrics, exact submission path and Kaggle score when measured. Leave unknown fields blank. Never equate maximum epoch AP50 with the best checkpoint's final evaluation: the installed Ultralytics version selects `best.pt` by mAP50–95.

Predictions in the Dashboard were collected at confidence 0.1 for E00. Native final validation and the submitted CSV use confidence 0.001. Export max_det is 300; the competition uses its separate COCOeval AP50 specification with maxDets 100. Always label which metric and data split a score describes.

The validation size audit measures one-to-one same-class matches at IoU ≥ 0.50 and a collected confidence threshold of 0.10. Size is the equivalent square side after scaling to fit 640 pixels. E11 matched more medium and large objects, and fewer small objects, than E00. Use final native AP50 for checkpoint comparisons. [E00 box-size breakdown](../results/E00/validation-size-audit.csv) · [E11 box-size breakdown](../results/E11/validation-size-audit.csv)

Run the same audit with the configured local Python and a completed native Run directory:

```bash
source scripts/env.sh
"$VIRTUAL_ENV/bin/python" -B scripts/audit_validation_sizes.py \
    "$TLC_PROJECT_ROOT_URL/exdark-competition/runs/E00_baseline_e10_b4_initial"
```
