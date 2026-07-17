from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Match:
    """Representa un partido de fútbol."""

    home_team: str
    away_team: str

    home_odds: float
    draw_odds: float
    away_odds: float