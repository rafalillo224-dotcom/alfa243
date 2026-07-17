from datetime import date, timedelta

import pytest

from alfa243.domain.classified_match import ClassifiedMatch
from alfa243.domain.match_analysis import MatchAnalysis
from alfa243.domain.match_category import MatchCategory
from alfa243.domain.match_data import MatchData
from alfa243.domain.prediction import Prediction
from alfa243.domain.score_probability import ScoreProbability
from alfa243.services.alfa_selector import AlfaSelector


def build_classified_match(
    index: int,
    category: MatchCategory,
    selected_probability: float,
    probability_gap: float,
) -> ClassifiedMatch:
    match = MatchData(
        competition="Test League",
        season="2026-2027",
        round_number=1,
        kickoff=date(2026, 8, 1) + timedelta(days=index),
        home_team=f"Local {index}",
        away_team=f"Visitante {index}",
        home_odds=2.10,
        draw_odds=3.40,
        away_odds=3.20,
    )

    prediction = Prediction(
        source="fusion",
        home=selected_probability,
        draw=(1.0 - selected_probability) / 2,
        away=(1.0 - selected_probability) / 2,
        confidence=0.80,
    )

    score = ScoreProbability(
        home_goals=1,
        away_goals=0,
        probability=0.12,
    )

    analysis = MatchAnalysis(
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

    return ClassifiedMatch(
        analysis=analysis,
        category=category,
        selected_outcome="1",
        selected_probability=selected_probability,
        probability_gap=probability_gap,
    )


def test_selector_builds_six_plus_six_selection() -> None:
    classified_matches = [
        build_classified_match(
            index=index,
            category=MatchCategory.FAVORITE,
            selected_probability=0.60 + index * 0.01,
            probability_gap=0.20,
        )
        for index in range(8)
    ]

    classified_matches += [
        build_classified_match(
            index=index,
            category=MatchCategory.BALANCED,
            selected_probability=0.36,
            probability_gap=0.01 + (index - 8) * 0.01,
        )
        for index in range(8, 16)
    ]

    selection = AlfaSelector().select(classified_matches)

    assert len(selection.favorites) == 6
    assert len(selection.balanced) == 6
    assert len(selection.all_matches) == 12


def test_selector_chooses_strongest_favorites() -> None:
    classified_matches = [
        build_classified_match(
            index=index,
            category=MatchCategory.FAVORITE,
            selected_probability=0.55 + index * 0.01,
            probability_gap=0.20,
        )
        for index in range(7)
    ]

    classified_matches += [
        build_classified_match(
            index=index,
            category=MatchCategory.BALANCED,
            selected_probability=0.36,
            probability_gap=0.03,
        )
        for index in range(7, 13)
    ]

    selection = AlfaSelector().select(classified_matches)

    probabilities = [
        match.selected_probability
        for match in selection.favorites
    ]

    assert min(probabilities) == pytest.approx(0.56)
    assert max(probabilities) == pytest.approx(0.61)


def test_selector_rejects_insufficient_balanced_matches() -> None:
    classified_matches = [
        build_classified_match(
            index=index,
            category=MatchCategory.FAVORITE,
            selected_probability=0.65,
            probability_gap=0.20,
        )
        for index in range(6)
    ]

    classified_matches += [
        build_classified_match(
            index=index,
            category=MatchCategory.BALANCED,
            selected_probability=0.36,
            probability_gap=0.03,
        )
        for index in range(6, 11)
    ]

    with pytest.raises(
        ValueError,
        match="No hay suficientes partidos igualados",
    ):
        AlfaSelector().select(classified_matches)


def test_selector_rejects_duplicate_matches() -> None:
    favorites = [
        build_classified_match(
            index=index,
            category=MatchCategory.FAVORITE,
            selected_probability=0.65,
            probability_gap=0.20,
        )
        for index in range(6)
    ]

    balanced = [
        build_classified_match(
            index=index,
            category=MatchCategory.BALANCED,
            selected_probability=0.36,
            probability_gap=0.03,
        )
        for index in range(6, 12)
    ]

    classified_matches = favorites + balanced
    classified_matches.append(favorites[0])

    with pytest.raises(
        ValueError,
        match="partidos duplicados",
    ):
        AlfaSelector().select(classified_matches)