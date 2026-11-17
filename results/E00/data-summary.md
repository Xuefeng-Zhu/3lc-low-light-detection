# Provided train/validation label inventory

Read-only count generated November 16, 2026 at 09:05 PM PST. Only `labels/train/*.txt` and `labels/val/*.txt` were read. Images and test data were not opened; labels were not changed. No model calls or annotation proposals were made.

| Split | Label files / images¹ | Boxes | Empty labels | Mean boxes/image | Median | 95th percentile | Range |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| train | 5,910 | 18,959 | 0 | 3.208 | 2 | 10 | 1–58 |
| val | 733 | 2,725 | 0 | 3.718 | 2 | 11 | 1–42 |

Across train and validation, training contains 88.97% of label files and 87.43% of boxes; validation contains 11.03% and 12.57%, respectively.

| ID | Class | Train boxes | Train images | Val boxes | Val images | Train box share | Val box share |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | Bicycle | 894 | 600 | 127 | 78 | 4.72% | 4.66% |
| 1 | Boat | 1,111 | 566 | 156 | 56 | 5.86% | 5.72% |
| 2 | Bottle | 1,277 | 554 | 174 | 83 | 6.74% | 6.39% |
| 3 | Bus | 565 | 462 | 77 | 62 | 2.98% | 2.83% |
| 4 | Car | 2,338 | 1,047 | 352 | 156 | 12.33% | 12.92% |
| 5 | Cat | 727 | 609 | 91 | 80 | 3.83% | 3.34% |
| 6 | Chair | 1,900 | 984 | 299 | 143 | 10.02% | 10.97% |
| 7 | Cup | 1,323 | 678 | 205 | 88 | 6.98% | 7.52% |
| 8 | Dog | 814 | 693 | 102 | 84 | 4.29% | 3.74% |
| 9 | Motorbike | 857 | 465 | 114 | 64 | 4.52% | 4.18% |
| 10 | People | 5,966 | 2,156 | 866 | 299 | 31.47% | 31.78% |
| 11 | Table | 1,187 | 799 | 162 | 111 | 6.26% | 5.95% |

¹ Image counts use the provided one-label-file-per-image convention; image folders were not independently inspected. “Images” in the class table means label files containing at least one instance of that class. Those counts overlap across classes. Box shares use each split’s total boxes as denominator. Empty means no nonblank label rows. Percentiles use linear interpolation. These counts describe existing annotations, not annotation correctness or model performance.

Evidence directories:
- `${KAGGLE_PLUGIN_ROOT}/data/exdark-low-light/v3/starter_kit/labels/train`
- `${KAGGLE_PLUGIN_ROOT}/data/exdark-low-light/v3/starter_kit/labels/val`

The [JSON summary](data-summary.json) includes per-class image-presence percentages, exact counts, and SHA256 inventory digests for reproducibility.
