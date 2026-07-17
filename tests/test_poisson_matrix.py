from alfa243.engines.poisson import PoissonEngine


def test_score_matrix_size():

    matrix = PoissonEngine.score_matrix(
        home_expected_goals=1.5,
        away_expected_goals=1.2,
    )

    assert len(matrix) == 121