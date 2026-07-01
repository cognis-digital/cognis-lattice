"""Deterministic synthetic dataset generator with planted ground truth.

Given a fixed seed, `generate()` produces transactions, infrastructure
observations, and an SDN list together with the ground-truth structure that was
planted (wallet clusters, mixer txids, peel-chain starts, infra clusters,
sanctioned addresses). This lets us measure how faithfully the analytics recover
known structure — reproducibly, on any machine.

Two profiles:
- "clean": cleanly separable structure (measures algorithmic correctness).
- "noisy": injects a shared-service transaction that co-spends across two actors
  (a realistic confounder that SHOULD reduce clustering precision) — so the
  metrics honestly reflect degradation, not just best-case numbers.
"""

from __future__ import annotations

import random


def _ts(rng):
    return f"2026-01-{rng.randint(1, 28):02d}T{rng.randint(0, 23):02d}:{rng.randint(0, 59):02d}:00Z"


def generate(seed=1337, profile="clean", n_actors=8, addrs_per_actor=5,
             n_mixers=5, mixer_in=4, mixer_out=4, n_noise_tx=15,
             n_peel=3, peel_len=4, n_infra=6, ips_per_infra=3,
             n_noise_ips=6, n_sanctioned=3) -> dict:
    rng = random.Random(seed)
    txs, obs, sdn = [], [], []
    counter = {"t": 0}

    def nt():
        counter["t"] += 1
        return f"tx{counter['t']}"

    # --- Actors: co-spending chains that should cluster into one wallet each ---
    actor_addrs = []
    truth_wallets = []
    input_universe = set()
    for a in range(n_actors):
        addrs = [f"a{a}_{i}" for i in range(addrs_per_actor)]
        actor_addrs.append(addrs)
        truth_wallets.append(set(addrs))
        input_universe.update(addrs)
        for i in range(len(addrs) - 1):
            txs.append({
                "txid": nt(), "asset": "BTC", "timestamp": _ts(rng),
                "inputs": [{"address": addrs[i], "value": round(rng.uniform(0.2, 3), 3)},
                           {"address": addrs[i + 1], "value": round(rng.uniform(0.2, 3), 3)}],
                "outputs": [{"address": f"a{a}_out{i}", "value": round(rng.uniform(0.2, 3), 3)}],
            })

    # --- Noisy confounder: shared service co-spends across actor pairs ---
    merged_pairs = []
    if profile == "noisy" and n_actors >= 2:
        for a in range(0, n_actors - 1, 2):
            txs.append({
                "txid": nt(), "asset": "BTC", "timestamp": _ts(rng),
                "inputs": [{"address": actor_addrs[a][0], "value": 1.0},
                           {"address": actor_addrs[a + 1][0], "value": 1.0}],
                "outputs": [{"address": f"svc{a}", "value": 1.9}],
            })
            merged_pairs.append((a, a + 1))

    # --- Mixers (positives) ---
    truth_mixers = set()
    for m in range(n_mixers):
        txid = nt()
        truth_mixers.add(txid)
        txs.append({
            "txid": txid, "asset": "BTC", "timestamp": _ts(rng),
            "inputs": [{"address": f"mix{m}_in{k}", "value": 2.0} for k in range(mixer_in)],
            "outputs": [{"address": f"mix{m}_out{k}", "value": 1.98} for k in range(mixer_out)],
        })

    # --- Noise transactions (negatives for mixer precision) ---
    for n in range(n_noise_tx):
        txs.append({
            "txid": nt(), "asset": "BTC", "timestamp": _ts(rng),
            "inputs": [{"address": f"n{n}_in", "value": round(rng.uniform(0.1, 5), 3)}],
            "outputs": [{"address": f"n{n}_o1", "value": round(rng.uniform(0.1, 2), 3)},
                        {"address": f"n{n}_o2", "value": round(rng.uniform(0.1, 2), 3)}],
        })

    # --- Peel chains ---
    truth_peel_starts = set()
    for p in range(n_peel):
        val = round(rng.uniform(9, 12), 3)
        prev = f"peel{p}_0"
        first = True
        for step in range(peel_len):
            txid = nt()
            big = round(val * 0.8, 3)
            small = round(val * 0.12, 3)
            txs.append({
                "txid": txid, "asset": "BTC", "timestamp": _ts(rng),
                "inputs": [{"address": prev, "value": val}],
                "outputs": [{"address": f"peel{p}_x{step}", "value": small},
                            {"address": f"peel{p}_{step + 1}", "value": big}],
            })
            if first:
                truth_peel_starts.add(txid)
                first = False
            prev = f"peel{p}_{step + 1}"
            val = big

    # --- Infrastructure clusters (shared cert) + noise singletons ---
    truth_infra = []
    for c in range(n_infra):
        cert = f"cert{c}"
        ips = [f"172.18.{c}.{k + 1}" for k in range(ips_per_infra)]
        truth_infra.append(set(ips))
        for ip in ips:
            obs.append({"ip": ip, "timestamp": _ts(rng), "asn": f"AS{6000 + c}",
                        "cert_sha256": cert, "domains": [f"host{c}.example.net"],
                        "ports": [443], "tags": []})
    for j in range(n_noise_ips):
        ip = f"172.19.{j}.1"
        obs.append({"ip": ip, "timestamp": _ts(rng), "asn": f"AS{7000 + j}",
                    "cert_sha256": f"noisecert{j}", "domains": [f"noise{j}.example.net"],
                    "ports": [443], "tags": []})
        truth_infra.append({ip})

    # --- Sanctioned addresses (subset of actor addresses) ---
    flat = [addr for addrs in actor_addrs for addr in addrs]
    truth_sanctioned = set()
    for s in range(min(n_sanctioned, len(flat))):
        truth_sanctioned.add(flat[(s * addrs_per_actor) % len(flat)])
    sdn = [{"name": f"SYNTH SDN {i}", "program": "BENCH", "aka": [],
            "addresses": {"crypto": [addr]}}
           for i, addr in enumerate(sorted(truth_sanctioned))]

    return {
        "txs": txs, "obs": obs, "sdn": sdn,
        "truth": {
            "wallets": truth_wallets,
            "actor_addrs": actor_addrs,
            "input_universe": input_universe,
            "mixers": truth_mixers,
            "peel_starts": truth_peel_starts,
            "infra": truth_infra,
            "sanctioned": truth_sanctioned,
            "merged_pairs": merged_pairs,
        },
    }
