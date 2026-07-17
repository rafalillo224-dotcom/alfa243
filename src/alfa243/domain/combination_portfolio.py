from dataclasses import dataclass

from alfa243.domain.combination_analysis import CombinationAnalysis


@dataclass(slots=True, frozen=True)
class CombinationPortfolio:
    """Resumen de las combinaciones seleccionadas por ALFA-243."""

    analyses: tuple[CombinationAnalysis, ...]
    selected_probability: float
    valid_universe_probability: float

    def __post_init__(self) -> None:
        if not self.analyses:
            raise ValueError(
                "El portfolio debe contener combinaciones."
            )

        if self.selected_probability < 0.0:
            raise ValueError(
                "La probabilidad seleccionada no puede ser negativa."
            )

        if self.valid_universe_probability < 0.0:
            raise ValueError(
                "La probabilidad del universo no puede ser negativa."
            )

        if (
            self.selected_probability
            > self.valid_universe_probability + 1e-12
        ):
            raise ValueError(
                "La probabilidad seleccionada no puede superar "
                "la probabilidad del universo válido."
            )

    @property
    def combination_count(self) -> int:
        return len(self.analyses)

    @property
    def coverage_ratio(self) -> float:
        if self.valid_universe_probability == 0.0:
            return 0.0

        return (
            self.selected_probability
            / self.valid_universe_probability
        )

    @property
    def coverage_percent(self) -> float:
        return self.coverage_ratio * 100.0