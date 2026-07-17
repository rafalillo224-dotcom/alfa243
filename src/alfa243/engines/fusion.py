from alfa243.domain.prediction import Prediction


class FusionEngine:
    """Combina dos predicciones mediante pesos configurables."""

    @staticmethod
    def predict(
        first: Prediction,
        second: Prediction,
        first_weight: float = 0.5,
        second_weight: float = 0.5,
    ) -> Prediction:
        if first_weight < 0 or second_weight < 0:
            raise ValueError("Los pesos no pueden ser negativos.")

        total_weight = first_weight + second_weight

        if total_weight == 0:
            raise ValueError("La suma de los pesos debe ser mayor que cero.")

        first_normalized = first_weight / total_weight
        second_normalized = second_weight / total_weight

        return Prediction(
            source="fusion",
            home=(
                first.home * first_normalized
                + second.home * second_normalized
            ),
            draw=(
                first.draw * first_normalized
                + second.draw * second_normalized
            ),
            away=(
                first.away * first_normalized
                + second.away * second_normalized
            ),
            confidence=(
                first.confidence * first_normalized
                + second.confidence * second_normalized
            ),
        )