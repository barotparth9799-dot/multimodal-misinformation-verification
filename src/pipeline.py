from pathlib import Path

from src.text.text_processor import prepare_claim
from src.text.text_encoder import create_text_encoder
from src.text.claim_decomposer import create_claim_decomposer
from src.image.image_encoder import create_image_encoder
from src.image.visual_consistency import create_visual_consistency_checker
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
        self.visual_consistency_checker = create_visual_consistency_checker()
        self.claim_decomposer = create_claim_decomposer()
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

    def _evaluate_subclaims(self, cleaned_claim, top_k):
        decomposition = self.claim_decomposer.decompose(cleaned_claim)

        if not decomposition.is_compound:
            return {
                "has_strong_contradiction": False,
                "all_supported": False,
                "subclaims": [],
            }

        subclaim_results = []

        for subclaim in decomposition.claims:
            query_embedding = self.evidence_encoder.encode(subclaim)

            evidence_results = self.retriever.search(
                query_embedding,
                top_k=top_k,
            )

            best_evidence = None
            best_stance = "NEUTRAL"
            best_confidence = 0.0

            if evidence_results:
                for evidence in evidence_results:
                    similarity = max(
                        0.0,
                        min(
                            1.0,
                            float(evidence["similarity"]),
                        ),
                    )

                    if similarity < 0.50:
                        continue

                    stance_result = self.stance_analyzer.analyze(
                        subclaim,
                        evidence["text"],
                    )

                    if (
                        stance_result.label == "CONTRADICTS"
                        and stance_result.confidence > best_confidence
                    ):
                        best_evidence = evidence
                        best_stance = stance_result.label
                        best_confidence = stance_result.confidence

                    elif (
                        best_evidence is None
                        and stance_result.label == "SUPPORTS"
                    ):
                        best_evidence = evidence
                        best_stance = stance_result.label
                        best_confidence = stance_result.confidence

            subclaim_results.append(
                {
                    "claim": subclaim,
                    "evidence": best_evidence,
                    "stance": best_stance,
                    "confidence": best_confidence,
                }
            )

        has_strong_contradiction = any(
            result["stance"] == "CONTRADICTS"
            and result["confidence"] >= 0.80
            for result in subclaim_results
        )

        all_supported = (
            len(subclaim_results) > 1
            and all(
                result["stance"] == "SUPPORTS"
                and result["confidence"] >= 0.80
                for result in subclaim_results
            )
        )

        return {
            "has_strong_contradiction": has_strong_contradiction,
            "all_supported": all_supported,
            "subclaims": subclaim_results,
        }

    def verify(self, claim, image_path, top_k=TOP_K_EVIDENCE):
        cleaned_claim = prepare_claim(claim)

        text_embedding = self.text_encoder.encode(cleaned_claim)

        visual_result = self.visual_consistency_checker.check(
            cleaned_claim,
            image_path,
        )

        consistency_score = visual_result.consistency_score

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

        text_score = evidence_score
        image_score = consistency_score

        fusion_result = self.fusion.fuse(
            text_score=text_score,
            image_score=image_score,
            consistency_score=consistency_score,
            evidence_score=evidence_score,
        )

        fused_score = fusion_result.fused_score

        strong_contradiction = (
            evidence_stance == "CONTRADICTS"
            and stance_confidence >= 0.80
        )

        if strong_contradiction:
            fused_score = min(
                fused_score,
                1.0 - stance_confidence,
            )

        verification_result = self.verifier.verify(
            fused_score=fused_score,
            evidence_score=evidence_score,
        )

        if strong_contradiction:
            verification_result = verification_result.__class__(
                label="MISINFORMATION",
                confidence=stance_confidence,
                fused_score=fused_score,
                reason=(
                    "Retrieved evidence strongly contradicts the claim."
                ),
            )

        elif visual_result.is_consistent is False:
            verification_result = verification_result.__class__(
                label="UNCERTAIN",
                confidence=0.50,
                fused_score=fused_score,
                reason=(
                    "The retrieved evidence may support the claim, "
                    "but the provided image is visually inconsistent "
                    "with the claim."
                ),
            )

        compound_result = self._evaluate_subclaims(
            cleaned_claim,
            top_k,
        )

        if compound_result["has_strong_contradiction"]:
            verification_result = verification_result.__class__(
                label="MISINFORMATION",
                confidence=0.90,
                fused_score=min(fused_score, 0.10),
                reason=(
                    "At least one independently evaluated subclaim "
                    "is strongly contradicted by retrieved evidence."
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
            compound_claim_results=compound_result["subclaims"],
        )

        return {
            "claim": cleaned_claim,
            "image_path": str(Path(image_path)),
            "text_score": text_score,
            "image_score": image_score,
            "consistency_score": consistency_score,
            "evidence_score": evidence_score,
            "fused_score": verification_result.fused_score,
            "label": verification_result.label,
            "confidence": verification_result.confidence,
            "reason": verification_result.reason,
            "explanation": explanation,
            "evidence": evidence_results,
            "evidence_stance": evidence_stance,
            "stance_confidence": stance_confidence,
            "claim_visual_topic": visual_result.claim_topic,
            "claim_visual_topic_confidence": (
                visual_result.claim_topic_confidence
            ),
            "image_visual_topic": visual_result.image_topic,
            "image_visual_topic_score": visual_result.image_topic_score,
            "image_visual_topic_margin": visual_result.image_topic_margin,
            "visual_consistent": visual_result.is_consistent,
            "compound_claim": compound_result["subclaims"],
        }


def create_pipeline() -> MultimodalVerificationPipeline:
    return MultimodalVerificationPipeline()