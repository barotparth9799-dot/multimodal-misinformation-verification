import pytest

from src.text.text_processor import (
    clean_text,
    get_text_statistics,
    prepare_claim,
    validate_claim,
)


def test_clean_text_removes_extra_whitespace():
    text = "  Climate    change   is real.  "

    result = clean_text(text)

    assert result == "Climate change is real."


def test_validate_claim_accepts_valid_claim():
    assert validate_claim("Climate change is real.") is True


def test_validate_claim_rejects_empty_claim():
    assert validate_claim("") is False


def test_prepare_claim_returns_clean_text():
    result = prepare_claim("  Climate    change is real.  ")

    assert result == "Climate change is real."


def test_get_text_statistics_returns_expected_values():
    result = get_text_statistics("Climate change is real.")

    assert result["character_count"] > 0
    assert result["word_count"] == 4
    assert result["sentence_count"] >= 1