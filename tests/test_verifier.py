import pytest

from src.verification.verifier import (
    Verifier,
    VerificationResult,
    create_verifier,
)


def test_verified_decision():
    verifier = Verifier()

    result = verifier.verify(0.80, evidence_score=0.90)

    assert isinstance(result, VerificationResult)
    assert result.label == "VERIFIED"
    assert result.confidence == 0.80
    assert result.fused_score == 0.80


def test_misinformation_decision():
    verifier = Verifier()

    result = verifier.verify(0.20, evidence_score=0.90)

    assert result.label == "MISINFORMATION"
    assert result.confidence == 0.80
    assert result.fused_score == 0.20


def test_uncertain_decision():
    verifier = Verifier()

    result = verifier.verify(0.50, evidence_score=0.90)

    assert result.label == "UNCERTAIN"
    assert result.confidence == 0.0
    assert result.fused_score == 0.50


def test_no_evidence_returns_uncertain():
    verifier = Verifier()

    result = verifier.verify(0.90, evidence_score=0.0)

    assert result.label == "UNCERTAIN"
    assert result.confidence == 0.80
    assert "No sufficiently relevant evidence" in result.reason


def test_verified_threshold_boundary():
    verifier = Verifier()

    result = verifier.verify(0.70, evidence_score=0.80)

    assert result.label == "VERIFIED"
    assert result.confidence == 0.70


def test_misinformation_threshold_boundary():
    verifier = Verifier()

    result = verifier.verify(0.35, evidence_score=0.80)

    assert result.label == "MISINFORMATION"
    assert result.confidence == 0.65


def test_invalid_fused_score_rejected():
    verifier = Verifier()

    with pytest.raises(ValueError):
        verifier.verify(1.1, evidence_score=0.8)

    with pytest.raises(ValueError):
        verifier.verify(-0.1, evidence_score=0.8)


def test_invalid_evidence_score_rejected():
    verifier = Verifier()

    with pytest.raises(ValueError):
        verifier.verify(0.5, evidence_score=1.1)

    with pytest.raises(ValueError):
        verifier.verify(0.5, evidence_score=-0.1)


def test_invalid_thresholds_rejected():
    with pytest.raises(ValueError):
        Verifier(
            verified_threshold=0.30,
            misinformation_threshold=0.40,
        )

    with pytest.raises(ValueError):
        Verifier(
            verified_threshold=1.1,
            misinformation_threshold=0.30,
        )


def test_create_verifier_uses_default_thresholds():
    verifier = create_verifier()

    assert isinstance(verifier, Verifier)
    assert verifier.verified_threshold == 0.70
    assert verifier.misinformation_threshold == 0.35