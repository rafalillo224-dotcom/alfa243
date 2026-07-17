from dataclasses import dataclass

from alfa243.domain.prediction import Prediction


@dataclass(slots=True)
class ValueResult:
    outcome: str
    market_probability: float
    model_probability: float
    edge: float
    expected_value: float
    is_value_bet: bool


class ValueEngine:
    """Compara la probabilidad del modelo con la del mercado."""

    @staticmethod
    def evaluate(
        market: Prediction,
        model: Prediction,
        outcome: str,
        odds: float,
    ) -> ValueResult:

        market_prob = getattr(market, outcome)
        model_prob = getattr(model, outcome)

        edge = model_prob - market_prob
        expected_value = model_prob * odds - 1

        return ValueResult(
            outcome=outcome,
            market_probability=market_prob,
            model_probability=model_prob,
            edge=edge,
            expected_value=expected_value,
            is_value_bet=expected_value > 0,
        )