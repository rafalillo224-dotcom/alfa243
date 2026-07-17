from alfa243.domain.score_probability import ScoreProbability


def test_score_probability():

    score = ScoreProbability(
        home_goals=2,
        away_goals=1,
        probability=0.135,
    )

    assert score.home_goals == 2
    assert score.away_goals == 1
    assert score.probability == 0.135