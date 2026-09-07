import pytest

from src.text.text_processor import (
    prepare_claim,
    validate_claim,
)
from src.image.image_encoder import ImageEncoder


def test_empty_claim_is_rejected():
    assert validate_claim("") is False

    with pytest.raises(ValueError):
        prepare_claim("")


def test_short_claim_is_rejected():
    assert validate_claim("ab") is False

    with pytest.raises(ValueError):
        prepare_claim("ab")


def test_whitespace_only_claim_is_rejected():
    assert validate_claim("   ") is False

    with pytest.raises(ValueError):
        prepare_claim("   ")


def test_non_string_claim_is_rejected():
    assert validate_claim(123) is False

    with pytest.raises(TypeError):
        prepare_claim(123)


def test_missing_image_is_rejected():
    encoder = ImageEncoder.__new__(ImageEncoder)

    with pytest.raises(FileNotFoundError):
        encoder.load_image("sample_media/nonexistent_image.jpg")