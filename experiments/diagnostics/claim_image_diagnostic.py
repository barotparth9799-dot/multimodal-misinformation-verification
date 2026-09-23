import open_clip
import torch
from PIL import Image

model, _, preprocess = open_clip.create_model_and_transforms(
    "ViT-B-32",
    pretrained="openai",
)

tokenizer = open_clip.get_tokenizer("ViT-B-32")
model.eval()

tests = [
    ("Moon claim + Moon image",
     "The Moon is Earth's only natural satellite.",
     "sample_media/moon_test.jpg"),

    ("Moon claim + Earth image",
     "The Moon is Earth's only natural satellite.",
     "sample_media/earth_test.jpg"),

    ("Climate claim + climate image",
     "Climate change refers to long-term shifts in temperatures and weather patterns, mainly caused by human activities.",
     "sample_media/climate_test.png"),

    ("Climate claim + Earth image",
     "Climate change refers to long-term shifts in temperatures and weather patterns, mainly caused by human activities.",
     "sample_media/earth_test.jpg"),

    ("Water claim + boiling image",
     "Water boils at approximately 100 degrees Celsius at standard atmospheric pressure.",
     "sample_media/boiling_water_test.jpg"),

    ("Water claim + Earth image",
     "Water boils at approximately 100 degrees Celsius at standard atmospheric pressure.",
     "sample_media/earth_test.jpg"),
]

visual_prompts = [
    "a photo of Earth",
    "a photo of the Moon",
    "a photo of boiling water",
    "a photo of a red sports car",
    "a photo of industrial pollution",
]

with torch.no_grad():
    text = tokenizer(visual_prompts)
    text_features = model.encode_text(text)
    text_features = text_features / text_features.norm(dim=-1, keepdim=True)

    for name, claim, image_path in tests:
        image = preprocess(
            Image.open(image_path).convert("RGB")
        ).unsqueeze(0)

        image_features = model.encode_image(image)
        image_features = image_features / image_features.norm(
            dim=-1,
            keepdim=True,
        )

        scores = (image_features @ text_features.T)[0]

        ranked = sorted(
            zip(visual_prompts, scores.tolist()),
            key=lambda x: x[1],
            reverse=True,
        )

        print()
        print("=" * 70)
        print(name)
        print("Claim:", claim)
        print("Image:", image_path)

        for prompt, score in ranked:
            print(f"{prompt:35s} {score:.4f}")

        print("TOP VISUAL:", ranked[0][0])
