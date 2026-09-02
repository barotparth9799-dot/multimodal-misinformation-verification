"""
FAISS-based evidence retrieval for the Multimodal Misinformation
Verification project.

This module builds a semantic search index over evidence embeddings
and retrieves the most relevant evidence for a given query embedding.
"""

from pathlib import Path

import faiss
import numpy as np
import pandas as pd
import torch


class FAISSEvidenceRetriever:
    """
    Semantic evidence retriever using FAISS inner-product search.
    
    Evidence embeddings are expected to be L2-normalized so that
    inner product is equivalent to cosine similarity.
    """

    def __init__(
        self,
        evidence_file: str | Path,
    ) -> None:
        self.evidence_file = Path(evidence_file)

        if not self.evidence_file.exists():
            raise FileNotFoundError(
                f"Evidence file not found: {self.evidence_file}"
            )

        self.evidence_data = pd.read_csv(
            self.evidence_file
        )

        required_columns = {
            "evidence_id",
            "text",
            "source",
            "url",
        }

        missing_columns = (
            required_columns
            - set(self.evidence_data.columns)
        )

        if missing_columns:
            raise ValueError(
                "Missing required evidence columns: "
                f"{sorted(missing_columns)}"
            )

        self.index = None
        self.embedding_dimension = None

    def build_index(
        self,
        embeddings: torch.Tensor,
    ) -> None:
        """
        Build a FAISS index from normalized evidence embeddings.

        Parameters
        ----------
        embeddings:
            Evidence embeddings with shape
            (number_of_records, embedding_dimension).
        """

        if not isinstance(embeddings, torch.Tensor):
            raise TypeError(
                "embeddings must be a torch.Tensor."
            )

        if embeddings.ndim != 2:
            raise ValueError(
                "embeddings must be a 2-dimensional tensor."
            )

        if embeddings.shape[0] != len(
            self.evidence_data
        ):
            raise ValueError(
                "Number of embeddings must match the "
                "number of evidence records."
            )

        embeddings_array = (
            embeddings.detach()
            .cpu()
            .numpy()
            .astype("float32")
        )

        self.embedding_dimension = embeddings_array.shape[1]

        self.index = faiss.IndexFlatIP(
            self.embedding_dimension
        )

        self.index.add(embeddings_array)

    def search(
        self,
        query_embedding: torch.Tensor,
        top_k: int = 3,
    ) -> list[dict]:
        """
        Retrieve the most relevant evidence for a query embedding.

        Parameters
        ----------
        query_embedding:
            A normalized query embedding.

        top_k:
            Number of evidence records to retrieve.

        Returns
        -------
        list[dict]
            Retrieved evidence records with similarity scores.
        """

        if self.index is None:
            raise RuntimeError(
                "FAISS index has not been built. "
                "Call build_index() first."
            )

        if not isinstance(
            query_embedding,
            torch.Tensor,
        ):
            raise TypeError(
                "query_embedding must be a torch.Tensor."
            )

        if query_embedding.ndim == 1:
            query_embedding = query_embedding.unsqueeze(0)

        if query_embedding.ndim != 2:
            raise ValueError(
                "query_embedding must be a 1D or 2D tensor."
            )

        if query_embedding.shape[1] != (
            self.embedding_dimension
        ):
            raise ValueError(
                "Query embedding dimension does not "
                "match the FAISS index dimension."
            )

        if top_k < 1:
            raise ValueError(
                "top_k must be at least 1."
            )

        top_k = min(
            top_k,
            len(self.evidence_data),
        )

        query_array = (
            query_embedding.detach()
            .cpu()
            .numpy()
            .astype("float32")
        )

        scores, indices = self.index.search(
            query_array,
            top_k,
        )

        results = []

        for score, index_position in zip(
            scores[0],
            indices[0],
        ):
            if index_position < 0:
                continue

            row = self.evidence_data.iloc[
                int(index_position)
            ]

            results.append(
                {
                    "evidence_id": str(
                        row["evidence_id"]
                    ),
                    "text": str(row["text"]),
                    "source": str(row["source"]),
                    "url": str(row["url"]),
                    "similarity": float(score),
                }
            )

        return results