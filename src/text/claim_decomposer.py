from dataclasses import dataclass
import re


@dataclass
class ClaimDecomposition:
    claims: list[str]
    is_compound: bool


class ClaimDecomposer:
    """Split compound claims into independently testable statements."""

    CONJUNCTION_PATTERN = re.compile(
        r"\s+(and|but|while)\s+",
        flags=re.IGNORECASE,
    )

    def decompose(self, claim: str) -> ClaimDecomposition:
        if not isinstance(claim, str):
            raise TypeError("claim must be a string.")

        cleaned = claim.strip()

        if not cleaned:
            return ClaimDecomposition(
                claims=[],
                is_compound=False,
            )

        parts = self.CONJUNCTION_PATTERN.split(cleaned)

        if len(parts) == 1:
            return ClaimDecomposition(
                claims=[cleaned],
                is_compound=False,
            )

        first_part = parts[0].strip(" ,.;:")
        subject_match = re.match(
            r"^(.*?)\s+is\s+",
            first_part,
            flags=re.IGNORECASE,
        )

        subject = subject_match.group(1).strip() if subject_match else ""

        claims = [first_part]

        for part in parts[2::2]:
            part = part.strip(" ,.;:")

            if not part:
                continue

            if re.match(r"^it\s+is\s+", part, flags=re.IGNORECASE):
                remainder = re.sub(
                    r"^it\s+is\s+",
                    "",
                    part,
                    flags=re.IGNORECASE,
                )
                if subject:
                    part = f"{subject} is {remainder}"

            elif subject and not re.match(
                r"^(the|a|an)\s+",
                part,
                flags=re.IGNORECASE,
            ):
                part = f"{subject} is {part}"

            claims.append(part)

        return ClaimDecomposition(
            claims=claims,
            is_compound=len(claims) > 1,
        )


def create_claim_decomposer() -> ClaimDecomposer:
    return ClaimDecomposer()