from dataclasses import dataclass

from alfa243.domain.match_analysis import MatchAnalysis
from alfa243.domain.match_category import MatchCategory


@dataclass(slots=True, frozen=True)
class ClassifiedMatch:
    """Resultado de clasificar un partido analizado."""

    analysis: MatchAnalysis
    category: MatchCategory
    selected_outcome: str
    selected_probability: float
    probability_gap: float

    def __post_init__(self) -> None:
        valid_outcomes = {"1", "X", "2"}

        if self.selected_outcome not in valid_outcomes:
            raise ValueError(
                "El resultado seleccionado debe ser 1, X o 2."
            )

        if not 0.0 <= self.selected_probability <= 1.0:
            raise ValueError(
                "La probabilidad seleccionada debe estar entre 0 y 1."
            )

        if not 0.0 <= self.probability_gap <= 1.0:
            raise ValueError(
                "La diferencia de probabilidades debe estar entre 0 y 1."
            )