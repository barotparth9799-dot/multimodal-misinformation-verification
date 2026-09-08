from src.text.claim_decomposer import ClaimDecomposer


def test_decomposes_moon_compound_claim():
    decomposer = ClaimDecomposer()

    result = decomposer.decompose(
        "The Moon is a planet and Earth's only natural satellite."
    )

    assert result.is_compound is True
    assert result.claims == [
        "The Moon is a planet",
        "The Moon is Earth's only natural satellite",
    ]


def test_decomposes_pronoun_compound_claim():
    decomposer = ClaimDecomposer()

    result = decomposer.decompose(
        "The Moon is Earth's only natural satellite and it is larger than the Earth."
    )

    assert result.is_compound is True
    assert result.claims == [
        "The Moon is Earth's only natural satellite",
        "The Moon is larger than the Earth",
    ]


def test_keeps_simple_claim_intact():
    decomposer = ClaimDecomposer()

    result = decomposer.decompose("The Earth is a planet.")

    assert result.is_compound is False
    assert result.claims == ["The Earth is a planet."]