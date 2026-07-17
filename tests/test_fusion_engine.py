from alfa243.domain.prediction import Prediction
from alfa243.engines.fusion import FusionEngine


def test_fusion_average():

    market = Prediction(
        source="market",
        home=0.40,
        draw=0.30,
        away=0.30,
        confidence=1.0,
    )

    poisson = Prediction(
        source="poisson",
        home=0.60,
        draw=0.20,
        away=0.20,
        confidence=0.8,
    )

    result = FusionEngine.predict(
        market,
        poisson,
    )

    assert abs(result.home - 0.50) < 1e-9
    assert abs(result.draw - 0.25) < 1e-9
    assert abs(result.away - 0.25) < 1e-9


def test_weighted_fusion():

    market = Prediction(
        source="market",
        home=0.40,
        draw=0.30,
        away=0.30,
        confidence=1.0,
    )

    poisson = Prediction(
        source="poisson",
        home=0.60,
        draw=0.20,
        away=0.20,
        confidence=0.8,
    )

    result = FusionEngine.predict(
        market,
        poisson,
        first_weight=0.70,
        second_weight=0.30,
    )

    assert abs(result.home - 0.46) < 1e-9
    assert abs(result.draw - 0.27) < 1e-9
    assert abs(result.away - 0.27) < 1e-9    