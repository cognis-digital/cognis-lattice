# SOLIC Challenge Area 2 — Capability Mapping

How Cognis Lattice maps to the DoW SOLIC / ONIX OTA **Challenge Area 2:
Deanonymization of Illicit Internet Activities for Counter-Threat Finance.**

| Desired capability | Cognis Lattice | Module |
|---|---|---|
| IP deanonymization across Tor/VPN/proxy | Anonymizer enrichment + TLS/domain fingerprint clustering to correlate anonymized addresses to shared infrastructure | `netattr` |
| Behavioral & temporal IP analysis | Activity-window signatures + co-occurrence correlation producing durable network signatures | `netattr` |
| Blockchain analytics & wallet identification | Common-input clustering + forward/backward flow tracing across transparent ledgers | `chain` |
| De-mixing / de-tumbling with confidence | Mixer/CoinJoin detection + confidence-scored de-mix candidate linkage (honest ambiguity) | `chain` |
| Real-time alerting on high-value/known-actor activity | Watchlist screening hooks over the fused graph (address/name/known-infra) | `sanctions`, `fusion` |
| Unified IP + crypto threat-actor profiles | Connected-component fusion into one confidence-scored threat-actor graph | `fusion` |
| Legally shareable products | Deterministic, provenance-tracked STIX 2.1 export | `stix` |
| Compliance / self-hosting | Zero-dependency, offline/air-gap deployment; no data egress | whole package |

## TRL posture (honest)

- **Components (TRL 5–6):** the clustering, tracing, infrastructure-fingerprinting,
  screening, and STIX-export methods are working, tested software.
- **Integrated fusion workflow (prototype):** the end-to-end fuse-to-STIX pipeline
  is demonstrable now (`cognis-lattice demo`) and is the artifact proposed for the
  July 24 pitch/demo, to be hardened against a Government-provided reference
  dataset post-award.

See the CA2 white paper for the full submission narrative.
