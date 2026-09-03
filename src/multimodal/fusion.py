"""
Multimodal fusion for the Multimodal Misinformation Verification project.

This module combines:
1. Evidence support
2. Text-image consistency

A consistency gate is used so that strong textual evidence
cannot completely override a substantially inconsistent image.
"""

from dataclasses import dataclass


@dataclass
class FusionResult:
    """
    Stores the multimodal verification signals and final score.
    """

    text_score: float
    image_score: float
    consistency_score: float
    evidence_score: float
    fused_score: float


class MultimodalFusion:
    """
    Combines evidence support and text-image consistency.

    Evidence support represents how strongly retrieved evidence
    supports the claim.

    Consistency represents how well the image agrees with the claim.

    A consistency penalty is applied when the image shows weak
    agreement with the claim.
    """

    def __init__(
        self,
        evidence_weight: float = 0.55,
        consistency_weight: float = 0.45,
        consistency_gate: float = 0.60,
    ) -> None:

        if evidence_weight < 0 or consistency_weight < 0:
            raise ValueError(
                "Fusion weights cannot be negative."
            )

        total_weight = (
            evidence_weight + consistency_weight
        )

        if total_weight <= 0:
            raise ValueError(
                "At least one fusion weight must be greater than zero."
            )

        if not 0.0 <= consistency_gate <= 1.0:
            raise ValueError(
                "consistency_gate must be between 0 and 1."
            )

        self.evidence_weight = (
            evidence_weight / total_weight
        )

        self.consistency_weight = (
            consistency_weight / total_weight
        )

        self.consistency_gate = consistency_gate

    @staticmethod
    def _validate_score(
        score: float,
        score_name: str,
    ) -> float:
        """
        Validate a score is within the range [0, 1].
        """

        score = float(score)

        if score < 0.0 or score > 1.0:
            raise ValueError(
                f"{score_name} must be between 0 and 1."
            )

        return score

    def fuse(
        self,
        text_score: float,
        image_score: float,
        consistency_score: float,
        evidence_score: float,
    ) -> FusionResult:
        """
        Combine evidence support and image consistency.

        When consistency is below the configured gate, the evidence
        contribution is reduced proportionally. This prevents strong
        textual evidence from completely overriding an inconsistent
        image.

        The text_score and image_score are retained for compatibility
        with the existing pipeline and UI.
        """

        text_score = self._validate_score(
            text_score,
            "text_score",
        )

        image_score = self._validate_score(
            image_score,
            "image_score",
        )

        consistency_score = self._validate_score(
            consistency_score,
            "consistency_score",
        )

        evidence_score = self._validate_score(
            evidence_score,
            "evidence_score",
        )

        if consistency_score < self.consistency_gate:
            consistency_factor = (
                consistency_score / self.consistency_gate
            )

            adjusted_evidence_score = (
                evidence_score * consistency_factor
            )
        else:
            adjusted_evidence_score = evidence_score

        fused_score = (
            self.evidence_weight * adjusted_evidence_score
            + self.consistency_weight * consistency_score
        )

        return FusionResult(
            text_score=text_score,
            image_score=image_score,
            consistency_score=consistency_score,
            evidence_score=evidence_score,
            fused_score=fused_score,
        )


def create_fusion() -> MultimodalFusion:
    """
    Create a MultimodalFusion instance with default settings.
    """

    return MultimodalFusion()