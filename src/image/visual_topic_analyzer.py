"""
CLIP-based visual topic analysis for multimodal verification.

This module uses zero-shot CLIP prompts to identify the visual concept
represented by an image. Low-margin predictions are treated as unknown
rather than being forced into an unrelated topic.
"""

from dataclasses import dataclass

import torch

from src.image.image_encoder import ImageEncoder


@dataclass
class VisualTopicResult:
    """Result of zero-shot visual topic analysis."""

    top_topic: str
    top_score: float
    second_topic: str
    second_score: float
    margin: float


class VisualTopicAnalyzer:
    """Analyze an image using a fixed set of zero-shot visual concepts."""

    UNKNOWN_MARGIN = 0.03

    TOPIC_PROMPTS = {
        "Earth": "a photo of Earth",
        "Moon": "a photo of the Moon",
        "boiling water": "a photo of boiling water",
        "red sports car": "a photo of a red sports car",
        "industrial pollution": "a photo of industrial pollution",
    }

    def __init__(self, image_encoder: ImageEncoder | None = None) -> None:
        self.image_encoder = image_encoder or ImageEncoder()
        self.topics = list(self.TOPIC_PROMPTS.keys())
        self.prompts = list(self.TOPIC_PROMPTS.values())

        self.text_embeddings = self.image_encoder.encode_text(
            self.prompts
        )

    def analyze(self, image_path: str) -> VisualTopicResult:
        """Identify the strongest visual topic in an image."""

        image_embedding = self.image_encoder.encode_from_path(
            image_path
        )

        similarities = torch.matmul(
            image_embedding,
            self.text_embeddings.T,
        )[0]

        ranked = sorted(
            zip(self.topics, similarities.tolist()),
            key=lambda item: item[1],
            reverse=True,
        )

        top_topic, top_score = ranked[0]
        second_topic, second_score = ranked[1]
        margin = float(top_score - second_score)

        if margin < self.UNKNOWN_MARGIN:
            top_topic = "Unknown"

        return VisualTopicResult(
            top_topic=top_topic,
            top_score=float(top_score),
            second_topic=second_topic,
            second_score=float(second_score),
            margin=margin,
        )


def create_visual_topic_analyzer() -> VisualTopicAnalyzer:
    """Create a visual topic analyzer."""

    return VisualTopicAnalyzer()
