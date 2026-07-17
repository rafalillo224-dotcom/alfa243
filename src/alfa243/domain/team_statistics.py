from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class TeamStatistics:
    """Estadísticas básicas de rendimiento de un equipo."""

    goals_for: float
    goals_against: float

    def __post_init__(self) -> None:
        if self.goals_for < 0:
            raise ValueError("Los goles a favor no pueden ser negativos.")

        if self.goals_against < 0:
            raise ValueError("Los goles en contra no pueden ser negativos.")