import csv
from pathlib import Path
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix

from src.pipeline import MultimodalVerificationPipeline


DATASET = Path("experiments/realistic_validation_dataset.csv")
RESULTS = Path("experiments/realistic_validation_results.csv")


def main():
    print("Loading production multimodal pipeline...")
    pipeline = MultimodalVerificationPipeline()

    with DATASET.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    results = []

    print(f"Running {len(rows)} realistic validation cases...\n")

    for row in rows:
        case_id = row["case_id"]
        claim = row["claim"]
        image_path = row["image_path"]
        expected = row["expected_label"]

        print(f"{case_id}: {row['test_type']}")

        try:
            output = pipeline.verify(claim, image_path)

            predicted = output["label"]
            confidence = float(output["confidence"])

            results.append({
                "case_id": case_id,
                "test_type": row["test_type"],
                "claim": claim,
                "image_path": image_path,
                "expected_label": expected,
                "predicted_label": predicted,
                "correct": predicted == expected,
                "confidence": confidence,
                "fused_score": float(output["fused_score"]),
                "evidence_score": float(output["evidence_score"]),
                "consistency_score": float(output["consistency_score"]),
                "evidence_stance": output["evidence_stance"],
                "stance_confidence": float(output["stance_confidence"]),
                "reason": output["reason"],
            })

            print(
                f"  Expected: {expected} | "
                f"Predicted: {predicted} | "
                f"Confidence: {confidence:.4f}"
            )

        except Exception as exc:
            print(f"  ERROR: {type(exc).__name__}: {exc}")

            results.append({
                "case_id": case_id,
                "test_type": row["test_type"],
                "claim": claim,
                "image_path": image_path,
                "expected_label": expected,
                "predicted_label": "ERROR",
                "correct": False,
                "confidence": 0.0,
                "fused_score": 0.0,
                "evidence_score": 0.0,
                "consistency_score": 0.0,
                "evidence_stance": "ERROR",
                "stance_confidence": 0.0,
                "reason": f"{type(exc).__name__}: {exc}",
            })

    fieldnames = [
        "case_id",
        "test_type",
        "claim",
        "image_path",
        "expected_label",
        "predicted_label",
        "correct",
        "confidence",
        "fused_score",
        "evidence_score",
        "consistency_score",
        "evidence_stance",
        "stance_confidence",
        "reason",
    ]

    with RESULTS.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    valid = [r for r in results if r["predicted_label"] != "ERROR"]

    if valid:
        y_true = [r["expected_label"] for r in valid]
        y_pred = [r["predicted_label"] for r in valid]

        labels = ["MISINFORMATION", "UNCERTAIN", "VERIFIED"]

        print("\n" + "=" * 60)
        print("REALISTIC VALIDATION RESULTS")
        print("=" * 60)

        print(f"Cases completed: {len(valid)}/{len(rows)}")
        print(f"Accuracy: {accuracy_score(y_true, y_pred):.4f}")
        print(f"Macro F1: {f1_score(y_true, y_pred, labels=labels, average='macro', zero_division=0):.4f}")

        print("\nConfusion Matrix")
        print("Labels:", labels)
        print(confusion_matrix(y_true, y_pred, labels=labels))

        print("\nIncorrect cases:")
        incorrect = [r for r in valid if not r["correct"]]

        if incorrect:
            for r in incorrect:
                print(
                    f"{r['case_id']} | "
                    f"{r['test_type']} | "
                    f"Expected={r['expected_label']} | "
                    f"Predicted={r['predicted_label']} | "
                    f"Confidence={r['confidence']:.4f}"
                )
        else:
            print("None")

    print(f"\nRaw results saved to: {RESULTS}")


if __name__ == "__main__":
    main()
