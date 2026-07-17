from dataclasses import dataclass

from alfa243.domain.classified_match import ClassifiedMatch


@dataclass(slots=True, frozen=True)
class CombinationPick:
    """Pronóstico elegido para un partido de una combinación."""

    classified_match: ClassifiedMatch
    outcome: str
    probability: float
    is_fixed: bool

    def __post_init__(self) -> None:
        if self.outcome not in {"1", "X", "2"}:
            raise ValueError(
                "El resultado debe ser 1, X o 2."
            )

        if not 0.0 <= self.probability <= 1.0:
            raise ValueError(
                "La probabilidad debe estar entre 0 y 1."
            )

    @property
    def match(self):
        return self.classified_match.analysis.match