"""
Evaluation metrics for the Multimodal Misinformation
Verification project.

This module calculates standard classification metrics and
generates a confusion matrix.
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
    Calculates classification metrics for verification results.
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
            Accuracy, precision, recall, F1-score,
            and confusion matrix.
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
            "confusion_matrix": matrix,
            "labels": self.labels,
        }


def create_evaluator() -> VerificationEvaluator:
    """
    Create a VerificationEvaluator instance.
    """

    return VerificationEvaluator()