from datetime import date
from pathlib import Path

from alfa243.domain.match_data import MatchData
from alfa243.repositories.team_repository import TeamRepository
from alfa243.services.match_analyzer import MatchAnalyzer


def test_match_analyzer_builds_complete_analysis(
    tmp_path: Path,
) -> None:
    csv_path = tmp_path / "teams.csv"

    csv_path.write_text(
        "team,goals_for,goals_against\n"
        "Real Madrid,2.10,0.90\n"
        "Barcelona,1.40,1.30\n",
        encoding="utf-8",
    )

    repository = TeamRepository(csv_path)
    analyzer = MatchAnalyzer(repository)

    match = MatchData(
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

    analysis = analyzer.analyze(match)

    assert analysis.match == match
    assert abs(analysis.home_expected_goals - 1.70) < 1e-9
    assert abs(analysis.away_expected_goals - 1.15) < 1e-9

    assert (
        abs(
            analysis.fusion_prediction.home
            + analysis.fusion_prediction.draw
            + analysis.fusion_prediction.away
            - 1.0
        )
        < 1e-9
    )

    assert 0.0 <= analysis.btts <= 1.0
    assert 0.0 <= analysis.over_25 <= 1.0
    assert 0.0 <= analysis.under_25 <= 1.0
    assert len(analysis.top_scores) == 5