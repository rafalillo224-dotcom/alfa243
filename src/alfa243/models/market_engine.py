from dataclasses import dataclass

from alfa243.domain.match import Match


@dataclass(slots=True)
class MarketProbabilities:
    home: float
    draw: float
    away: float
    overround: float


class MarketEngine:
    """Calcula probabilidades ajustadas a partir de cuotas."""

    @staticmethod
    def calculate(match: Match) -> MarketProbabilities:
        home_raw = 1 / match.home_odds
        draw_raw = 1 / match.draw_odds
        away_raw = 1 / match.away_odds

        overround = home_raw + draw_raw + away_raw

        return MarketProbabilities(
            home=home_raw / overround,
            draw=draw_raw / overround,
            away=away_raw / overround,
            overround=overround,
        )