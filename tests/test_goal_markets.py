from alfa243.engines.poisson import PoissonEngine
from alfa243.services.match_statistics import MatchStatistics


def test_goal_markets():

    matrix = PoissonEngine.score_matrix(
        home_expected_goals=1.8,
        away_expected_goals=1.1,
    )

    over = MatchStatistics.over_25(matrix)
    under = MatchStatistics.under_25(matrix)

    assert 0 <= over <= 1
    assert 0 <= under <= 1
    assert abs((over + under) - 1.0) < 1e-9