from dataclasses import dataclass

from alfa243.domain.alfa_selection import AlfaSelection
from alfa243.domain.combination_portfolio import CombinationPortfolio
from alfa243.domain.match_analysis import MatchAnalysis


@dataclass(slots=True, frozen=True)
class Alfa243Result:
    """Resultado completo de ejecutar el sistema ALFA-243."""

    competition: str
    season: str
    round_number: int
    match_analyses: tuple[MatchAnalysis, ...]
    selection: AlfaSelection
    portfolio: CombinationPortfolio
    valid_pattern_count: int

    def __post_init__(self) -> None:
        if not self.competition.strip():
            raise ValueError(
                "La competición no puede estar vacía."
            )

        if not self.season.strip():
            raise ValueError(
                "La temporada no puede estar vacía."
            )

        if self.round_number <= 0:
            raise ValueError(
                "El número de jornada debe ser positivo."
            )

        if not self.match_analyses:
            raise ValueError(
                "El resultado debe contener análisis de partidos."
            )

        if self.valid_pattern_count <= 0:
            raise ValueError(
                "El número de patrones válidos debe ser positivo."
            )

    @property
    def analyzed_match_count(self) -> int:
        return len(self.match_analyses)

    @property
    def selected_combination_count(self) -> int:
        return self.portfolio.combination_count

    @property
    def coverage_percent(self) -> float:
        return self.portfolio.coverage_percent