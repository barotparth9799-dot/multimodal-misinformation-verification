"""
Multimodal fusion for the Multimodal Misinformation Verification project.

This module combines text, image, consistency, and evidence signals
into a single multimodal verification score.
"""

from dataclasses import dataclass


@dataclass
class FusionResult:
    """
    Stores the combined multimodal signals.
    """

    text_score: float
    image_score: float
    consistency_score: float
    evidence_score: float
    fused_score: float


class MultimodalFusion:
    """
    Combines multiple verification signals using weighted fusion.
    """

    def __init__(
        self,
        text_weight: float = 0.25,
        image_weight: float = 0.20,
        consistency_weight: float = 0.30,
        evidence_weight: float = 0.25,
    ) -> None:
        weights = [
            text_weight,
            image_weight,
            consistency_weight,
            evidence_weight,
        ]

        if any(weight < 0 for weight in weights):
            raise ValueError(
                "Fusion weights cannot be negative."
            )

        total_weight = sum(weights)

        if total_weight <= 0:
            raise ValueError(
                "At least one fusion weight must be greater than zero."
            )

        self.text_weight = text_weight / total_weight
        self.image_weight = image_weight / total_weight
        self.consistency_weight = (
            consistency_weight / total_weight
        )
        self.evidence_weight = (
            evidence_weight / total_weight
        )

    @staticmethod
    def _validate_score(
        score: float,
        score_name: str,
    ) -> float:
        """
        Validate and clamp a score to the range [0, 1].
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
        Combine the four verification signals.

        Parameters
        ----------
        text_score:
            Text-based verification signal.

        image_score:
            Image-based verification signal.

        consistency_score:
            Text-image consistency score.

        evidence_score:
            Relevance score of retrieved evidence.

        Returns
        -------
        FusionResult
            Individual signals and the final fused score.
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
            self.text_weight * text_score
            + self.image_weight * image_score
            + self.consistency_weight * consistency_score
            + self.evidence_weight * evidence_score
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