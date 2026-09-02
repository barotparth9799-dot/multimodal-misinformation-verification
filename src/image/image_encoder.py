"""
Image encoder for the Multimodal Misinformation Verification project.

This module uses OpenCLIP to convert images into normalized feature
embeddings that can be compared with text embeddings.
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
    Encodes images using a pretrained OpenCLIP vision model.
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

        self.model, _, self.preprocess = open_clip.create_model_and_transforms(
            self.model_name,
            pretrained=self.pretrained,
        )

        self.model.to(self.device)
        self.model.eval()

    def load_image(self, image_path: str | Path) -> Image.Image:
        """
        Load an image from disk and convert it to RGB.

        Parameters
        ----------
        image_path:
            Path to the image file.

        Returns
        -------
        PIL.Image.Image
            RGB image.

        Raises
        ------
        FileNotFoundError
            If the image does not exist.
        ValueError
            If the file cannot be opened as an image.
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
        Convert a PIL image into a normalized image embedding.

        Parameters
        ----------
        image:
            RGB PIL image.

        Returns
        -------
        torch.Tensor
            Normalized image embedding.
        """

        if not isinstance(image, Image.Image):
            raise TypeError(
                "image must be a PIL.Image.Image object."
            )

        image_tensor = self.preprocess(image).unsqueeze(0)
        image_tensor = image_tensor.to(self.device)

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

        Parameters
        ----------
        images:
            List of RGB PIL images.

        Returns
        -------
        torch.Tensor
            Normalized image embeddings.
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

        image_tensors = image_tensors.to(self.device)

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


def create_image_encoder() -> ImageEncoder:
    """
    Create and return an ImageEncoder instance.
    """

    return ImageEncoder()