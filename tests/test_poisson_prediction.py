from alfa243.engines.poisson import PoissonEngine


def test_prediction_probabilities_sum_to_one():

    engine = PoissonEngine()

    prediction = engine.predict(
        home_expected_goals=1.8,
        away_expected_goals=1.1,
    )

    total = (
        prediction.home
        + prediction.draw
        + prediction.away
    )

    assert abs(total - 1.0) < 0.001