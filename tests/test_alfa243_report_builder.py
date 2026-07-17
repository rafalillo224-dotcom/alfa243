from unittest.mock import Mock

import pytest

from alfa243.services.alfa243_report_builder import (
    Alfa243ReportBuilder,
)


def build_result() -> Mock:
    result = Mock()

    result.competition = "LaLiga"
    result.season = "2026-2027"
    result.round_number = 1
    result.analyzed_match_count = 20
    result.valid_pattern_count = 652
    result.selected_combination_count = 243
    result.coverage_percent = 71.84

    favorite = build_classified_match(
        home_team="Real Madrid",
        away_team="Getafe",
        outcome="1",
        probability=0.68,
        gap=0.24,
    )

    balanced = build_classified_match(
        home_team="Sevilla",
        away_team="Betis",
        outcome="X",
        probability=0.34,
        gap=0.02,
    )

    result.selection.favorites = (
        favorite,
        favorite,
        favorite,
        favorite,
        favorite,
        favorite,
    )

    result.selection.balanced = (
        balanced,
        balanced,
        balanced,
        balanced,
        balanced,
        balanced,
    )

    first_analysis = Mock()
    first_analysis.rank = 1
    first_analysis.code = "XX1121"
    first_analysis.home_count = 7
    first_analysis.draw_count = 2
    first_analysis.away_count = 3
    first_analysis.probability_percent = 0.00482
    first_analysis.fair_odds = 20746.89
    first_analysis.cumulative_coverage = 0.015

    second_analysis = Mock()
    second_analysis.rank = 2
    second_analysis.code = "X11121"
    second_analysis.home_count = 8
    second_analysis.draw_count = 1
    second_analysis.away_count = 3
    second_analysis.probability_percent = 0.00450
    second_analysis.fair_odds = 22222.22
    second_analysis.cumulative_coverage = 0.029

    result.portfolio.analyses = (
        first_analysis,
        second_analysis,
    )

    return result


def build_classified_match(
    home_team: str,
    away_team: str,
    outcome: str,
    probability: float,
    gap: float,
) -> Mock:
    classified = Mock()

    classified.analysis.match.home_team = home_team
    classified.analysis.match.away_team = away_team

    classified.selected_outcome = outcome
    classified.selected_probability = probability
    classified.probability_gap = gap

    return classified


def test_report_contains_round_summary() -> None:
    report = Alfa243ReportBuilder().build(
        build_result()
    )

    assert "ALFA-243" in report
    assert "Competición : LaLiga" in report
    assert "Temporada   : 2026-2027" in report
    assert "Jornada     : 1" in report
    assert "Partidos analizados ............ 20" in report
    assert "Patrones válidos ............... 652" in report
    assert "Combinaciones seleccionadas .... 243" in report
    assert "Cobertura del universo válido .. 71.84 %" in report


def test_report_contains_selected_matches() -> None:
    report = Alfa243ReportBuilder().build(
        build_result()
    )

    assert "6 FAVORITOS" in report
    assert "Real Madrid vs Getafe" in report
    assert "Signo: 1" in report
    assert "Prob.: 68.00 %" in report

    assert "6 IGUALADOS" in report
    assert "Sevilla vs Betis" in report
    assert "Signo: X" in report
    assert "Gap: 2.00 pp" in report


def test_report_contains_ranked_combinations() -> None:
    report = Alfa243ReportBuilder().build(
        build_result(),
        top_limit=2,
    )

    assert "TOP 2 COMBINACIONES" in report
    assert "#1" in report
    assert "Código: XX1121" in report
    assert "Cuota justa: 20746.89" in report
    assert "Cobertura acumulada: 1.50 %" in report

    assert "#2" in report
    assert "Código: X11121" in report


def test_report_respects_top_limit() -> None:
    report = Alfa243ReportBuilder().build(
        build_result(),
        top_limit=1,
    )

    assert "TOP 1 COMBINACIONES" in report
    assert "Código: XX1121" in report
    assert "Código: X11121" not in report


def test_report_rejects_invalid_top_limit() -> None:
    with pytest.raises(
        ValueError,
        match="límite del ranking",
    ):
        Alfa243ReportBuilder().build(
            build_result(),
            top_limit=0,
        )