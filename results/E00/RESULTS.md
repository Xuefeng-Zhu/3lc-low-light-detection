# E00 baseline results

Completed November 16, 2026 using the official 3LC Kaggle Competition plugin 1.2.15. Training used the NVIDIA T500 GPU (4 GiB VRAM), 10 epochs, batch 4 and 640-pixel images. Total native training-job time, including final evaluation, was **121.04 minutes**.

## Final saved checkpoint

| Native validation metric | Value |
| --- | ---: |
| mAP@0.5 | 0.633096 |
| mAP@0.5:0.95 | 0.401513 |
| Precision | 0.704511 |
| Recall | 0.567799 |
| Validation images | 733 |
| Ground-truth instances | 2,725 |

These are the native **After** metrics for the final best checkpoint on the validation table. Ultralytics selected the checkpoint by mAP50–95. The maximum epoch-history mAP50 was 0.63314; the separate final-checkpoint evaluation above is the result recorded in the experiment ledger. Validation uses confidence 0.001 and max_det 300. The 0.1 collection threshold only limits predictions stored for Dashboard review.

This is a local validation result. The competition's hidden-test score uses its COCOeval AP50 specification and maxDets 100; Kaggle accepted this CSV on November 17, 2026 and returned public score **0.56515**. The private score is not yet available. [Competition evaluation](https://www.kaggle.com/competitions/the-3lc-low-light-detection-challenge)

## Submission artifact

[submission.csv](submission.csv) contains **715 rows**, one for every test image, and **60,538 predicted boxes**. The native GPU prediction job, including loading, inference, CSV export and checks, took 17.59 seconds. The official plugin passed all five format checks: exact columns, row count, unique image IDs, sequential IDs aligned with sorted image IDs, and valid prediction strings.

The export uses the native best.pt, confidence **0.001**, 640 pixels and max_det 300. The low confidence cutoff retains candidates for ranked AP scoring; it does not establish an improved hidden-test score. The file was copied byte-for-byte from the plugin's timestamped output, and the SHA256 matches. **The user submitted it to Kaggle on November 17, 2026. It was accepted with public score 0.56515.** [Submission evidence](kaggle-baseline-score.jpg).

CSV SHA256: `fddd1a496f42fd3c5480f655e045fb3c127e769a5c4534a5039bb1bd032725a8`.

## Provenance and reproducibility

All four official training provenance checks passed: YOLOv11n, 640 pixels, pretrained initialization, and the pinned initial checkpoint SHA256. Train and validation revisions remain `initial`; no labels were edited. Every future training experiment must start from the pinned official initialization again.

- [Provenance, settings and artifact hashes](provenance.json)
- [Per-class final validation metrics](final-validation-per-class.csv)
- [Native per-epoch metrics](epoch-results.csv)
- [Native training curves](training-curves.png)
- [Experiment ledger](../../experiments.csv)
- [Machine setup and restart instructions](../../docs/SETUP.md)

The optimizer setting was `auto`; Ultralytics chooses the optimizer and overrides the requested `lr0=0.01`. The requested configuration is preserved in provenance, and actual per-group learning rates are in the native per-epoch CSV.

Native Run: `${THREE_LC_ROOT}/projects/exdark-competition/runs/E00_baseline_e10_b4_initial`.

## Per-class validation results

| Class | AP50 | AP50–95 | Instances |
| --- | ---: | ---: | ---: |
| Bicycle | 0.6572 | 0.4245 | 127 |
| Boat | 0.6331 | 0.3457 | 156 |
| Bottle | 0.5879 | 0.3606 | 174 |
| Bus | 0.8031 | 0.6246 | 77 |
| Car | 0.6576 | 0.4157 | 352 |
| Cat | 0.7113 | 0.4587 | 91 |
| Chair | 0.5139 | 0.2983 | 299 |
| Cup | 0.5890 | 0.3619 | 205 |
| Dog | 0.6821 | 0.4569 | 102 |
| Motorbike | 0.6077 | 0.3952 | 114 |
| People | 0.6438 | 0.3519 | 866 |
| Table | 0.5105 | 0.3241 | 162 |

Table and Chair have the lowest class AP50 in this baseline. That numerical finding can prioritize human review; it does not identify any specific annotation as incorrect. Use the native Run's Dashboard review workflows and inspect each proposed change yourself. Annotation proposals must come from your own plugin Runs or built-in 3LC tools, and label edits require human review under the host's rules. Codex has made no annotation decisions. [Host clarification](https://www.kaggle.com/competitions/the-3lc-low-light-detection-challenge/discussion/744551)

After committing an accepted training-table revision, retrain from the official initialization with the same E00 settings to isolate the effect of label changes. Keep the validation revision fixed for that comparison.

Repository metadata copies use portable path placeholders; native project records remain on the training machine. The full native project export is not part of this snapshot.
