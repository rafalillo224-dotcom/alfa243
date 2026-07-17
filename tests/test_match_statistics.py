from alfa243.engines.poisson import PoissonEngine
from alfa243.services.match_statistics import MatchStatistics


def test_most_likely_score():

    matrix = PoissonEngine.score_matrix(
        home_expected_goals=1.8,
        away_expected_goals=1.1,
    )

    score = MatchStatistics.most_likely_score(matrix)

    assert score.home_goals >= 0
    assert score.away_goals >= 0
    assert score.probability > 0