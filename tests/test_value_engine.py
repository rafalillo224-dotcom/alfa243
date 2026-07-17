from alfa243.domain.prediction import Prediction
from alfa243.engines.value import ValueEngine


def test_positive_expected_value():

    market = Prediction(
        source="market",
        home=0.44,
        draw=0.28,
        away=0.28,
    )

    model = Prediction(
        source="model",
        home=0.50,
        draw=0.25,
        away=0.25,
    )

    result = ValueEngine.evaluate(
        market=market,
        model=model,
        outcome="home",
        odds=2.20,
    )

    assert result.is_value_bet
    assert result.expected_value > 0