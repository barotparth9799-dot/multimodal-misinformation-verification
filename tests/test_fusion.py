import pytest

from src.multimodal.fusion import (
    FusionResult,
    MultimodalFusion,
    create_fusion,
)


def test_fusion_returns_fusion_result():
    fusion = MultimodalFusion()

    result = fusion.fuse(
        text_score=0.8,
        image_score=0.7,
        consistency_score=0.8,
        evidence_score=0.9,
    )

    assert isinstance(result, FusionResult)


def test_weights_are_normalized():
    fusion = MultimodalFusion(
        evidence_weight=2.0,
        consistency_weight=1.0,
    )

    assert fusion.evidence_weight == pytest.approx(2.0 / 3.0)
    assert fusion.consistency_weight == pytest.approx(1.0 / 3.0)


def test_high_consistency_keeps_full_evidence_score():
    fusion = MultimodalFusion(
        evidence_weight=0.55,
        consistency_weight=0.45,
        consistency_gate=0.60,
    )

    result = fusion.fuse(
        text_score=0.8,
        image_score=0.8,
        consistency_score=0.80,
        evidence_score=1.0,
    )

    expected = (0.55 * 1.0) + (0.45 * 0.80)

    assert result.fused_score == pytest.approx(expected)


def test_low_consistency_reduces_evidence_contribution():
    fusion = MultimodalFusion(
        evidence_weight=0.55,
        consistency_weight=0.45,
        consistency_gate=0.60,
    )

    result = fusion.fuse(
        text_score=0.9,
        image_score=0.4,
        consistency_score=0.30,
        evidence_score=1.0,
    )

    adjusted_evidence = 1.0 * (0.30 / 0.60)
    expected = (0.55 * adjusted_evidence) + (0.45 * 0.30)

    assert result.fused_score == pytest.approx(expected)


def test_consistency_at_gate_does_not_reduce_evidence():
    fusion = MultimodalFusion(
        evidence_weight=0.55,
        consistency_weight=0.45,
        consistency_gate=0.60,
    )

    result = fusion.fuse(
        text_score=0.9,
        image_score=0.6,
        consistency_score=0.60,
        evidence_score=1.0,
    )

    expected = (0.55 * 1.0) + (0.45 * 0.60)

    assert result.fused_score == pytest.approx(expected)


def test_text_and_image_scores_are_retained():
    fusion = MultimodalFusion()

    result = fusion.fuse(
        text_score=0.82,
        image_score=0.63,
        consistency_score=0.75,
        evidence_score=0.90,
    )

    assert result.text_score == pytest.approx(0.82)
    assert result.image_score == pytest.approx(0.63)
    assert result.consistency_score == pytest.approx(0.75)
    assert result.evidence_score == pytest.approx(0.90)


def test_scores_must_be_between_zero_and_one():
    fusion = MultimodalFusion()

    with pytest.raises(ValueError):
        fusion.fuse(1.1, 0.5, 0.5, 0.5)

    with pytest.raises(ValueError):
        fusion.fuse(0.5, -0.1, 0.5, 0.5)

    with pytest.raises(ValueError):
        fusion.fuse(0.5, 0.5, 1.1, 0.5)

    with pytest.raises(ValueError):
        fusion.fuse(0.5, 0.5, 0.5, -0.1)


def test_negative_weights_are_rejected():
    with pytest.raises(ValueError):
        MultimodalFusion(
            evidence_weight=-0.1,
            consistency_weight=0.5,
        )


def test_zero_total_weight_is_rejected():
    with pytest.raises(ValueError):
        MultimodalFusion(
            evidence_weight=0.0,
            consistency_weight=0.0,
        )


def test_invalid_consistency_gate_is_rejected():
    with pytest.raises(ValueError):
        MultimodalFusion(consistency_gate=-0.1)

    with pytest.raises(ValueError):
        MultimodalFusion(consistency_gate=1.1)


def test_create_fusion_uses_default_configuration():
    fusion = create_fusion()

    assert isinstance(fusion, MultimodalFusion)
    assert fusion.evidence_weight == pytest.approx(0.55)
    assert fusion.consistency_weight == pytest.approx(0.45)
    assert fusion.consistency_gate == pytest.approx(0.60)