from math import exp, factorial

from alfa243.domain.prediction import Prediction
from alfa243.domain.score_probability import ScoreProbability


class PoissonEngine:
    """Motor de predicción basado en la distribución de Poisson."""

    @staticmethod
    def probability(
        expected_goals: float,
        goals: int,
    ) -> float:
        return (
            exp(-expected_goals)
            * expected_goals**goals
            / factorial(goals)
        )

    @classmethod
    def distribution(
        cls,
        expected_goals: float,
        max_goals: int = 10,
    ) -> list[float]:
        return [
            cls.probability(expected_goals, goals)
            for goals in range(max_goals + 1)
        ]

    @classmethod
    def score_matrix(
        cls,
        home_expected_goals: float,
        away_expected_goals: float,
        max_goals: int = 10,
    ) -> list[ScoreProbability]:

        home_distribution = cls.distribution(
            home_expected_goals,
            max_goals,
        )

        away_distribution = cls.distribution(
            away_expected_goals,
            max_goals,
        )

        matrix: list[ScoreProbability] = []

        for home_goals in range(max_goals + 1):
            for away_goals in range(max_goals + 1):
                matrix.append(
                    ScoreProbability(
                        home_goals=home_goals,
                        away_goals=away_goals,
                        probability=(
                            home_distribution[home_goals]
                            * away_distribution[away_goals]
                        ),
                    )
                )

        return matrix

    def predict(
        self,
        home_expected_goals: float,
        away_expected_goals: float,
    ) -> Prediction:

        matrix = self.score_matrix(
            home_expected_goals=home_expected_goals,
            away_expected_goals=away_expected_goals,
        )

        home_probability = sum(
            score.probability
            for score in matrix
            if score.home_goals > score.away_goals
        )

        draw_probability = sum(
            score.probability
            for score in matrix
            if score.home_goals == score.away_goals
        )

        away_probability = sum(
            score.probability
            for score in matrix
            if score.home_goals < score.away_goals
        )

        # Normalización para compensar la probabilidad
        # que queda fuera del límite de la matriz.
        total_probability = (
            home_probability
            + draw_probability
            + away_probability
        )

        if total_probability <= 0:
            raise ValueError(
                "La probabilidad total debe ser mayor que cero."
            )

        return Prediction(
            source="poisson",
            home=home_probability / total_probability,
            draw=draw_probability / total_probability,
            away=away_probability / total_probability,
            confidence=0.75,
        )