"""
Map verification claims to visual concepts.

The mapper is intentionally conservative: it only assigns a visual topic
when the claim contains recognizable concepts represented by the project's
visual-topic vocabulary.
"""

from dataclasses import dataclass


@dataclass
class ClaimVisualTopic:
    topic: str | None
    confidence: float


class ClaimVisualTopicMapper:
    """Map a claim to one of the supported visual concepts."""

    TOPIC_KEYWORDS = {
        "Earth": (
            "earth",
            "planet earth",
            "our planet",
            "the planet",
        ),
        "Moon": (
            "moon",
            "lunar",
            "natural satellite",
        ),
        "boiling water": (
            "water boils",
            "boiling water",
            "boil water",
            "boils at",
            "boiling point",
            "100 degrees celsius",
        ),
        "red sports car": (
            "sports car",
            "red car",
            "red sports car",
            "car",
            "automobile",
            "vehicle",
        ),
        "industrial pollution": (
            "climate change",
            "global warming",
            "greenhouse gas",
            "greenhouse gases",
            "carbon emissions",
            "industrial pollution",
            "pollution",
            "factory emissions",
        ),
    }

    def map_claim(self, claim: str) -> ClaimVisualTopic:
        """Return the strongest recognized visual topic."""

        if not isinstance(claim, str):
            return ClaimVisualTopic(None, 0.0)

        normalized = claim.lower().strip()

        if not normalized:
            return ClaimVisualTopic(None, 0.0)

        matches: list[tuple[str, int]] = []

        for topic, keywords in self.TOPIC_KEYWORDS.items():
            count = sum(
                1
                for keyword in keywords
                if keyword in normalized
            )

            if count > 0:
                matches.append((topic, count))

        if not matches:
            return ClaimVisualTopic(None, 0.0)

        matches.sort(key=lambda item: item[1], reverse=True)

        topic, count = matches[0]

        confidence = min(1.0, 0.5 + 0.2 * count)

        return ClaimVisualTopic(
            topic=topic,
            confidence=confidence,
        )


def create_claim_visual_topic_mapper() -> ClaimVisualTopicMapper:
    """Create a claim visual-topic mapper."""

    return ClaimVisualTopicMapper()
