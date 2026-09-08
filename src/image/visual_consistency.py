"""
Claim-image visual consistency decision logic.

Combines the claim's expected visual topic with the image's detected
visual topic. This signal is used only for multimodal consistency,
not as a standalone truth detector.
"""

from dataclasses import dataclass

from src.image.claim_visual_topic_mapper import (
    ClaimVisualTopic,
    ClaimVisualTopicMapper,
)
from src.image.visual_topic_analyzer import (
    VisualTopicAnalyzer,
    VisualTopicResult,
)


@dataclass
class VisualConsistencyResult:
    claim_topic: str | None
    claim_topic_confidence: float
    image_topic: str
    image_topic_score: float
    image_topic_margin: float
    is_consistent: bool | None
    consistency_score: float


class VisualConsistencyChecker:
    """Compare the visual topic expected by a claim with the image topic."""

    def __init__(
        self,
        topic_mapper: ClaimVisualTopicMapper | None = None,
        topic_analyzer: VisualTopicAnalyzer | None = None,
    ) -> None:
        self.topic_mapper = topic_mapper or ClaimVisualTopicMapper()
        self.topic_analyzer = topic_analyzer or VisualTopicAnalyzer()

    def check(
        self,
        claim: str,
        image_path: str,
    ) -> VisualConsistencyResult:
        claim_topic: ClaimVisualTopic = self.topic_mapper.map_claim(claim)
        image_result: VisualTopicResult = self.topic_analyzer.analyze(
            image_path
        )

        if claim_topic.topic is None:
            return VisualConsistencyResult(
                claim_topic=None,
                claim_topic_confidence=0.0,
                image_topic=image_result.top_topic,
                image_topic_score=image_result.top_score,
                image_topic_margin=image_result.margin,
                is_consistent=None,
                consistency_score=0.5,
            )

        if claim_topic.topic == image_result.top_topic:
            consistency_score = min(
                1.0,
                0.5
                + 0.5
                * image_result.margin
                / 0.10,
            )
            is_consistent = True
        else:
            consistency_score = max(
                0.0,
                0.5
                - 0.5
                * image_result.margin
                / 0.10,
            )
            is_consistent = False

        return VisualConsistencyResult(
            claim_topic=claim_topic.topic,
            claim_topic_confidence=claim_topic.confidence,
            image_topic=image_result.top_topic,
            image_topic_score=image_result.top_score,
            image_topic_margin=image_result.margin,
            is_consistent=is_consistent,
            consistency_score=consistency_score,
        )


def create_visual_consistency_checker() -> VisualConsistencyChecker:
    """Create a visual consistency checker."""

    return VisualConsistencyChecker()
