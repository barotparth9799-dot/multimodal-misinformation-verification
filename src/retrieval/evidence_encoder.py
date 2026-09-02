"""
Evidence encoder for the Multimodal Misinformation Verification project.

This module converts evidence text into normalized semantic embeddings
using a pretrained Sentence Transformer model.
"""

from pathlib import Path

import torch
from sentence_transformers import SentenceTransformer

from configs.config import DEVICE, EMBEDDING_MODEL_NAME


class EvidenceEncoder:
    """
    Encodes evidence statements into semantic vector representations.
    """

    def __init__(
        self,
        model_name: str = EMBEDDING_MODEL_NAME,
        device: str = DEVICE,
    ) -> None:
        self.model_name = model_name
        self.device = device

        self.model = SentenceTransformer(
            self.model_name,
            device=self.device,
        )

    def encode(
        self,
        texts: str | list[str],
    ) -> torch.Tensor:
        """
        Convert one or more evidence statements into embeddings.

        Parameters
        ----------
        texts:
            A single evidence statement or a list of statements.

        Returns
        -------
        torch.Tensor
            Normalized evidence embeddings.
        """

        if isinstance(texts, str):
            texts = [texts]

        if not texts:
            raise ValueError(
                "At least one evidence statement is required."
            )

        if not all(
            isinstance(text, str)
            for text in texts
        ):
            raise TypeError(
                "All evidence inputs must be strings."
            )

        embeddings = self.model.encode(
            texts,
            convert_to_tensor=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        return embeddings.detach().cpu()

    def encode_from_file(
        self,
        file_path: str | Path,
        text_column: str = "text",
    ) -> torch.Tensor:
        """
        Encode evidence text from a CSV file.

        Parameters
        ----------
        file_path:
            Path to the evidence CSV file.

        text_column:
            Name of the column containing evidence text.

        Returns
        -------
        torch.Tensor
            Normalized evidence embeddings.
        """

        import pandas as pd

        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(
                f"Evidence file not found: {file_path}"
            )

        dataframe = pd.read_csv(file_path)

        if text_column not in dataframe.columns:
            raise ValueError(
                f"Required column '{text_column}' "
                "was not found in the evidence file."
            )

        texts = dataframe[text_column].fillna("").tolist()

        if not texts or not any(text.strip() for text in texts):
            raise ValueError(
                "The evidence file contains no usable text."
            )

        return self.encode(texts)


def create_evidence_encoder() -> EvidenceEncoder:
    """
    Create and return an EvidenceEncoder instance.
    """

    return EvidenceEncoder()