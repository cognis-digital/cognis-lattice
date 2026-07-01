# Changelog

All notable changes to Cognis Lattice are documented here.
This project adheres to [Semantic Versioning](https://semver.org/).

## [0.1.0] — 2026-06-30

Initial public release.

### Added
- Blockchain analytics: common-input wallet clustering, forward/backward money-flow
  tracing, mixer/CoinJoin detection, within-transaction de-mix candidate linkage,
  and peel-chain detection (`cognis_lattice.chain`).
- Network/infrastructure attribution: anonymizer (Tor/VPN/proxy) enrichment,
  TLS-certificate/domain fingerprint clustering, temporal signatures, and
  behavioral co-occurrence correlation (`cognis_lattice.netattr`).
- OFAC-style sanctions screening for crypto addresses and names
  (`cognis_lattice.sanctions`).
- Fusion engine building a confidence-scored threat-actor graph from all sources
  (`cognis_lattice.fusion`) with a noisy-OR confidence model
  (`cognis_lattice.confidence`).
- STIX 2.1 bundle export with deterministic IDs (`cognis_lattice.stix`).
- CLI (`cognis-lattice`) with `demo`, `cluster-chain`, `trace`, `detect-mixer`,
  `infra`, `screen`, and `fuse` subcommands.
- Zero-dependency (stdlib-only) design for offline / air-gapped deployment.
- Verification harness (`bench/`): deterministic ground-truth datasets, accuracy
  metrics (precision/recall/F1) on clean and noisy profiles, performance
  benchmarks, and a determinism check; results in `RESULTS.md`.
- 29 tests (24 unit + 5 verification gates); GitHub Actions CI across Python 3.9–3.13.
