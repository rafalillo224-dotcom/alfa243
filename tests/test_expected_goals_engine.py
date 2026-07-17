import pytest

from alfa243.domain.team_statistics import TeamStatistics
from alfa243.engines.expected_goals import ExpectedGoalsEngine


def test_expected_goals_calculation():

    home_statistics = TeamStatistics(
        goals_for=2.10,
        goals_against=0.90,
    )

    away_statistics = TeamStatistics(
        goals_for=1.40,
        goals_against=1.30,
    )

    home_xg, away_xg = ExpectedGoalsEngine.calculate(
        home_statistics,
        away_statistics,
    )

    assert abs(home_xg - 1.70) < 1e-9
    assert abs(away_xg - 1.15) < 1e-9


def test_team_statistics_rejects_negative_values():

    with pytest.raises(ValueError):
        TeamStatistics(
            goals_for=-1.0,
            goals_against=0.90,
        )