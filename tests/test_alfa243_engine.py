from unittest.mock import Mock

import pytest

from alfa243.services.alfa243_engine import Alfa243Engine


def build_engine():
    match_repository = Mock()
    round_analyzer = Mock()
    match_classifier = Mock()
    alfa_selector = Mock()
    combination_generator = Mock()
    combination_analyzer = Mock()

    engine = Alfa243Engine(
        match_repository=match_repository,
        round_analyzer=round_analyzer,
        match_classifier=match_classifier,
        alfa_selector=alfa_selector,
        combination_generator=combination_generator,
        combination_analyzer=combination_analyzer,
    )

    return (
        engine,
        match_repository,
        round_analyzer,
        match_classifier,
        alfa_selector,
        combination_generator,
        combination_analyzer,
    )


def configure_pipeline(
    match_repository,
    round_analyzer,
    match_classifier,
    alfa_selector,
    combination_generator,
    combination_analyzer,
):
    matches = [Mock(name="match_1"), Mock(name="match_2")]
    analyses = [Mock(name="analysis_1"), Mock(name="analysis_2")]
    classified = [
        Mock(name="classified_1"),
        Mock(name="classified_2"),
    ]
    selection = Mock(name="selection")
    selected = [Mock(name="combination_1")]
    valid_universe = [
        Mock(name="combination_1"),
        Mock(name="combination_2"),
    ]
    portfolio = Mock(name="portfolio")
    portfolio.combination_count = 1
    portfolio.coverage_percent = 75.0

    match_repository.get_by_round.return_value = matches
    round_analyzer.analyze.return_value = analyses
    match_classifier.classify_all.return_value = classified
    alfa_selector.select.return_value = selection
    combination_generator.generate.return_value = selected
    combination_generator.generate_all.return_value = (
        valid_universe
    )
    combination_analyzer.analyze.return_value = portfolio

    return {
        "matches": matches,
        "analyses": analyses,
        "classified": classified,
        "selection": selection,
        "selected": selected,
        "valid_universe": valid_universe,
        "portfolio": portfolio,
    }


def test_engine_executes_complete_pipeline() -> None:
    (
        engine,
        repository,
        round_analyzer,
        classifier,
        selector,
        generator,
        combination_analyzer,
    ) = build_engine()

    data = configure_pipeline(
        repository,
        round_analyzer,
        classifier,
        selector,
        generator,
        combination_analyzer,
    )

    result = engine.analyze_round(
        competition="LaLiga",
        season="2026-2027",
        round_number=1,
    )

    repository.get_by_round.assert_called_once_with(
        competition="LaLiga",
        season="2026-2027",
        round_number=1,
    )

    round_analyzer.analyze.assert_called_once_with(
        data["matches"]
    )

    classifier.classify_all.assert_called_once_with(
        data["analyses"]
    )

    selector.select.assert_called_once_with(
        data["classified"]
    )

    generator.generate.assert_called_once_with(
        data["selection"]
    )

    generator.generate_all.assert_called_once_with(
        data["selection"]
    )

    combination_analyzer.analyze.assert_called_once_with(
        selected=data["selected"],
        valid_universe=data["valid_universe"],
    )

    assert result.portfolio is data["portfolio"]


def test_engine_returns_complete_result() -> None:
    (
        engine,
        repository,
        round_analyzer,
        classifier,
        selector,
        generator,
        combination_analyzer,
    ) = build_engine()

    data = configure_pipeline(
        repository,
        round_analyzer,
        classifier,
        selector,
        generator,
        combination_analyzer,
    )

    result = engine.analyze_round(
        competition="LaLiga",
        season="2026-2027",
        round_number=1,
    )

    assert result.competition == "LaLiga"
    assert result.season == "2026-2027"
    assert result.round_number == 1
    assert result.match_analyses == tuple(data["analyses"])
    assert result.selection is data["selection"]
    assert result.valid_pattern_count == 2
    assert result.analyzed_match_count == 2


def test_engine_rejects_round_without_matches() -> None:
    (
        engine,
        repository,
        _,
        _,
        _,
        _,
        _,
    ) = build_engine()

    repository.get_by_round.return_value = []

    with pytest.raises(
        ValueError,
        match="No se encontraron partidos",
    ):
        engine.analyze_round(
            competition="LaLiga",
            season="2026-2027",
            round_number=1,
        )


def test_engine_rejects_invalid_round_number() -> None:
    engine, *_ = build_engine()

    with pytest.raises(
        ValueError,
        match="número de jornada",
    ):
        engine.analyze_round(
            competition="LaLiga",
            season="2026-2027",
            round_number=0,
        )


def test_analyze_matches_does_not_use_repository() -> None:
    (
        engine,
        repository,
        round_analyzer,
        classifier,
        selector,
        generator,
        combination_analyzer,
    ) = build_engine()

    data = configure_pipeline(
        repository,
        round_analyzer,
        classifier,
        selector,
        generator,
        combination_analyzer,
    )

    result = engine.analyze_matches(
        matches=data["matches"],
        competition="LaLiga",
        season="2026-2027",
        round_number=1,
    )

    repository.get_by_round.assert_not_called()

    assert result.match_analyses == tuple(data["analyses"])
    assert result.valid_pattern_count == 2