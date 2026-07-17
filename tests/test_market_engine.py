from alfa243.domain.match import Match
from alfa243.engines.market import MarketEngine


def test_market_probabilities_sum_to_one():
    match = Match(
        home_team="A",
        away_team="B",
        home_odds=2.10,
        draw_odds=3.40,
        away_odds=3.20,
    )

    result = MarketEngine.calculate(match)

    total = result.home + result.draw + result.away

    assert abs(total - 1.0) < 1e-9