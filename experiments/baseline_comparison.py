from pathlib import Path

import pandas as pd

from src.text.text_processor import prepare_claim
from src.image.image_encoder import create_image_encoder
from src.retrieval.evidence_encoder import create_evidence_encoder
from src.retrieval.faiss_retriever import FAISSEvidenceRetriever
from src.retrieval.evidence_stance import create_evidence_stance_analyzer
from src.multimodal.consistency import calculate_contrastive_consistency
from src.multimodal.fusion import MultimodalFusion
from src.verification.verifier import create_verifier
from src.evaluation.metrics import create_evaluator


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATASET_FILE = PROJECT_ROOT / "data" / "processed" / "evaluation_dataset.csv"
EVIDENCE_FILE = PROJECT_ROOT / "data" / "evidence" / "evidence.csv"


def classify_from_evidence(
    evidence_score: float,
    evidence_stance: str,
    stance_confidence: float,
) -> str:
    """
    Evidence-only baseline.

    Uses retrieved evidence and NLI stance without image
    consistency.
    """

    if evidence_score == 0.0:
        return "UNCERTAIN"

    if (
        evidence_stance == "CONTRADICTS"
        and stance_confidence >= 0.80
    ):
        return "MISINFORMATION"

    if (
        evidence_stance == "SUPPORTS"
        and evidence_score >= 0.70
    ):
        return "VERIFIED"

    return "UNCERTAIN"


def classify_from_image(
    consistency_score: float,
) -> str:
    """
    Image-only baseline.

    Uses only text-image consistency.
    """

    if consistency_score >= 0.70:
        return "VERIFIED"

    if consistency_score <= 0.35:
        return "MISINFORMATION"

    return "UNCERTAIN"


def main() -> None:
    dataset = pd.read_csv(DATASET_FILE)

    image_encoder = create_image_encoder()
    evidence_encoder = create_evidence_encoder()
    stance_analyzer = create_evidence_stance_analyzer()

    retriever = FAISSEvidenceRetriever(
        str(EVIDENCE_FILE)
    )

    evidence_embeddings = (
        evidence_encoder.encode_from_file(
            str(EVIDENCE_FILE)
        )
    )

    retriever.build_index(
        evidence_embeddings
    )

    fusion = MultimodalFusion()
    verifier = create_verifier()
    evaluator = create_evaluator()

    true_labels = []

    evidence_predictions = []
    image_predictions = []
    multimodal_predictions = []

    print("=" * 60)
    print("BASELINE COMPARISON")
    print("=" * 60)

    for _, row in dataset.iterrows():
        claim = prepare_claim(
            str(row["claim"])
        )

        image_path = PROJECT_ROOT / str(
            row["image_path"]
        )

        true_label = str(row["label"])

        true_labels.append(true_label)

        # Evidence signal
        evidence_query_embedding = (
            evidence_encoder.encode(claim)
        )

        evidence_results = retriever.search(
            evidence_query_embedding,
            top_k=5,
        )

        evidence_score = 0.0
        evidence_stance = "NEUTRAL"
        stance_confidence = 0.0

        if evidence_results:
            raw_score = max(
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

            if raw_score >= 0.50:
                evidence_score = raw_score

                stance_result = (
                    stance_analyzer.analyze(
                        claim,
                        evidence_results[0]["text"],
                    )
                )

                evidence_stance = (
                    stance_result.label
                )

                stance_confidence = (
                    stance_result.confidence
                )

        # Image consistency signal
        clip_text_embedding = (
            image_encoder.encode_text(claim)
        )

        negative_embedding = (
            image_encoder.encode_text(
                "a photo of an unrelated subject"
            )
        )

        image_embedding = (
            image_encoder.encode_from_path(
                image_path
            )
        )

        consistency_score = (
            calculate_contrastive_consistency(
                clip_text_embedding,
                negative_embedding,
                image_embedding,
            )
        )

        # Baseline 1: evidence only
        evidence_prediction = (
            classify_from_evidence(
                evidence_score,
                evidence_stance,
                stance_confidence,
            )
        )

        # Baseline 2: image only
        image_prediction = (
            classify_from_image(
                consistency_score
            )
        )

        # Full multimodal system
        fusion_result = fusion.fuse(
            text_score=evidence_score,
            image_score=consistency_score,
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

        verification_result = verifier.verify(
            fused_score=fused_score,
            evidence_score=evidence_score,
        )

        if (
            evidence_stance == "CONTRADICTS"
            and stance_confidence >= 0.80
        ):
            multimodal_prediction = (
                "MISINFORMATION"
            )
        else:
            multimodal_prediction = (
                verification_result.label
            )

        evidence_predictions.append(
            evidence_prediction
        )

        image_predictions.append(
            image_prediction
        )

        multimodal_predictions.append(
            multimodal_prediction
        )

    evidence_metrics = evaluator.evaluate(
        true_labels,
        evidence_predictions,
    )

    image_metrics = evaluator.evaluate(
        true_labels,
        image_predictions,
    )

    multimodal_metrics = evaluator.evaluate(
        true_labels,
        multimodal_predictions,
    )

    print()
    print("EVIDENCE-ONLY BASELINE")
    print(
        f"Accuracy: {evidence_metrics['accuracy']:.4f}"
    )
    print(
        f"Macro F1: {evidence_metrics['macro_f1']:.4f}"
    )

    print()
    print("IMAGE-ONLY BASELINE")
    print(
        f"Accuracy: {image_metrics['accuracy']:.4f}"
    )
    print(
        f"Macro F1: {image_metrics['macro_f1']:.4f}"
    )

    print()
    print("FULL MULTIMODAL SYSTEM")
    print(
        f"Accuracy: {multimodal_metrics['accuracy']:.4f}"
    )
    print(
        f"Macro F1: {multimodal_metrics['macro_f1']:.4f}"
    )

    print()
    print("=" * 60)
    print("COMPARISON COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()