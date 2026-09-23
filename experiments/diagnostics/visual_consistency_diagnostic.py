from src.image.visual_consistency import VisualConsistencyChecker

checker = VisualConsistencyChecker()

tests = [
    (
        "The Moon is Earth's only natural satellite.",
        "sample_media/moon_test.jpg",
    ),
    (
        "The Moon is Earth's only natural satellite.",
        "sample_media/earth_test.jpg",
    ),
]

for claim, image in tests:
    result = checker.check(claim, image)
    print()
    print("CLAIM:", claim)
    print("IMAGE:", image)
    print(result)
