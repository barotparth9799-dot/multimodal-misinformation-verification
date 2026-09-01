"""
Text processing utilities for the Multimodal Misinformation Verification project.

This module handles basic claim cleaning and text preparation before the
claim is passed to transformer-based models.
"""

import re
from typing import Optional


def clean_text(text: str) -> str:
    """
    Clean and normalize a text claim.

    Parameters
    ----------
    text:
        Raw claim text.

    Returns
    -------
    str
        Cleaned claim text.
    """

    if not isinstance(text, str):
        raise TypeError("text must be a string.")

    # Remove leading and trailing whitespace.
    text = text.strip()

    # Replace multiple whitespace characters with a single space.
    text = re.sub(r"\s+", " ", text)

    # Remove control characters while preserving normal punctuation.
    text = "".join(
        character
        for character in text
        if character.isprintable()
    )

    return text.strip()


def validate_claim(text: str) -> bool:
    """
    Check whether a claim contains usable text.

    Parameters
    ----------
    text:
        Claim text to validate.

    Returns
    -------
    bool
        True if the claim is valid, otherwise False.
    """

    if not isinstance(text, str):
        return False

    cleaned_text = clean_text(text)

    return len(cleaned_text) >= 3


def prepare_claim(text: str) -> str:
    """
    Clean and validate a claim before model processing.

    Parameters
    ----------
    text:
        Raw claim text.

    Returns
    -------
    str
        Prepared claim.

    Raises
    ------
    ValueError
        If the claim is empty or too short.
    """

    cleaned_text = clean_text(text)

    if not validate_claim(cleaned_text):
        raise ValueError(
            "Claim must contain at least 3 usable characters."
        )

    return cleaned_text


def get_text_statistics(text: str) -> dict:
    """
    Calculate basic statistics for a claim.

    Parameters
    ----------
    text:
        Claim text.

    Returns
    -------
    dict
        Basic text statistics.
    """

    cleaned_text = clean_text(text)

    words = cleaned_text.split()

    return {
        "character_count": len(cleaned_text),
        "word_count": len(words),
        "sentence_count": max(
            1,
            len(re.findall(r"[.!?]+", cleaned_text)),
        ),
    }