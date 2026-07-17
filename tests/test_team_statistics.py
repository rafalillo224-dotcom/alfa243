import pytest

from alfa243.domain.team_statistics import TeamStatistics


def test_team_statistics_creation():

    statistics = TeamStatistics(
        goals_for=2.10,
        goals_against=0.90,
    )

    assert statistics.goals_for == 2.10
    assert statistics.goals_against == 0.90


def test_team_statistics_rejects_negative_goals_against():

    with pytest.raises(ValueError):
        TeamStatistics(
            goals_for=2.10,
            goals_against=-0.50,
        )