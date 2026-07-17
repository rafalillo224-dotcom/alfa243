from datetime import date
from pathlib import Path

from alfa243.domain.match_data import MatchData
from alfa243.repositories.team_repository import TeamRepository
from alfa243.services.match_analyzer import MatchAnalyzer
from alfa243.services.round_analyzer import RoundAnalyzer


def test_round_analyzer_analyzes_and_orders_matches(
    tmp_path: Path,
) -> None:
    csv_path = tmp_path / "teams.csv"

    csv_path.write_text(
        "team,goals_for,goals_against\n"
        "Real Madrid,2.10,0.90\n"
        "Barcelona,1.40,1.30\n"
        "Sevilla,1.35,1.20\n"
        "Betis,1.45,1.25\n",
        encoding="utf-8",
    )

    team_repository = TeamRepository(csv_path)
    match_analyzer = MatchAnalyzer(team_repository)
    round_analyzer = RoundAnalyzer(match_analyzer)

    later_match = MatchData(
        competition="LaLiga",
        season="2026-2027",
        round_number=1,
        kickoff=date(2026, 8, 16),
        home_team="Sevilla",
        away_team="Betis",
        home_odds=2.45,
        draw_odds=3.20,
        away_odds=2.95,
    )

    earlier_match = MatchData(
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

    analyses = round_analyzer.analyze(
        [later_match, earlier_match]
    )

    assert len(analyses) == 2
    assert analyses[0].match == earlier_match
    assert analyses[1].match == later_match