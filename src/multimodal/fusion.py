"""
Multimodal fusion for the Multimodal Misinformation Verification project.

This module combines:
1. Evidence support
2. Text-image consistency

The design avoids double-counting the same underlying signals.
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

    The final score combines these two independent signals
    without double-counting them.
    """

    def __init__(
        self,
        evidence_weight: float = 0.55,
        consistency_weight: float = 0.45,
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

        self.evidence_weight = (
            evidence_weight / total_weight
        )

        self.consistency_weight = (
            consistency_weight / total_weight
        )

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

        The text_score and image_score are retained for compatibility
        with the existing pipeline and UI, but the final score uses
        the two independent signals:
        - evidence_score
        - consistency_score
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

        fused_score = (
            self.evidence_weight * evidence_score
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
    Create a MultimodalFusion instance with default weights.
    """

    return MultimodalFusion()