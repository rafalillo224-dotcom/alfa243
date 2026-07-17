from dataclasses import dataclass

from alfa243.domain.match_data import MatchData
from alfa243.domain.prediction import Prediction
from alfa243.domain.score_probability import ScoreProbability


@dataclass(slots=True, frozen=True)
class MatchAnalysis:
    """Resultado completo del análisis de un partido."""

    match: MatchData
    home_expected_goals: float
    away_expected_goals: float
    market_prediction: Prediction
    poisson_prediction: Prediction
    fusion_prediction: Prediction
    btts: float
    over_25: float
    under_25: float
    top_scores: tuple[ScoreProbability, ...]

    @property
    def most_likely_score(self) -> ScoreProbability:
        if not self.top_scores:
            raise ValueError(
                "El análisis no contiene marcadores probables."
            )

        return self.top_scores[0]