"""
Image and OpenCLIP text encoder for the Multimodal Misinformation
Verification project.

This module uses OpenCLIP to convert images and text into normalized
feature embeddings in the same shared multimodal embedding space.
"""

from pathlib import Path

import torch
from PIL import Image
import open_clip

from configs.config import (
    DEVICE,
    IMAGE_TEXT_MODEL_NAME,
    IMAGE_TEXT_PRETRAINED,
)


class ImageEncoder:
    """
    Encodes images and text using a pretrained OpenCLIP model.
    """

    def __init__(
        self,
        model_name: str = IMAGE_TEXT_MODEL_NAME,
        pretrained: str = IMAGE_TEXT_PRETRAINED,
        device: str = DEVICE,
    ) -> None:
        self.model_name = model_name
        self.pretrained = pretrained
        self.device = torch.device(device)

        self.model, _, self.preprocess = (
            open_clip.create_model_and_transforms(
                self.model_name,
                pretrained=self.pretrained,
            )
        )

        self.tokenizer = open_clip.get_tokenizer(
            self.model_name
        )

        self.model.to(self.device)
        self.model.eval()

    def load_image(
        self,
        image_path: str | Path,
    ) -> Image.Image:
        """
        Load an image from disk and convert it to RGB.
        """

        image_path = Path(image_path)

        if not image_path.exists():
            raise FileNotFoundError(
                f"Image not found: {image_path}"
            )

        try:
            image = Image.open(image_path).convert("RGB")
        except Exception as exc:
            raise ValueError(
                f"Unable to open image: {image_path}"
            ) from exc

        return image

    def encode(
        self,
        image: Image.Image,
    ) -> torch.Tensor:
        """
        Convert a PIL image into a normalized OpenCLIP
        image embedding.
        """

        if not isinstance(image, Image.Image):
            raise TypeError(
                "image must be a PIL.Image.Image object."
            )

        image_tensor = self.preprocess(
            image
        ).unsqueeze(0)

        image_tensor = image_tensor.to(
            self.device
        )

        with torch.no_grad():
            image_features = self.model.encode_image(
                image_tensor
            )

        image_features = image_features.float()

        image_features = torch.nn.functional.normalize(
            image_features,
            p=2,
            dim=-1,
        )

        return image_features.cpu()

    def encode_from_path(
        self,
        image_path: str | Path,
    ) -> torch.Tensor:
        """
        Load an image from a path and encode it.
        """

        image = self.load_image(image_path)

        return self.encode(image)

    def encode_batch(
        self,
        images: list[Image.Image],
    ) -> torch.Tensor:
        """
        Encode multiple PIL images as a batch.
        """

        if not images:
            raise ValueError(
                "At least one image is required."
            )

        if not all(
            isinstance(image, Image.Image)
            for image in images
        ):
            raise TypeError(
                "All inputs must be PIL.Image.Image objects."
            )

        image_tensors = torch.stack(
            [
                self.preprocess(image)
                for image in images
            ]
        )

        image_tensors = image_tensors.to(
            self.device
        )

        with torch.no_grad():
            image_features = self.model.encode_image(
                image_tensors
            )

        image_features = image_features.float()

        image_features = torch.nn.functional.normalize(
            image_features,
            p=2,
            dim=-1,
        )

        return image_features.cpu()

    def encode_text(
        self,
        texts: str | list[str],
    ) -> torch.Tensor:
        """
        Convert text into normalized OpenCLIP text embeddings.

        These embeddings are in the same shared space as the
        OpenCLIP image embeddings and can therefore be compared
        directly for text-image consistency.
        """

        if isinstance(texts, str):
            texts = [texts]

        if not texts:
            raise ValueError(
                "At least one text input is required."
            )

        if not all(
            isinstance(text, str)
            for text in texts
        ):
            raise TypeError(
                "All text inputs must be strings."
            )

        tokens = self.tokenizer(
            texts
        ).to(self.device)

        with torch.no_grad():
            text_features = self.model.encode_text(
                tokens
            )

        text_features = text_features.float()

        text_features = torch.nn.functional.normalize(
            text_features,
            p=2,
            dim=-1,
        )

        return text_features.cpu()


def create_image_encoder() -> ImageEncoder:
    """
    Create and return an ImageEncoder instance.
    """

    return ImageEncoder()