"""
Verification and classification for the Multimodal Misinformation
Verification project.

This module converts multimodal signals into a final verification
decision and confidence score.
"""

from dataclasses import dataclass


@dataclass
class VerificationResult:
    """
    Stores the final verification decision.
    """

    label: str
    confidence: float
    fused_score: float
    reason: str


class Verifier:
    """
    Converts a fused multimodal score into a verification label.
    """

    VERIFIED_THRESHOLD = 0.70
    MISINFORMATION_THRESHOLD = 0.35

    def __init__(
        self,
        verified_threshold: float = VERIFIED_THRESHOLD,
        misinformation_threshold: float = MISINFORMATION_THRESHOLD,
    ) -> None:
        if not 0.0 <= misinformation_threshold < verified_threshold <= 1.0:
            raise ValueError(
                "Thresholds must satisfy "
                "0 <= misinformation_threshold "
                "< verified_threshold <= 1."
            )

        self.verified_threshold = verified_threshold
        self.misinformation_threshold = (
            misinformation_threshold
        )

    @staticmethod
    def _validate_score(score: float) -> float:
        """
        Validate a fused score.
        """

        score = float(score)

        if not 0.0 <= score <= 1.0:
            raise ValueError(
                "fused_score must be between 0 and 1."
            )

        return score

    def verify(
        self,
        fused_score: float,
    ) -> VerificationResult:
        """
        Convert a fused score into a verification decision.

        Parameters
        ----------
        fused_score:
            Combined multimodal verification score.

        Returns
        -------
        VerificationResult
            Final label, score, confidence, and explanation.
        """

        fused_score = self._validate_score(
            fused_score
        )

        if fused_score >= self.verified_threshold:
            label = "VERIFIED"
            confidence = fused_score
            reason = (
                "The multimodal signals provide strong "
                "support for the claim."
            )

        elif fused_score <= self.misinformation_threshold:
            label = "MISINFORMATION"
            confidence = 1.0 - fused_score
            reason = (
                "The multimodal signals provide weak "
                "support for the claim."
            )

        else:
            label = "UNCERTAIN"

            # Confidence is low near the middle of the
            # uncertain range and increases toward the
            # decision boundaries.
            confidence = 2.0 * abs(
                fused_score - 0.5
            )

            reason = (
                "The multimodal signals are not strong "
                "enough for a confident decision."
            )

        return VerificationResult(
            label=label,
            confidence=confidence,
            fused_score=fused_score,
            reason=reason,
        )


def create_verifier() -> Verifier:
    """
    Create a Verifier instance with default thresholds.
    """

    return Verifier()