import open_clip
import torch
from PIL import Image

model, _, preprocess = open_clip.create_model_and_transforms(
    "ViT-B-32",
    pretrained="openai",
)

tokenizer = open_clip.get_tokenizer("ViT-B-32")
model.eval()

labels = [
    "Earth",
    "the Moon",
    "boiling water",
    "a red sports car",
    "industrial pollution",
]

images = [
    "sample_media/earth_test.jpg",
    "sample_media/moon_test.jpg",
    "sample_media/boiling_water_test.jpg",
    "sample_media/test 2.png",
    "sample_media/climate_test.png",
]

with torch.no_grad():
    text = tokenizer([f"a photo of {label}" for label in labels])
    text_features = model.encode_text(text)
    text_features = text_features / text_features.norm(dim=-1, keepdim=True)

    for image_path in images:
        image = preprocess(
            Image.open(image_path).convert("RGB")
        ).unsqueeze(0)

        image_features = model.encode_image(image)
        image_features = image_features / image_features.norm(
            dim=-1,
            keepdim=True,
        )

        similarities = (image_features @ text_features.T)[0]

        ranked = sorted(
            zip(labels, similarities.tolist()),
            key=lambda x: x[1],
            reverse=True,
        )

        print()
        print("=" * 60)
        print("IMAGE:", image_path)

        for label, score in ranked:
            print(f"{label:25s} {score:.4f}")

        print("PREDICTED:", ranked[0][0])
