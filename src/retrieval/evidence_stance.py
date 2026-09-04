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

    def _predict(self, text: str, text_pair: str) -> tuple[str, float]:
        result = self.classifier(
            {
                "text": text,
                "text_pair": text_pair,
            }
        )

        if isinstance(result, list):
            result = result[0]

        return result["label"].lower(), float(result["score"])

    def analyze(self, claim: str, evidence: str) -> EvidenceStance:
        if not isinstance(claim, str) or not claim.strip():
            raise ValueError("claim must be a non-empty string")

        if not isinstance(evidence, str) or not evidence.strip():
            raise ValueError("evidence must be a non-empty string")

        claim_label, claim_confidence = self._predict(
            claim,
            evidence,
        )

        evidence_label, evidence_confidence = self._predict(
            evidence,
            claim,
        )

        # Strong contradiction in either direction is treated as contradiction.
        if (
            claim_label == "contradiction"
            and claim_confidence >= 0.80
        ) or (
            evidence_label == "contradiction"
            and evidence_confidence >= 0.80
        ):
            confidence = max(
                claim_confidence
                if claim_label == "contradiction"
                else 0.0,
                evidence_confidence
                if evidence_label == "contradiction"
                else 0.0,
            )

            return EvidenceStance(
                label="CONTRADICTS",
                confidence=confidence,
            )

        # If the original claim -> evidence direction is entailment,
        # treat the evidence as supporting the claim.
        if claim_label == "entailment":
            return EvidenceStance(
                label="SUPPORTS",
                confidence=claim_confidence,
            )

        return EvidenceStance(
            label="NEUTRAL",
            confidence=max(
                claim_confidence,
                evidence_confidence,
            ),
        )


def create_evidence_stance_analyzer() -> EvidenceStanceAnalyzer:
    return EvidenceStanceAnalyzer()