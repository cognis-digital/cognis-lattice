"""Standard evaluation metrics (stdlib only).

- pairwise_prf: precision/recall/F1 for clustering, computed over co-membership
  pairs (the standard way to score clusterings against ground truth).
- label_prf: precision/recall/F1 for set-labeling tasks (e.g. mixer detection).
"""

from __future__ import annotations


def _pairs(clusters, universe=None):
    U = set(universe) if universe is not None else None
    s = set()
    for c in clusters:
        items = sorted(x for x in c if (U is None or x in U))
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                s.add((items[i], items[j]))
    return s


def pairwise_prf(pred_clusters, truth_clusters, universe=None) -> dict:
    P = _pairs(pred_clusters, universe)
    T = _pairs(truth_clusters, universe)
    tp = len(P & T)
    fp = len(P - T)
    fn = len(T - P)
    prec = tp / (tp + fp) if (tp + fp) else 1.0
    rec = tp / (tp + fn) if (tp + fn) else 1.0
    f1 = (2 * prec * rec / (prec + rec)) if (prec + rec) else 0.0
    return {"precision": round(prec, 4), "recall": round(rec, 4),
            "f1": round(f1, 4), "tp": tp, "fp": fp, "fn": fn}


def label_prf(pred_set, truth_set) -> dict:
    pred_set, truth_set = set(pred_set), set(truth_set)
    tp = len(pred_set & truth_set)
    fp = len(pred_set - truth_set)
    fn = len(truth_set - pred_set)
    prec = tp / (tp + fp) if (tp + fp) else 1.0
    rec = tp / (tp + fn) if (tp + fn) else 1.0
    f1 = (2 * prec * rec / (prec + rec)) if (prec + rec) else 0.0
    return {"precision": round(prec, 4), "recall": round(rec, 4),
            "f1": round(f1, 4), "tp": tp, "fp": fp, "fn": fn}
