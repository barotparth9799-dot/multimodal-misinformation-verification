import pytest
import torch

from src.multimodal.consistency import (
    calculate_consistency_score,
    calculate_contrastive_consistency,
    cosine_similarity,
    normalize_similarity,
)


def test_cosine_similarity_identical_vectors():
    first = torch.tensor([1.0, 0.0, 0.0])
    second = torch.tensor([1.0, 0.0, 0.0])

    result = cosine_similarity(first, second)

    assert result == pytest.approx(1.0)


def test_cosine_similarity_opposite_vectors():
    first = torch.tensor([1.0, 0.0])
    second = torch.tensor([-1.0, 0.0])

    result = cosine_similarity(first, second)

    assert result == pytest.approx(-1.0)


def test_normalize_similarity():
    assert normalize_similarity(-1.0) == pytest.approx(0.0)
    assert normalize_similarity(0.0) == pytest.approx(0.5)
    assert normalize_similarity(1.0) == pytest.approx(1.0)


def test_consistency_score_for_identical_vectors():
    first = torch.tensor([1.0, 0.0, 0.0])
    second = torch.tensor([1.0, 0.0, 0.0])

    result = calculate_consistency_score(first, second)

    assert result == pytest.approx(1.0)


def test_contrastive_consistency_prefers_positive_description():
    positive = torch.tensor([1.0, 0.0, 0.0])
    negative = torch.tensor([-1.0, 0.0, 0.0])
    image = torch.tensor([1.0, 0.0, 0.0])

    result = calculate_contrastive_consistency(
        positive,
        negative,
        image,
    )

    assert result == pytest.approx(1.0)


def test_contrastive_consistency_equal_similarity():
    positive = torch.tensor([1.0, 0.0])
    negative = torch.tensor([0.0, 1.0])
    image = torch.tensor([1.0, 1.0])

    result = calculate_contrastive_consistency(
        positive,
        negative,
        image,
    )

    assert result == pytest.approx(0.5)


def test_cosine_similarity_rejects_wrong_dimension():
    first = torch.tensor([1.0, 0.0])
    second = torch.tensor([1.0, 0.0, 0.0])

    with pytest.raises(ValueError):
        cosine_similarity(first, second)


def test_cosine_similarity_rejects_zero_vector():
    first = torch.tensor([0.0, 0.0])
    second = torch.tensor([1.0, 0.0])

    with pytest.raises(ValueError):
        cosine_similarity(first, second)


def test_normalize_similarity_rejects_invalid_value():
    with pytest.raises(ValueError):
        normalize_similarity(1.5)