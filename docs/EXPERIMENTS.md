# Experiment protocol

E00 used original train and validation revisions, 10 epochs, batch 4, seed 0, and the official plugin. It achieved final validation AP50 0.633096 and Kaggle public score 0.56515.

E00's `epochs=10` and `close_mosaic=10` disabled mosaic before epoch 1. E10 evaluated a 30-epoch cosine schedule with AdamW, batch 8, workers 2 and mosaic for the first 20 epochs. The run stalled during epoch 5 after four completed epochs. The participant approved restarting the Kaggle worker. [E10 settings and recovery record](../configs/E10-experiment.json)

E11 retried with workers set to 0 and `warmup_bias_lr=0.0` and completed all 30 epochs. Its selected checkpoint reached 0.693278 validation AP50, with gains in all 12 classes. The changed parameters were tested together. [E11 configuration](../configs/E11-experiment.json) · [Results](../results/E11/RESULTS.md)

E13 starts again from the official pretrained weights and uses the same initial train and validation revisions. It extends the cosine schedule to 50 epochs, retains early stopping after eight epochs without validation fitness improvement, and sets `close_mosaic=30` to keep mosaic active for the first 20 epochs. The longer cosine schedule changes learning rates throughout training. [E13 configuration](../configs/E13-experiment.json)

For label-quality experiments, use the native Dashboard workflows to present model-derived candidates to the participant. The participant reviews each change and commits a descriptively named training-table revision. Preserve the original validation revision for comparable measurements. Compare otherwise identical runs before and after each batch of changes; each run still starts from the pinned official initialization.

The separate [W01 sampling revision](../configs/W01-experiment.json), saved by 3LC as `exdark_train/Modified1297Values`, sets Weight to 1.5 for exactly 1,297 training images with a supplied Chair or Table label. The other 4,613 have weight 1.0. The SDK verified all rows, schema, image references, and boxes against `initial`. If E11's final class scores justify testing it, select this exact training revision and `exdark_val/initial`, turn **Use latest revision** off, and enable **Use sampling weights**. This activates sampling with replacement. For the human review experiment, select the reviewed revision explicitly.

Append completed and active experiments to `experiments.csv`, including native Run URL, revisions, requested/effective settings, duration, final-checkpoint validation metrics, exact submission path and Kaggle score when measured. Leave unknown fields blank. Never equate maximum epoch AP50 with the best checkpoint's final evaluation: the installed Ultralytics version selects `best.pt` by mAP50–95.

Predictions in the Dashboard were collected at confidence 0.1 for E00. Native final validation and the submitted CSV use confidence 0.001. Export max_det is 300; the competition uses its separate COCOeval AP50 specification with maxDets 100. Always label which metric and data split a score describes.

The validation size audit measures one-to-one same-class matches at IoU ≥ 0.50 and a collected confidence threshold of 0.10. Size is the equivalent square side after scaling to fit 640 pixels. E11 matched more medium and large objects, and fewer small objects, than E00. Use final native AP50 for checkpoint comparisons. [E00 box-size breakdown](../results/E00/validation-size-audit.csv) · [E11 box-size breakdown](../results/E11/validation-size-audit.csv)

Run the same audit with the configured local Python and a completed native Run directory:

```bash
source scripts/env.sh
"$VIRTUAL_ENV/bin/python" -B scripts/audit_validation_sizes.py \
    "$TLC_PROJECT_ROOT_URL/exdark-competition/runs/E00_baseline_e10_b4_initial"
```
