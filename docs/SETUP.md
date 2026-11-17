# Local setup

The recorded working installation used Python 3.12.14, 3LC 3.4.2 and 3LC Compute 1.1.0. The official Hub plugin 1.2.15 managed its own Python 3.12.16, PyTorch 2.11.0+cu128, CUDA 12.8, Ultralytics 8.4.66 and 3LC 3.3.2 environment. Training was verified on an NVIDIA T500 with 4 GiB VRAM and driver 595.99.02.

Run the following from the repository root in Bash:

```bash
source scripts/env.sh
python3.12 -m venv "$VIRTUAL_ENV"
"$VIRTUAL_ENV/bin/python" -m pip install -r requirements.txt
bash scripts/login.sh
```

Use Python 3.11+ if Python 3.12 is unavailable. To reuse an existing installation, export an **absolute** `THREE_LC_ROOT` before sourcing `scripts/env.sh`; otherwise local state is placed under `.local/three-lc` in this checkout. For a fresh installation the runtime folder, keys, plugins and cache are created locally and ignored by Git. The plugin may also keep its starter kit and job state under its official default `~/.3lc-kaggle-plugin` location.

The login script invokes the official hidden CLI prompt. Obtain the existing key from [your 3LC account](https://account.3lc.ai/api-key); do not pass it as a shell argument or commit it.

Start each service in its own terminal, from the repository root:

```bash
bash scripts/start-services.sh object
```

```bash
bash scripts/start-services.sh compute
```

Both bind to localhost only: Object Service on 5015 and Compute Service on 5020. Open [3LC Hub](https://hub.3lc.ai), install the official **Kaggle Competition** plugin from its catalog, and use its Import, Train, and Predict tabs. Keep the service terminals running. Follow the [official setup guide](https://www.kaggle.com/competitions/the-3lc-low-light-detection-challenge/overview/setup) for platform-specific requirements.

## Package records

`requirements.txt` pins the two main service packages used here. `environment/main-environment-freeze.txt` is an archival snapshot of the original main virtual environment, **not a portable cross-platform lockfile or the plugin's dependency environment**. The official Hub provisions plugin dependencies.

## Optional Linux compiler fallback

On the original machine, Annoy required a C++ compiler and none was installed. A local Zig compiler built the unmodified dependency. If a system C/C++ compiler is already available, use it normally. Otherwise the recorded fallback can be enabled for the Compute Service terminal:

```bash
source scripts/env.sh
"$VIRTUAL_ENV/bin/python" -m pip install -r requirements-compiler.txt
export PATH="$PWD/scripts/toolchain:$PATH"
bash scripts/start-services.sh compute
```

The `c++` adapter omits Zig's unsupported GNU archive-visibility option and adds `-fno-finite-math-only` to preserve Annoy's infinity semantics. The original installation passed Euclidean, angular, Manhattan and dot-product index-query checks. These wrappers are portable equivalents; they do not modify plugin source or model logic.

## Export numerical metrics from a completed Run

```bash
source scripts/env.sh
"$VIRTUAL_ENV/bin/python" -B scripts/export_run_metrics.py   --run-url "$TLC_PROJECT_ROOT_URL/exdark-competition/runs/E00_baseline_e10_b4_initial"   --output "$THREE_LC_ROOT/final-validation-per-class.csv"
```

The helper reads only final per-class numerical metrics through the 3LC SDK. It refuses incomplete or ambiguous Runs and existing output files; it does not train models, create predictions or edit labels. SDK reads may validate the existing 3LC login online.

## Recorded hardware limitation

CPU clocks temporarily fell to about 400 MHz during E00, slowing data preparation even though training used CUDA. A later sample recovered to 2–3.5 GHz with 85% GPU utilization. The cause was not established, and no power or thermal controls were changed. Future timing estimates should use each new run's measured epochs.
