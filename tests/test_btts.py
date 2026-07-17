from alfa243.engines.poisson import PoissonEngine
from alfa243.services.match_statistics import MatchStatistics


def test_btts_probability():

    matrix = PoissonEngine.score_matrix(
        home_expected_goals=1.8,
        away_expected_goals=1.1,
    )

    probability = MatchStatistics.btts(matrix)

    assert 0.0 <= probability <= 1.0