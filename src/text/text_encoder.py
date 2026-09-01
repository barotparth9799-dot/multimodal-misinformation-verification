"""
Transformer-based text encoder for the Multimodal Misinformation
Verification project.
"""

import torch
from transformers import AutoModel, AutoTokenizer

from configs.config import DEVICE, TEXT_MODEL_NAME


class TextEncoder:
    """
    Encodes text claims into dense vector representations using
    a pretrained transformer model.
    """

    def __init__(
        self,
        model_name: str = TEXT_MODEL_NAME,
        device: str = DEVICE,
    ) -> None:
        self.model_name = model_name
        self.device = torch.device(device)

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name
        )

        self.model = AutoModel.from_pretrained(
            self.model_name
        )

        self.model.to(self.device)
        self.model.eval()

    @staticmethod
    def mean_pooling(
        model_output: torch.Tensor,
        attention_mask: torch.Tensor,
    ) -> torch.Tensor:
        """
        Apply attention-mask-aware mean pooling to token embeddings.
        """

        token_embeddings = model_output.last_hidden_state

        input_mask_expanded = (
            attention_mask
            .unsqueeze(-1)
            .expand(token_embeddings.size())
            .float()
        )

        sum_embeddings = torch.sum(
            token_embeddings * input_mask_expanded,
            dim=1,
        )

        sum_mask = torch.clamp(
            input_mask_expanded.sum(dim=1),
            min=1e-9,
        )

        return sum_embeddings / sum_mask

    def encode(
        self,
        texts: str | list[str],
        max_length: int = 256,
    ) -> torch.Tensor:
        """
        Convert one or more text claims into dense embeddings.

        Parameters
        ----------
        texts:
            A single claim or a list of claims.
        max_length:
            Maximum number of tokens processed per claim.

        Returns
        -------
        torch.Tensor
            Tensor containing one embedding per input claim.
        """

        if isinstance(texts, str):
            texts = [texts]

        if not texts:
            raise ValueError("At least one text claim is required.")

        if not all(isinstance(text, str) for text in texts):
            raise TypeError("All text inputs must be strings.")

        encoded_inputs = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=max_length,
            return_tensors="pt",
        )

        encoded_inputs = {
            key: value.to(self.device)
            for key, value in encoded_inputs.items()
        }

        with torch.no_grad():
            model_output = self.model(**encoded_inputs)

        embeddings = self.mean_pooling(
            model_output,
            encoded_inputs["attention_mask"],
        )

        embeddings = torch.nn.functional.normalize(
            embeddings,
            p=2,
            dim=1,
        )

        return embeddings.cpu()

    def encode_single(
        self,
        text: str,
        max_length: int = 256,
    ) -> torch.Tensor:
        """
        Encode a single claim and return one embedding vector.
        """

        embeddings = self.encode(
            text,
            max_length=max_length,
        )

        return embeddings[0]


def create_text_encoder() -> TextEncoder:
    """
    Create and return a TextEncoder instance.
    """

    return TextEncoder()