from dataclasses import dataclass

from transformers import pipeline


@dataclass
class EvidenceStance:
    label: str
    confidence: float


class EvidenceStanceAnalyzer:
    """Classifies whether evidence supports, contradicts, or is neutral to a claim."""

    def __init__(
        self,
        model_name: str = "cross-encoder/nli-deberta-v3-small",
    ) -> None:
        self.model_name = model_name
        self.classifier = pipeline(
            "text-classification",
            model=model_name,
        )

    def analyze(self, claim: str, evidence: str) -> EvidenceStance:
        if not isinstance(claim, str) or not claim.strip():
            raise ValueError("claim must be a non-empty string")

        if not isinstance(evidence, str) or not evidence.strip():
            raise ValueError("evidence must be a non-empty string")

        result = self.classifier(
            {
                "text": claim,
                "text_pair": evidence,
            }
        )

        if isinstance(result, list):
            result = result[0]

        raw_label = result["label"].lower()
        confidence = float(result["score"])

        if raw_label == "entailment":
            label = "SUPPORTS"
        elif raw_label == "contradiction":
            label = "CONTRADICTS"
        else:
            label = "NEUTRAL"

        return EvidenceStance(
            label=label,
            confidence=confidence,
        )


def create_evidence_stance_analyzer() -> EvidenceStanceAnalyzer:
    return EvidenceStanceAnalyzer()