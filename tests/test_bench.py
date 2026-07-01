"""Gate the verification claims: the metrics in RESULTS.md must hold."""

from bench import datagen, evaluate


def test_clean_profile_recovers_ground_truth():
    r = evaluate.evaluate(datagen.generate(profile="clean"))
    assert r["wallet_clustering"]["f1"] == 1.0
    assert r["mixer_detection"]["f1"] == 1.0
    assert r["infra_clustering"]["f1"] == 1.0
    assert r["sanctions"]["precision"] == 1.0
    assert r["sanctions"]["recall"] == 1.0
    assert r["peel_chain_recall"] == 1.0
    assert r["trace_recall"] == 1.0
    assert r["determinism"] is True


def test_mixer_precision_no_false_positives():
    r = evaluate.evaluate(datagen.generate(profile="clean"))
    assert r["mixer_detection"]["fp"] == 0


def test_noisy_profile_degrades_precision_but_keeps_recall():
    r = evaluate.evaluate(datagen.generate(profile="noisy"))
    # confounder over-merges clusters: recall stays perfect, precision drops
    assert r["wallet_clustering"]["recall"] == 1.0
    assert r["wallet_clustering"]["precision"] < 1.0
    # sanctions/infra are unaffected by the confounder
    assert r["sanctions"]["f1"] == 1.0
    assert r["infra_clustering"]["f1"] == 1.0


def test_demix_reports_ambiguity():
    r = evaluate.evaluate(datagen.generate(profile="clean"))
    assert r["demix"]["input_coverage"] == 1.0
    assert r["demix"]["mean_ambiguity"] >= 2.0  # equal-value mixing is ambiguous
    assert r["demix"]["mean_confidence"] < 0.8  # confidence scaled down accordingly


def test_determinism_both_profiles():
    for profile in ("clean", "noisy"):
        assert evaluate.evaluate(datagen.generate(profile=profile))["determinism"] is True
