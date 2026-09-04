from pathlib import Path

from src.text.text_processor import prepare_claim
from src.text.text_encoder import create_text_encoder
from src.image.image_encoder import create_image_encoder
from src.multimodal.consistency import calculate_contrastive_consistency
from src.retrieval.evidence_encoder import create_evidence_encoder
from src.retrieval.faiss_retriever import FAISSEvidenceRetriever
from src.retrieval.evidence_stance import create_evidence_stance_analyzer
from src.multimodal.fusion import MultimodalFusion
from src.verification.verifier import create_verifier
from src.explanation.explainer import ExplanationGenerator
from configs.config import TOP_K_EVIDENCE


class MultimodalVerificationPipeline:
    def __init__(self, evidence_file="data/evidence/evidence.csv"):
        self.text_encoder = create_text_encoder()
        self.image_encoder = create_image_encoder()
        self.evidence_encoder = create_evidence_encoder()
        self.stance_analyzer = create_evidence_stance_analyzer()

        self.retriever = FAISSEvidenceRetriever(evidence_file)

        evidence_embeddings = self.evidence_encoder.encode_from_file(
            evidence_file
        )
        self.retriever.build_index(evidence_embeddings)

        self.fusion = MultimodalFusion()
        self.verifier = create_verifier()
        self.explainer = ExplanationGenerator()

    def verify(self, claim, image_path, top_k=TOP_K_EVIDENCE):
        cleaned_claim = prepare_claim(claim)

        text_embedding = self.text_encoder.encode(cleaned_claim)

        clip_text_embedding = self.image_encoder.encode_text(
            cleaned_claim
        )

        image_embedding = self.image_encoder.encode_from_path(
            image_path
        )

        negative_description = "a photo of an unrelated subject"

        negative_text_embedding = self.image_encoder.encode_text(
            negative_description
        )

        contrastive_consistency = calculate_contrastive_consistency(
            clip_text_embedding,
            negative_text_embedding,
            image_embedding,
        )

        evidence_query_embedding = self.evidence_encoder.encode(
            cleaned_claim
        )

        evidence_results = self.retriever.search(
            evidence_query_embedding,
            top_k=top_k,
        )

        evidence_score = 0.0
        evidence_stance = "NEUTRAL"
        stance_confidence = 0.0

        if evidence_results:
            raw_evidence_score = max(
                0.0,
                min(
                    1.0,
                    float(evidence_results[0]["similarity"]),
                ),
            )

            if raw_evidence_score >= 0.50:
                evidence_score = raw_evidence_score

                stance_result = self.stance_analyzer.analyze(
                    cleaned_claim,
                    evidence_results[0]["text"],
                )

                evidence_stance = stance_result.label
                stance_confidence = stance_result.confidence

        consistency_score = contrastive_consistency

        text_score = evidence_score
        image_score = consistency_score

        fusion_result = self.fusion.fuse(
            text_score=text_score,
            image_score=image_score,
            consistency_score=consistency_score,
            evidence_score=evidence_score,
        )

        fused_score = fusion_result.fused_score

        if (
            evidence_stance == "CONTRADICTS"
            and stance_confidence >= 0.80
        ):
            fused_score = min(
                fused_score,
                1.0 - stance_confidence,
            )

        verification_result = self.verifier.verify(
            fused_score=fused_score,
            evidence_score=evidence_score,
        )

        if (
            evidence_stance == "CONTRADICTS"
            and stance_confidence >= 0.80
        ):
            verification_result = verification_result.__class__(
                label="MISINFORMATION",
                confidence=stance_confidence,
                fused_score=fused_score,
                reason=(
                    "Retrieved evidence strongly contradicts the claim."
                ),
            )

        explanation = self.explainer.generate(
            label=verification_result.label,
            confidence=verification_result.confidence,
            text_score=text_score,
            image_score=image_score,
            consistency_score=consistency_score,
            evidence_score=evidence_score,
            evidence_results=evidence_results,
            evidence_stance=evidence_stance,
            stance_confidence=stance_confidence,
        )

        return {
            "claim": cleaned_claim,
            "image_path": str(Path(image_path)),
            "text_score": text_score,
            "image_score": image_score,
            "consistency_score": consistency_score,
            "evidence_score": evidence_score,
            "fused_score": fused_score,
            "label": verification_result.label,
            "confidence": verification_result.confidence,
            "reason": verification_result.reason,
            "explanation": explanation,
            "evidence": evidence_results,
            "evidence_stance": evidence_stance,
            "stance_confidence": stance_confidence,
        }


def create_pipeline() -> MultimodalVerificationPipeline:
    return MultimodalVerificationPipeline()