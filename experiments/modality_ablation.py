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


def get_evidence_signal(claim, evidence_encoder, retriever, stance_analyzer):
    query_embedding = evidence_encoder.encode(claim)
    evidence_results = retriever.search(query_embedding, top_k=5)

    evidence_score = 0.0
    evidence_stance = "NEUTRAL"
    stance_confidence = 0.0

    if evidence_results:
        raw_score = max(
            0.0,
            min(1.0, float(evidence_results[0]["similarity"])),
        )

        if raw_score >= 0.50:
            evidence_score = raw_score

            stance_result = stance_analyzer.analyze(
                claim,
                evidence_results[0]["text"],
            )

            evidence_stance = stance_result.label
            stance_confidence = stance_result.confidence

    return evidence_score, evidence_stance, stance_confidence


def get_image_signal(claim, image_path, image_encoder):
    positive_embedding = image_encoder.encode_text(claim)

    negative_embedding = image_encoder.encode_text(
        "a photo of an unrelated subject"
    )

    image_embedding = image_encoder.encode_from_path(image_path)

    return calculate_contrastive_consistency(
        positive_embedding,
        negative_embedding,
        image_embedding,
    )


def classify_evidence_only(
    evidence_score,
    evidence_stance,
    stance_confidence,
):
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


def classify_image_only(consistency_score):
    if consistency_score >= 0.70:
        return "VERIFIED"

    if consistency_score <= 0.35:
        return "MISINFORMATION"

    return "UNCERTAIN"


def main():
    dataset = pd.read_csv(DATASET_FILE)

    image_encoder = create_image_encoder()
    evidence_encoder = create_evidence_encoder()
    stance_analyzer = create_evidence_stance_analyzer()

    retriever = FAISSEvidenceRetriever(str(EVIDENCE_FILE))

    evidence_embeddings = evidence_encoder.encode_from_file(
        str(EVIDENCE_FILE)
    )

    retriever.build_index(evidence_embeddings)

    fusion = MultimodalFusion()
    verifier = create_verifier()
    evaluator = create_evaluator()

    true_labels = []

    full_predictions = []
    evidence_predictions = []
    image_predictions = []
    evidence_image_predictions = []

    print("=" * 60)
    print("MODALITY ABLATION EXPERIMENT")
    print("=" * 60)

    for _, row in dataset.iterrows():
        claim = prepare_claim(str(row["claim"]))
        image_path = PROJECT_ROOT / str(row["image_path"])
        true_label = str(row["label"])

        true_labels.append(true_label)

        evidence_score, evidence_stance, stance_confidence = (
            get_evidence_signal(
                claim,
                evidence_encoder,
                retriever,
                stance_analyzer,
            )
        )

        consistency_score = get_image_signal(
            claim,
            image_path,
            image_encoder,
        )

        # --------------------------------------------------------
        # 1. Evidence-only
        # --------------------------------------------------------
        evidence_prediction = classify_evidence_only(
            evidence_score,
            evidence_stance,
            stance_confidence,
        )

        # --------------------------------------------------------
        # 2. Image-only
        # --------------------------------------------------------
        image_prediction = classify_image_only(
            consistency_score,
        )

        # --------------------------------------------------------
        # 3. Evidence + Image Consistency
        # --------------------------------------------------------
        evidence_image_fusion = fusion.fuse(
            text_score=evidence_score,
            image_score=consistency_score,
            consistency_score=consistency_score,
            evidence_score=evidence_score,
        )

        evidence_image_score = evidence_image_fusion.fused_score

        if (
            evidence_stance == "CONTRADICTS"
            and stance_confidence >= 0.80
        ):
            evidence_image_score = min(
                evidence_image_score,
                1.0 - stance_confidence,
            )

        evidence_image_result = verifier.verify(
            fused_score=evidence_image_score,
            evidence_score=evidence_score,
        )

        if (
            evidence_stance == "CONTRADICTS"
            and stance_confidence >= 0.80
        ):
            evidence_image_prediction = "MISINFORMATION"
        else:
            evidence_image_prediction = evidence_image_result.label

        # --------------------------------------------------------
        # 4. Full multimodal production-style decision
        # --------------------------------------------------------
        full_fusion = fusion.fuse(
            text_score=evidence_score,
            image_score=consistency_score,
            consistency_score=consistency_score,
            evidence_score=evidence_score,
        )

        full_score = full_fusion.fused_score

        if (
            evidence_stance == "CONTRADICTS"
            and stance_confidence >= 0.80
        ):
            full_score = min(
                full_score,
                1.0 - stance_confidence,
            )

        full_result = verifier.verify(
            fused_score=full_score,
            evidence_score=evidence_score,
        )

        if (
            evidence_stance == "CONTRADICTS"
            and stance_confidence >= 0.80
        ):
            full_prediction = "MISINFORMATION"
        else:
            full_prediction = full_result.label

        evidence_predictions.append(evidence_prediction)
        image_predictions.append(image_prediction)
        evidence_image_predictions.append(
            evidence_image_prediction
        )
        full_predictions.append(full_prediction)

    evidence_metrics = evaluator.evaluate(
        true_labels,
        evidence_predictions,
    )

    image_metrics = evaluator.evaluate(
        true_labels,
        image_predictions,
    )

    evidence_image_metrics = evaluator.evaluate(
        true_labels,
        evidence_image_predictions,
    )

    full_metrics = evaluator.evaluate(
        true_labels,
        full_predictions,
    )

    print()
    print("EVIDENCE-ONLY")
    print(
        f"Accuracy: {evidence_metrics['accuracy']:.4f}"
    )
    print(
        f"Macro F1: {evidence_metrics['macro_f1']:.4f}"
    )

    print()
    print("IMAGE-ONLY")
    print(
        f"Accuracy: {image_metrics['accuracy']:.4f}"
    )
    print(
        f"Macro F1: {image_metrics['macro_f1']:.4f}"
    )

    print()
    print("EVIDENCE + IMAGE CONSISTENCY")
    print(
        f"Accuracy: {evidence_image_metrics['accuracy']:.4f}"
    )
    print(
        f"Macro F1: {evidence_image_metrics['macro_f1']:.4f}"
    )

    print()
    print("FULL MULTIMODAL SYSTEM")
    print(
        f"Accuracy: {full_metrics['accuracy']:.4f}"
    )
    print(
        f"Macro F1: {full_metrics['macro_f1']:.4f}"
    )

    print()
    print("=" * 60)
    print("ABLATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()