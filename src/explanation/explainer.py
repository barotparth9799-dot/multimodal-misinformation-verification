"""
Explanation generation for the Multimodal Misinformation
Verification project.

This module converts verification signals and retrieved evidence
into a human-readable explanation.
"""

from typing import Any


class ExplanationGenerator:
    """
    Generates an understandable explanation for a verification result.
    """

    def generate(
        self,
        label: str,
        confidence: float,
        text_score: float,
        image_score: float,
        consistency_score: float,
        evidence_score: float,
        evidence_results: list[dict[str, Any]] | None = None,
        evidence_stance: str = "NEUTRAL",
        stance_confidence: float = 0.0,
        compound_claim_results: list[dict[str, Any]] | None = None,
    ) -> str:
        """
        Generate a human-readable verification explanation.
        """

        evidence_results = evidence_results or []
        compound_claim_results = compound_claim_results or []

        explanation_parts = [
            f"Final result: {label}.",
            f"Confidence: {confidence * 100:.1f}%.",
        ]

        if text_score >= 0.70:
            explanation_parts.append(
                "The text signal provides strong support."
            )
        elif text_score <= 0.35:
            explanation_parts.append(
                "The text signal provides weak support."
            )
        else:
            explanation_parts.append(
                "The text signal provides moderate support."
            )

        if image_score >= 0.70:
            explanation_parts.append(
                "The image signal provides strong support."
            )
        elif image_score <= 0.35:
            explanation_parts.append(
                "The image signal provides weak support."
            )
        else:
            explanation_parts.append(
                "The image signal provides moderate support."
            )

        if consistency_score >= 0.70:
            explanation_parts.append(
                "The text and image are strongly consistent."
            )
        elif consistency_score <= 0.35:
            explanation_parts.append(
                "The text and image show low consistency."
            )
        else:
            explanation_parts.append(
                "The text and image show moderate consistency."
            )

        strong_compound_contradictions = [
            result
            for result in compound_claim_results
            if (
                result.get("stance") == "CONTRADICTS"
                and result.get("confidence", 0.0) >= 0.80
            )
        ]

        if strong_compound_contradictions:
            contradicted_claims = [
                result.get("claim", "an evaluated subclaim")
                for result in strong_compound_contradictions
            ]

            explanation_parts.append(
                "Compound claim analysis found at least one strongly "
                "contradicted subclaim: "
                + "; ".join(
                    f'"{claim}"' for claim in contradicted_claims
                )
                + "."
            )
        elif (
            evidence_stance == "CONTRADICTS"
            and stance_confidence >= 0.80
        ):
            explanation_parts.append(
                "Retrieved evidence strongly contradicts the claim."
            )
        elif evidence_stance == "SUPPORTS":
            if evidence_score >= 0.70:
                explanation_parts.append(
                    "Retrieved evidence strongly supports the claim."
                )
            elif evidence_score <= 0.35:
                explanation_parts.append(
                    "Retrieved evidence provides weak support."
                )
            else:
                explanation_parts.append(
                    "Retrieved evidence provides moderate support."
                )
        else:
            if evidence_score >= 0.70:
                explanation_parts.append(
                    "Retrieved evidence is highly relevant to the claim."
                )
            elif evidence_score <= 0.35:
                explanation_parts.append(
                    "Retrieved evidence provides weak support."
                )
            else:
                explanation_parts.append(
                    "Retrieved evidence provides moderate support."
                )

        if evidence_results:
            top_evidence = evidence_results[0]

            evidence_id = top_evidence.get(
                "evidence_id",
                "unknown",
            )

            source = top_evidence.get(
                "source",
                "unknown source",
            )

            explanation_parts.append(
                f"Top retrieved evidence: {evidence_id} "
                f"from {source}."
            )

        return " ".join(explanation_parts)


def create_explainer() -> ExplanationGenerator:
    """
    Create an ExplanationGenerator instance.
    """

    return ExplanationGenerator()