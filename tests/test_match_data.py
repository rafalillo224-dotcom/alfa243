from datetime import date

import pytest

from alfa243.domain.match_data import MatchData


def test_match_data_creation() -> None:
    match = MatchData(
        competition="LaLiga",
        season="2026-2027",
        round_number=8,
        kickoff=date(2026, 10, 18),
        home_team="Real Madrid",
        away_team="Barcelona",
        home_odds=2.10,
        draw_odds=3.40,
        away_odds=3.20,
    )

    assert match.competition == "LaLiga"
    assert match.season == "2026-2027"
    assert match.round_number == 8
    assert match.kickoff == date(2026, 10, 18)
    assert match.home_team == "Real Madrid"
    assert match.away_team == "Barcelona"


def test_match_data_rejects_invalid_round() -> None:
    with pytest.raises(ValueError):
        MatchData(
            competition="LaLiga",
            season="2026-2027",
            round_number=0,
            kickoff=date(2026, 10, 18),
            home_team="Real Madrid",
            away_team="Barcelona",
            home_odds=2.10,
            draw_odds=3.40,
            away_odds=3.20,
        )


def test_match_data_rejects_same_team() -> None:
    with pytest.raises(ValueError):
        MatchData(
            competition="LaLiga",
            season="2026-2027",
            round_number=8,
            kickoff=date(2026, 10, 18),
            home_team="Real Madrid",
            away_team="real madrid",
            home_odds=2.10,
            draw_odds=3.40,
            away_odds=3.20,
        )


def test_match_data_rejects_invalid_odds() -> None:
    with pytest.raises(ValueError):
        MatchData(
            competition="LaLiga",
            season="2026-2027",
            round_number=8,
            kickoff=date(2026, 10, 18),
            home_team="Real Madrid",
            away_team="Barcelona",
            home_odds=1.00,
            draw_odds=3.40,
            away_odds=3.20,
        )