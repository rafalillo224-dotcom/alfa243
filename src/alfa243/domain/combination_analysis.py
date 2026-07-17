from dataclasses import dataclass
from math import inf

from alfa243.domain.alfa_combination import AlfaCombination


@dataclass(slots=True, frozen=True)
class CombinationAnalysis:
    """Métricas calculadas para una combinación ALFA-243."""

    rank: int
    combination: AlfaCombination
    cumulative_probability: float
    cumulative_coverage: float

    def __post_init__(self) -> None:
        if self.rank <= 0:
            raise ValueError(
                "El ranking debe ser un número positivo."
            )

        if self.cumulative_probability < 0.0:
            raise ValueError(
                "La probabilidad acumulada no puede ser negativa."
            )

        if not 0.0 <= self.cumulative_coverage <= 1.0:
            raise ValueError(
                "La cobertura acumulada debe estar entre 0 y 1."
            )

    @property
    def probability(self) -> float:
        return self.combination.probability

    @property
    def probability_percent(self) -> float:
        return self.probability * 100.0

    @property
    def fair_odds(self) -> float:
        if self.probability == 0.0:
            return inf

        return 1.0 / self.probability

    @property
    def home_count(self) -> int:
        return sum(
            pick.outcome == "1"
            for pick in self.combination.all_picks
        )

    @property
    def draw_count(self) -> int:
        return sum(
            pick.outcome == "X"
            for pick in self.combination.all_picks
        )

    @property
    def away_count(self) -> int:
        return sum(
            pick.outcome == "2"
            for pick in self.combination.all_picks
        )

    @property
    def code(self) -> str:
        return self.combination.code