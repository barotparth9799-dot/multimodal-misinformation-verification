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

    Parameters
    ----------
    text_embedding:
        Text embedding tensor.

    image_embedding:
        Image embedding tensor.

    Returns
    -------
    float
        Cosine similarity score.
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

    Parameters
    ----------
    similarity:
        Raw cosine similarity.

    Returns
    -------
    float
        Normalized similarity score.
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

    Parameters
    ----------
    text_embedding:
        Text embedding tensor.

    image_embedding:
        Image embedding tensor.

    Returns
    -------
    float
        Consistency score between 0 and 1.
    """

    similarity = cosine_similarity(
        text_embedding,
        image_embedding,
    )

    return normalize_similarity(similarity)