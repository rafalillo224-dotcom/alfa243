from alfa243.engines.poisson import PoissonEngine
from alfa243.services.match_statistics import MatchStatistics


def test_top_scores():

    matrix = PoissonEngine.score_matrix(
        home_expected_goals=1.8,
        away_expected_goals=1.1,
    )

    scores = MatchStatistics.top_scores(matrix)

    assert len(scores) == 5

    assert (
        scores[0].probability
        >= scores[1].probability
        >= scores[2].probability
    )