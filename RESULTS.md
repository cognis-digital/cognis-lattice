# Cognis Lattice — Verification Results

Reproduce with: `python bench/run_all.py` (regenerates this file).

Environment: CPython 3.14.0 on Windows/AMD64. Inputs are deterministic (fixed seed).

## Accuracy vs. planted ground truth

Metrics computed against known synthetic structure. The **clean** profile measures algorithmic correctness; the **noisy** profile injects a shared-service confounder that co-spends across actors, so clustering precision is *expected* to drop — an honest degradation measurement.

| Metric | Clean | Noisy |
|---|---|---|
| Wallet clustering (pairwise) | P=1.000 / R=1.000 / F1=1.000 | P=0.444 / R=1.000 / F1=0.615 |
| Mixer detection | P=1.000 / R=1.000 / F1=1.000 | P=1.000 / R=1.000 / F1=1.000 |
| Infrastructure clustering (pairwise) | P=1.000 / R=1.000 / F1=1.000 | P=1.000 / R=1.000 / F1=1.000 |
| Sanctions screening | P=1.000 / R=1.000 / F1=1.000 | P=1.000 / R=1.000 / F1=1.000 |
| Peel-chain recall | 1.000 | 1.000 |
| Trace reachability recall | 1.000 | 1.000 |
| STIX determinism (2 runs identical) | True | True |

### De-mix (equal-value mixing is intentionally ambiguous)

- Input coverage: **1.000** (fraction of mixer inputs given ≥1 candidate)
- Mean ambiguity: **4.0** candidate outputs per input
- Mean candidate confidence: **0.371** (scaled down by ambiguity, by design)

## Performance (single-thread, stdlib only)

| Transactions | Cluster (s) | Mixer (s) | Peel (s) | Build graph (s) | Total (s) | Tx/s |
|---:|---:|---:|---:|---:|---:|---:|
| 2,000 | 0.0027 | 0.0002 | 0.0008 | 0.0181 | 0.0219 | 91,385 |
| 10,000 | 0.0157 | 0.0016 | 0.0052 | 0.1129 | 0.1353 | 73,907 |
| 40,000 | 0.072 | 0.0062 | 0.0319 | 0.6622 | 0.7723 | 51,792 |

All numbers above are produced by `bench/run_all.py` and gated in CI by `tests/test_bench.py`. See `docs/LIMITATIONS.md` for scope caveats.
