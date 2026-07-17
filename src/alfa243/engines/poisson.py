from math import exp, factorial

from alfa243.domain.prediction import Prediction
from alfa243.domain.score_probability import ScoreProbability
from alfa243.engines.base import BaseEngine


class PoissonEngine(BaseEngine):
    """Motor de distribución de Poisson."""

    def predict(
        self,
        home_expected_goals: float,
        away_expected_goals: float,
    ) -> Prediction:

        matrix = self.score_matrix(
            home_expected_goals,
            away_expected_goals,
        )

        home = sum(
            score.probability
            for score in matrix
            if score.home_goals > score.away_goals
        )

        draw = sum(
            score.probability
            for score in matrix
            if score.home_goals == score.away_goals
        )

        away = sum(
            score.probability
            for score in matrix
            if score.home_goals < score.away_goals
        )

        return Prediction(
            source="poisson",
            home=home,
            draw=draw,
            away=away,
            confidence=0.75,
        )

    @staticmethod
    def probability(expected_goals: float, goals: int) -> float:
        return (
            exp(-expected_goals)
            * (expected_goals ** goals)
            / factorial(goals)
        )

    @staticmethod
    def distribution(
        expected_goals: float,
        max_goals: int = 10,
    ) -> list[float]:
        return [
            PoissonEngine.probability(expected_goals, goals)
            for goals in range(max_goals + 1)
        ]

    @staticmethod
    def score_matrix(
        home_expected_goals: float,
        away_expected_goals: float,
        max_goals: int = 10,
    ) -> list[ScoreProbability]:

        home_distribution = PoissonEngine.distribution(
            home_expected_goals,
            max_goals,
        )

        away_distribution = PoissonEngine.distribution(
            away_expected_goals,
            max_goals,
        )

        matrix: list[ScoreProbability] = []

        for home_goals, home_probability in enumerate(home_distribution):
            for away_goals, away_probability in enumerate(away_distribution):
                matrix.append(
                    ScoreProbability(
                        home_goals=home_goals,
                        away_goals=away_goals,
                        probability=home_probability * away_probability,
                    )
                )

        return matrix