from datetime import date

import pytest

from alfa243.domain.match_analysis import MatchAnalysis
from alfa243.domain.match_category import MatchCategory
from alfa243.domain.match_data import MatchData
from alfa243.domain.prediction import Prediction
from alfa243.domain.score_probability import ScoreProbability
from alfa243.services.match_classifier import MatchClassifier


def build_analysis(
    home: float,
    draw: float,
    away: float,
) -> MatchAnalysis:
    match = MatchData(
        competition="LaLiga",
        season="2026-2027",
        round_number=1,
        kickoff=date(2026, 8, 15),
        home_team="Local",
        away_team="Visitante",
        home_odds=2.10,
        draw_odds=3.40,
        away_odds=3.20,
    )

    prediction = Prediction(
        source="fusion",
        home=home,
        draw=draw,
        away=away,
        confidence=0.80,
    )

    score = ScoreProbability(
        home_goals=1,
        away_goals=0,
        probability=0.12,
    )

    return MatchAnalysis(
        match=match,
        home_expected_goals=1.50,
        away_expected_goals=1.00,
        market_prediction=prediction,
        poisson_prediction=prediction,
        fusion_prediction=prediction,
        btts=0.50,
        over_25=0.50,
        under_25=0.50,
        top_scores=(score,),
    )


def test_classifier_detects_favorite() -> None:
    analysis = build_analysis(
        home=0.62,
        draw=0.22,
        away=0.16,
    )

    result = MatchClassifier().classify(analysis)

    assert result.category == MatchCategory.FAVORITE
    assert result.selected_outcome == "1"
    assert result.selected_probability == 0.62


def test_classifier_detects_balanced_match() -> None:
    analysis = build_analysis(
        home=0.36,
        draw=0.31,
        away=0.33,
    )

    result = MatchClassifier().classify(analysis)

    assert result.category == MatchCategory.BALANCED
    assert result.selected_outcome == "1"
    assert abs(result.probability_gap - 0.03) < 1e-9


def test_classifier_detects_neutral_match() -> None:
    analysis = build_analysis(
        home=0.50,
        draw=0.29,
        away=0.21,
    )

    result = MatchClassifier().classify(analysis)

    assert result.category == MatchCategory.NEUTRAL


def test_classifier_rejects_invalid_limits() -> None:
    with pytest.raises(ValueError):
        MatchClassifier(
            favorite_gap=0.10,
            balanced_gap=0.20,
        )