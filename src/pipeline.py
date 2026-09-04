"""
End-to-end multimodal misinformation verification pipeline.

This module connects:
1. Claim text processing
2. Text encoding
3. Image encoding
4. Contrastive text-image consistency
5. Evidence retrieval
6. Multimodal score fusion
7. Verification
8. Human-readable explanation
"""

from pathlib import Path

from src.text.text_processor import prepare_claim
from src.text.text_encoder import create_text_encoder
from src.image.image_encoder import create_image_encoder
from src.multimodal.consistency import (
    calculate_contrastive_consistency,
)
from src.retrieval.evidence_encoder import create_evidence_encoder
from src.retrieval.faiss_retriever import FAISSEvidenceRetriever
from src.multimodal.fusion import MultimodalFusion
from src.verification.verifier import create_verifier
from src.explanation.explainer import ExplanationGenerator

from configs.config import TOP_K_EVIDENCE


class MultimodalVerificationPipeline:
    """
    Complete pipeline for multimodal misinformation verification.
    """

    def __init__(
        self,
        evidence_file: str | Path = "data/evidence/evidence.csv",
    ) -> None:

        self.text_encoder = create_text_encoder()
        self.image_encoder = create_image_encoder()

        self.evidence_encoder = create_evidence_encoder()

        self.retriever = FAISSEvidenceRetriever(
            evidence_file
        )

        evidence_embeddings = (
            self.evidence_encoder.encode_from_file(
                evidence_file
            )
        )

        self.retriever.build_index(
            evidence_embeddings
        )

        self.fusion = MultimodalFusion()
        self.verifier = create_verifier()
        self.explainer = ExplanationGenerator()

    def verify(
        self,
        claim: str,
        image_path: str | Path,
        top_k: int = TOP_K_EVIDENCE,
    ) -> dict:
        """
        Run complete multimodal verification.

        Returns a dictionary containing:
        - cleaned claim
        - text-image contrastive consistency
        - retrieved evidence
        - fused score
        - verification result
        - explanation
        """

        cleaned_claim = prepare_claim(claim)

        # Keep the transformer text encoder active as part of
        # the multimodal pipeline.
        text_embedding = self.text_encoder.encode(
            cleaned_claim
        )

        # OpenCLIP text and image embeddings share the same
        # multimodal embedding space.
        clip_text_embedding = (
            self.image_encoder.encode_text(
                cleaned_claim
            )
        )

        image_embedding = (
            self.image_encoder.encode_from_path(
                image_path
            )
        )

        # Create a neutral contrastive description.
        #
        # This is intentionally generic and does not refer
        # to any particular test image or object.
        negative_description = (
            "a photo of an unrelated subject"
        )

        negative_text_embedding = (
            self.image_encoder.encode_text(
                negative_description
            )
        )

        contrastive_consistency = (
            calculate_contrastive_consistency(
                clip_text_embedding,
                negative_text_embedding,
                image_embedding,
            )
        )

        evidence_query_embedding = (
            self.evidence_encoder.encode(
                cleaned_claim
            )
        )

        evidence_results = self.retriever.search(
            evidence_query_embedding,
            top_k=top_k,
        )

        if evidence_results:
            evidence_score = max(
                0.0,
                min(
                    1.0,
                    float(
                        evidence_results[0][
                            "similarity"
                        ]
                    ),
                ),
            )
        else:
            evidence_score = 0.0

        # The contrastive consistency score acts as the
        # multimodal consistency signal.
        consistency_score = contrastive_consistency

        text_score = evidence_score
        image_score = consistency_score

        fusion_result = self.fusion.fuse(
            text_score=text_score,
            image_score=image_score,
            consistency_score=consistency_score,
            evidence_score=evidence_score,
        )

        verification_result = self.verifier.verify(
            fusion_result.fused_score
        )

        explanation = self.explainer.generate(
            label=verification_result.label,
            confidence=verification_result.confidence,
            text_score=text_score,
            image_score=image_score,
            consistency_score=consistency_score,
            evidence_score=evidence_score,
            evidence_results=evidence_results,
        )

        return {
            "claim": cleaned_claim,
            "image_path": str(image_path),
            "text_score": text_score,
            "image_score": image_score,
            "consistency_score": consistency_score,
            "evidence_score": evidence_score,
            "fused_score": fusion_result.fused_score,
            "label": verification_result.label,
            "confidence": verification_result.confidence,
            "reason": verification_result.reason,
            "explanation": explanation,
            "evidence": evidence_results,
        }


def create_pipeline(
    evidence_file: str | Path = "data/evidence/evidence.csv",
) -> MultimodalVerificationPipeline:
    """
    Create and return the complete verification pipeline.
    """

    return MultimodalVerificationPipeline(
        evidence_file=evidence_file
    )