import pytest
import torch

from src.retrieval.faiss_retriever import FAISSEvidenceRetriever


EVIDENCE_FILE = "data/evidence/evidence.csv"


@pytest.fixture
def retriever():
    return FAISSEvidenceRetriever(EVIDENCE_FILE)


def test_retriever_loads_evidence_file(retriever):
    assert len(retriever.evidence_data) == 11
    assert retriever.index is None


def test_build_index_creates_faiss_index(retriever):
    embeddings = torch.eye(11, dtype=torch.float32)

    retriever.build_index(embeddings)

    assert retriever.index is not None
    assert retriever.embedding_dimension == 11
    assert retriever.index.ntotal == 11


def test_search_returns_requested_number_of_results(retriever):
    embeddings = torch.eye(11, dtype=torch.float32)
    retriever.build_index(embeddings)

    query = embeddings[0]

    results = retriever.search(query, top_k=3)

    assert len(results) == 3
    assert results[0]["evidence_id"] == "E001"


def test_search_returns_expected_metadata(retriever):
    embeddings = torch.eye(11, dtype=torch.float32)
    retriever.build_index(embeddings)

    results = retriever.search(embeddings[0], top_k=1)

    result = results[0]

    assert result["evidence_id"] == "E001"
    assert isinstance(result["text"], str)
    assert isinstance(result["source"], str)
    assert isinstance(result["url"], str)
    assert result["similarity"] == pytest.approx(1.0)


def test_top_k_cannot_exceed_evidence_count(retriever):
    embeddings = torch.eye(11, dtype=torch.float32)
    retriever.build_index(embeddings)

    results = retriever.search(embeddings[0], top_k=100)

    assert len(results) == 11


def test_search_accepts_2d_query_embedding(retriever):
    embeddings = torch.eye(11, dtype=torch.float32)
    retriever.build_index(embeddings)

    results = retriever.search(
        embeddings[0].unsqueeze(0),
        top_k=1,
    )

    assert len(results) == 1
    assert results[0]["evidence_id"] == "E001"


def test_search_requires_built_index(retriever):
    query = torch.ones(11)

    with pytest.raises(RuntimeError):
        retriever.search(query)


def test_build_index_requires_tensor(retriever):
    with pytest.raises(TypeError):
        retriever.build_index([[1.0, 0.0]] * 11)


def test_build_index_requires_2d_tensor(retriever):
    with pytest.raises(ValueError):
        retriever.build_index(torch.ones(11))


def test_build_index_requires_matching_record_count(retriever):
    embeddings = torch.eye(10, dtype=torch.float32)

    with pytest.raises(ValueError):
        retriever.build_index(embeddings)


def test_search_rejects_wrong_dimension(retriever):
    embeddings = torch.eye(11, dtype=torch.float32)
    retriever.build_index(embeddings)

    with pytest.raises(ValueError):
        retriever.search(torch.ones(10), top_k=1)


def test_search_rejects_invalid_top_k(retriever):
    embeddings = torch.eye(11, dtype=torch.float32)
    retriever.build_index(embeddings)

    with pytest.raises(ValueError):
        retriever.search(embeddings[0], top_k=0)


def test_missing_evidence_file_is_rejected():
    with pytest.raises(FileNotFoundError):
        FAISSEvidenceRetriever(
            "data/evidence/does_not_exist.csv"
        )


def test_missing_required_columns_are_rejected(tmp_path):
    csv_file = tmp_path / "invalid_evidence.csv"

    csv_file.write_text(
        "id,text\n"
        "E001,Example evidence\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        FAISSEvidenceRetriever(csv_file)