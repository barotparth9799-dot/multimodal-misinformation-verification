"""
Text-image consistency utilities for the Multimodal Misinformation
Verification project.

This module compares text and image embeddings to estimate how well
the image is semantically related to the submitted claim.
"""

import torch


def cosine_similarity(
    text_embedding: torch.Tensor,
    image_embedding: torch.Tensor,
) -> float:
    """
    Calculate cosine similarity between one text and one image embedding.
    """

    if not isinstance(text_embedding, torch.Tensor):
        raise TypeError("text_embedding must be a torch.Tensor.")

    if not isinstance(image_embedding, torch.Tensor):
        raise TypeError("image_embedding must be a torch.Tensor.")

    text_embedding = text_embedding.float().flatten()
    image_embedding = image_embedding.float().flatten()

    if text_embedding.numel() != image_embedding.numel():
        raise ValueError(
            "Text and image embeddings must have the same dimension."
        )

    text_norm = torch.norm(text_embedding)
    image_norm = torch.norm(image_embedding)

    if text_norm == 0 or image_norm == 0:
        raise ValueError(
            "Embeddings must not contain a zero vector."
        )

    similarity = torch.nn.functional.cosine_similarity(
        text_embedding.unsqueeze(0),
        image_embedding.unsqueeze(0),
        dim=1,
    )

    return float(similarity.item())


def normalize_similarity(similarity: float) -> float:
    """
    Convert cosine similarity from [-1, 1] to [0, 1].
    """

    if not -1.0 <= similarity <= 1.0:
        raise ValueError(
            "Cosine similarity must be between -1 and 1."
        )

    return (similarity + 1.0) / 2.0


def calculate_consistency_score(
    text_embedding: torch.Tensor,
    image_embedding: torch.Tensor,
) -> float:
    """
    Calculate a normalized text-image consistency score.

    This preserves the original cosine-based consistency calculation
    for compatibility with the existing pipeline.
    """

    similarity = cosine_similarity(
        text_embedding,
        image_embedding,
    )

    return normalize_similarity(similarity)


def calculate_contrastive_consistency(
    positive_text_embedding: torch.Tensor,
    negative_text_embedding: torch.Tensor,
    image_embedding: torch.Tensor,
) -> float:
    """
    Calculate contrastive image-text consistency.

    The score measures whether the image is more similar to the
    positive claim description than to the negative description.

    The result is normalized to the range [0, 1]:

        0.5 = equal similarity
        >0.5 = positive description is more compatible
        <0.5 = negative description is more compatible
    """

    positive_similarity = cosine_similarity(
        positive_text_embedding,
        image_embedding,
    )

    negative_similarity = cosine_similarity(
        negative_text_embedding,
        image_embedding,
    )

    margin = positive_similarity - negative_similarity

    score = 0.5 + (margin / 2.0)

    return max(
        0.0,
        min(
            1.0,
            score,
        ),
    )