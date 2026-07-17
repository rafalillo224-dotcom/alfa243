from dataclasses import dataclass
from datetime import date


@dataclass(slots=True, frozen=True)
class MatchData:
    """Representa un partido dentro de una competición y temporada."""

    competition: str
    season: str
    round_number: int
    kickoff: date
    home_team: str
    away_team: str
    home_odds: float
    draw_odds: float
    away_odds: float

    def __post_init__(self) -> None:
        if not self.competition.strip():
            raise ValueError("La competición no puede estar vacía.")

        if not self.season.strip():
            raise ValueError("La temporada no puede estar vacía.")

        if self.round_number <= 0:
            raise ValueError("La jornada debe ser mayor que cero.")

        if not self.home_team.strip():
            raise ValueError("El equipo local no puede estar vacío.")

        if not self.away_team.strip():
            raise ValueError("El equipo visitante no puede estar vacío.")

        if self.home_team.casefold() == self.away_team.casefold():
            raise ValueError(
                "El equipo local y visitante deben ser distintos."
            )

        odds = (
            self.home_odds,
            self.draw_odds,
            self.away_odds,
        )

        if any(odd <= 1.0 for odd in odds):
            raise ValueError("Todas las cuotas deben ser mayores que 1.0.")