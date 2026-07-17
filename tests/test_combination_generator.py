from datetime import date, timedelta

import pytest

from alfa243.domain.alfa_selection import AlfaSelection
from alfa243.domain.classified_match import ClassifiedMatch
from alfa243.domain.match_analysis import MatchAnalysis
from alfa243.domain.match_category import MatchCategory
from alfa243.domain.match_data import MatchData
from alfa243.domain.prediction import Prediction
from alfa243.domain.score_probability import ScoreProbability
from alfa243.services.combination_generator import (
    CombinationGenerator,
)


def build_classified_match(
    index: int,
    category: MatchCategory,
    home: float,
    draw: float,
    away: float,
    selected_outcome: str,
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
        home=home,
        draw=draw,
        away=away,
        confidence=0.80,
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
        top_scores=(
            ScoreProbability(
                home_goals=1,
                away_goals=0,
                probability=0.12,
            ),
        ),
    )

    probabilities = {
        "1": home,
        "X": draw,
        "2": away,
    }

    ordered_probabilities = sorted(
        probabilities.values(),
        reverse=True,
    )

    return ClassifiedMatch(
        analysis=analysis,
        category=category,
        selected_outcome=selected_outcome,
        selected_probability=probabilities[selected_outcome],
        probability_gap=(
            ordered_probabilities[0]
            - ordered_probabilities[1]
        ),
    )


def build_selection() -> AlfaSelection:
    favorites = tuple(
        build_classified_match(
            index=index,
            category=MatchCategory.FAVORITE,
            home=0.65,
            draw=0.20,
            away=0.15,
            selected_outcome="1",
        )
        for index in range(6)
    )

    balanced = tuple(
        build_classified_match(
            index=index,
            category=MatchCategory.BALANCED,
            home=0.36,
            draw=0.34,
            away=0.30,
            selected_outcome="1",
        )
        for index in range(6, 12)
    )

    return AlfaSelection(
        favorites=favorites,
        balanced=balanced,
    )


def test_generator_returns_243_combinations() -> None:
    combinations = CombinationGenerator().generate(
        build_selection()
    )

    assert len(combinations) == 243


def test_combinations_have_six_favorites_and_six_balanced() -> None:
    combination = CombinationGenerator().generate(
        build_selection()
    )[0]

    assert len(combination.favorites) == 6
    assert len(combination.balanced) == 6
    assert len(combination.all_picks) == 12


def test_generator_excludes_zero_five_and_six_draws() -> None:
    combinations = CombinationGenerator().generate(
        build_selection()
    )

    assert all(
        1 <= combination.draw_count <= 4
        for combination in combinations
    )


def test_combinations_are_sorted_by_probability() -> None:
    combinations = CombinationGenerator().generate(
        build_selection()
    )

    probabilities = [
        combination.probability
        for combination in combinations
    ]

    assert probabilities == sorted(
        probabilities,
        reverse=True,
    )


def test_generator_counts_all_patterns_before_limit() -> None:
    generator = CombinationGenerator()

    assert generator.count_valid_patterns() == 652


def test_generator_rejects_invalid_draw_range() -> None:
    with pytest.raises(ValueError):
        CombinationGenerator(
            minimum_draws=5,
            maximum_draws=4,
        )