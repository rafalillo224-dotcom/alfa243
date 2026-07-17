from datetime import date

from alfa243.domain.match_analysis import MatchAnalysis
from alfa243.domain.match_data import MatchData
from alfa243.domain.prediction import Prediction
from alfa243.domain.score_probability import ScoreProbability


def test_match_analysis_returns_most_likely_score() -> None:
    match = MatchData(
        competition="LaLiga",
        season="2026-2027",
        round_number=1,
        kickoff=date(2026, 8, 15),
        home_team="Real Madrid",
        away_team="Barcelona",
        home_odds=2.10,
        draw_odds=3.40,
        away_odds=3.20,
    )

    prediction = Prediction(
        source="test",
        home=0.50,
        draw=0.25,
        away=0.25,
        confidence=1.0,
    )

    first_score = ScoreProbability(
        home_goals=1,
        away_goals=1,
        probability=0.12,
    )

    second_score = ScoreProbability(
        home_goals=2,
        away_goals=1,
        probability=0.10,
    )

    analysis = MatchAnalysis(
        match=match,
        home_expected_goals=1.70,
        away_expected_goals=1.15,
        market_prediction=prediction,
        poisson_prediction=prediction,
        fusion_prediction=prediction,
        btts=0.55,
        over_25=0.54,
        under_25=0.46,
        top_scores=(first_score, second_score),
    )

    assert analysis.most_likely_score == first_score