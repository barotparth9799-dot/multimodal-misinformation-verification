"""
Evaluation metrics for the Multimodal Misinformation
Verification project.

This module calculates standard classification metrics,
macro-averaged metrics, a confusion matrix, and
confidence calibration metrics.
"""

from typing import Any

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)


class VerificationEvaluator:
    """
    Calculates classification and confidence calibration
    metrics for verification results.
    """

    def __init__(
        self,
        labels: list[str] | None = None,
    ) -> None:
        self.labels = labels or [
            "MISINFORMATION",
            "UNCERTAIN",
            "VERIFIED",
        ]

    def evaluate(
        self,
        true_labels: list[str],
        predicted_labels: list[str],
    ) -> dict[str, Any]:
        """
        Calculate classification metrics.

        Parameters
        ----------
        true_labels:
            Ground-truth labels.

        predicted_labels:
            Model-predicted labels.

        Returns
        -------
        dict
            Accuracy, weighted precision, weighted recall,
            weighted F1-score, macro F1-score, and confusion matrix.
        """

        if len(true_labels) != len(predicted_labels):
            raise ValueError(
                "true_labels and predicted_labels "
                "must have the same length."
            )

        if not true_labels:
            raise ValueError(
                "At least one evaluation sample is required."
            )

        unknown_true = set(true_labels) - set(self.labels)
        unknown_predicted = (
            set(predicted_labels) - set(self.labels)
        )

        if unknown_true:
            raise ValueError(
                f"Unknown true labels: {sorted(unknown_true)}"
            )

        if unknown_predicted:
            raise ValueError(
                "Unknown predicted labels: "
                f"{sorted(unknown_predicted)}"
            )

        accuracy = accuracy_score(
            true_labels,
            predicted_labels,
        )

        precision = precision_score(
            true_labels,
            predicted_labels,
            labels=self.labels,
            average="weighted",
            zero_division=0,
        )

        recall = recall_score(
            true_labels,
            predicted_labels,
            labels=self.labels,
            average="weighted",
            zero_division=0,
        )

        f1 = f1_score(
            true_labels,
            predicted_labels,
            labels=self.labels,
            average="weighted",
            zero_division=0,
        )

        macro_f1 = f1_score(
            true_labels,
            predicted_labels,
            labels=self.labels,
            average="macro",
            zero_division=0,
        )

        matrix = confusion_matrix(
            true_labels,
            predicted_labels,
            labels=self.labels,
        )

        return {
            "accuracy": float(accuracy),
            "precision": float(precision),
            "recall": float(recall),
            "f1_score": float(f1),
            "macro_f1": float(macro_f1),
            "confusion_matrix": matrix,
            "labels": self.labels,
        }

    def evaluate_calibration(
        self,
        true_labels: list[str],
        predicted_labels: list[str],
        confidences: list[float],
    ) -> dict[str, float]:
        """
        Evaluate whether reported confidence matches actual correctness.

        The main metric is Expected Calibration Error (ECE).
        Lower ECE means better calibration.

        Parameters
        ----------
        true_labels:
            Ground-truth labels.

        predicted_labels:
            Model-predicted labels.

        confidences:
            Model confidence values between 0 and 1.

        Returns
        -------
        dict
            Expected Calibration Error and mean confidence.
        """

        if not (
            len(true_labels)
            == len(predicted_labels)
            == len(confidences)
        ):
            raise ValueError(
                "true_labels, predicted_labels, and confidences "
                "must have the same length."
            )

        if not true_labels:
            raise ValueError(
                "At least one calibration sample is required."
            )

        if any(
            not isinstance(confidence, (int, float, np.number))
            for confidence in confidences
        ):
            raise ValueError(
                "All confidence values must be numeric."
            )

        if any(
            confidence < 0.0 or confidence > 1.0
            for confidence in confidences
        ):
            raise ValueError(
                "All confidence values must be between 0 and 1."
            )

        self.evaluate(
            true_labels,
            predicted_labels,
        )

        correctness = np.array(
            [
                true == predicted
                for true, predicted
                in zip(true_labels, predicted_labels)
            ],
            dtype=float,
        )

        confidence_array = np.array(
            confidences,
            dtype=float,
        )

        number_of_bins = 5
        bin_edges = np.linspace(
            0.0,
            1.0,
            number_of_bins + 1,
        )

        ece = 0.0

        for index in range(number_of_bins):
            lower = bin_edges[index]
            upper = bin_edges[index + 1]

            if index == number_of_bins - 1:
                mask = (
                    (confidence_array >= lower)
                    & (confidence_array <= upper)
                )
            else:
                mask = (
                    (confidence_array >= lower)
                    & (confidence_array < upper)
                )

            if not np.any(mask):
                continue

            bin_accuracy = float(
                np.mean(correctness[mask])
            )

            bin_confidence = float(
                np.mean(confidence_array[mask])
            )

            bin_fraction = float(
                np.mean(mask)
            )

            ece += (
                bin_fraction
                * abs(bin_accuracy - bin_confidence)
            )

        mean_confidence = float(
            np.mean(confidence_array)
        )

        return {
            "expected_calibration_error": float(ece),
            "mean_confidence": mean_confidence,
        }


def create_evaluator() -> VerificationEvaluator:
    """
    Create a VerificationEvaluator instance.
    """

    return VerificationEvaluator()