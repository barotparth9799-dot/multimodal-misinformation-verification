import pytest
import torch

from src.retrieval.evidence_encoder import (
    EvidenceEncoder,
    create_evidence_encoder,
)


@pytest.fixture(scope="module")
def encoder():
    return EvidenceEncoder()


def test_encode_single_text_returns_tensor(encoder):
    result = encoder.encode("The Earth is approximately spherical.")

    assert isinstance(result, torch.Tensor)
    assert result.ndim == 2
    assert result.shape[0] == 1
    assert result.shape[1] == 384


def test_encode_multiple_texts_returns_expected_shape(encoder):
    texts = [
        "The Earth is approximately spherical.",
        "Water boils at 100 degrees Celsius at sea level.",
    ]

    result = encoder.encode(texts)

    assert isinstance(result, torch.Tensor)
    assert result.shape == (2, 384)


def test_embeddings_are_normalized(encoder):
    result = encoder.encode(
        [
            "The Earth is approximately spherical.",
            "The Moon orbits the Earth.",
        ]
    )

    norms = torch.norm(result, dim=1)

    assert torch.allclose(
        norms,
        torch.ones_like(norms),
        atol=1e-5,
    )


def test_empty_input_is_rejected(encoder):
    with pytest.raises(ValueError):
        encoder.encode([])


def test_non_string_input_is_rejected(encoder):
    with pytest.raises(TypeError):
        encoder.encode(["valid evidence", 123])


def test_encode_from_missing_file_is_rejected(encoder, tmp_path):
    missing_file = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        encoder.encode_from_file(missing_file)


def test_encode_from_file_missing_column_is_rejected(
    encoder,
    tmp_path,
):
    csv_file = tmp_path / "evidence.csv"
    csv_file.write_text(
        "id,source\n"
        "E001,NASA\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        encoder.encode_from_file(csv_file)


def test_encode_from_file_with_valid_data(
    encoder,
    tmp_path,
):
    csv_file = tmp_path / "evidence.csv"
    csv_file.write_text(
        "id,text\n"
        "E001,The Earth is approximately spherical.\n"
        "E002,The Moon orbits the Earth.\n",
        encoding="utf-8",
    )

    result = encoder.encode_from_file(csv_file)

    assert isinstance(result, torch.Tensor)
    assert result.shape == (2, 384)


def test_encode_from_file_without_usable_text_is_rejected(
    encoder,
    tmp_path,
):
    csv_file = tmp_path / "evidence.csv"
    csv_file.write_text(
        "id,text\n"
        "E001,\n"
        "E002,\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        encoder.encode_from_file(csv_file)


def test_create_evidence_encoder_returns_encoder():
    encoder = create_evidence_encoder()

    assert isinstance(encoder, EvidenceEncoder)