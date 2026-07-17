from alfa243.domain.match import Match
from alfa243.domain.prediction import Prediction


class MarketEngine:
    """Calcula probabilidades implícitas ajustadas del mercado."""

    @staticmethod
    def calculate(match: Match) -> Prediction:
        home = 1 / match.home_odds
        draw = 1 / match.draw_odds
        away = 1 / match.away_odds

        total = home + draw + away

        return Prediction(
            source="market",
            home=home / total,
            draw=draw / total,
            away=away / total,
            confidence=1.0,
        )