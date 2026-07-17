from datetime import date, timedelta

import pytest

from alfa243.domain.alfa_selection import AlfaSelection
from alfa243.domain.classified_match import ClassifiedMatch
from alfa243.domain.match_analysis import MatchAnalysis
from alfa243.domain.match_category import MatchCategory
from alfa243.domain.match_data import MatchData
from alfa243.domain.prediction import Prediction
from alfa243.domain.score_probability import ScoreProbability
from alfa243.services.combination_analyzer import CombinationAnalyzer
from alfa243.services.combination_generator import CombinationGenerator


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

    ordered = sorted(
        probabilities.values(),
        reverse=True,
    )

    return ClassifiedMatch(
        analysis=analysis,
        category=category,
        selected_outcome=selected_outcome,
        selected_probability=probabilities[selected_outcome],
        probability_gap=ordered[0] - ordered[1],
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


def build_portfolio():
    selection = build_selection()
    generator = CombinationGenerator()

    selected = generator.generate(selection)
    valid_universe = generator.generate_all(selection)

    return CombinationAnalyzer().analyze(
        selected=selected,
        valid_universe=valid_universe,
    )


def test_analyzer_creates_ranked_portfolio() -> None:
    portfolio = build_portfolio()

    assert portfolio.combination_count == 243
    assert portfolio.analyses[0].rank == 1
    assert portfolio.analyses[-1].rank == 243


def test_portfolio_is_sorted_by_probability() -> None:
    portfolio = build_portfolio()

    probabilities = [
        analysis.probability
        for analysis in portfolio.analyses
    ]

    assert probabilities == sorted(
        probabilities,
        reverse=True,
    )


def test_analysis_calculates_fair_odds() -> None:
    portfolio = build_portfolio()
    analysis = portfolio.analyses[0]

    assert analysis.fair_odds == pytest.approx(
        1.0 / analysis.probability
    )

    assert analysis.probability_percent == pytest.approx(
        analysis.probability * 100.0
    )


def test_sign_counts_total_twelve_picks() -> None:
    portfolio = build_portfolio()
    analysis = portfolio.analyses[0]

    assert (
        analysis.home_count
        + analysis.draw_count
        + analysis.away_count
        == 12
    )


def test_cumulative_coverage_finishes_at_portfolio_coverage() -> None:
    portfolio = build_portfolio()
    final_analysis = portfolio.analyses[-1]

    assert final_analysis.cumulative_coverage == pytest.approx(
        portfolio.coverage_ratio
    )

    assert 0.0 < portfolio.coverage_ratio <= 1.0


def test_analyzer_rejects_empty_selection() -> None:
    selection = build_selection()
    valid_universe = CombinationGenerator().generate_all(
        selection
    )

    with pytest.raises(
        ValueError,
        match="al menos una combinación",
    ):
        CombinationAnalyzer().analyze(
            selected=[],
            valid_universe=valid_universe,
        )


def test_analyzer_rejects_duplicate_combinations() -> None:
    selection = build_selection()
    generator = CombinationGenerator()

    selected = generator.generate(selection)
    valid_universe = generator.generate_all(selection)

    duplicated = selected + [selected[0]]

    with pytest.raises(
        ValueError,
        match="combinaciones duplicadas",
    ):
        CombinationAnalyzer().analyze(
            selected=duplicated,
            valid_universe=valid_universe,
        )