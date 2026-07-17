from pathlib import Path

from alfa243.cli.round_console import show_round_analysis
from alfa243.repositories.match_repository import MatchRepository
from alfa243.repositories.team_repository import TeamRepository
from alfa243.services.match_analyzer import MatchAnalyzer
from alfa243.services.round_analyzer import RoundAnalyzer
from alfa243.version import __version__


def main() -> None:
    print("====================================")
    print(f"ALFA-243 v{__version__}")
    print("====================================")

    data_directory = Path("data")

    team_repository = TeamRepository(
        data_directory / "teams.csv"
    )

    match_repository = MatchRepository(
        data_directory / "matches.csv"
    )

    match_analyzer = MatchAnalyzer(
        team_repository=team_repository,
        market_weight=0.50,
        poisson_weight=0.50,
        top_scores_limit=5,
    )

    round_analyzer = RoundAnalyzer(
        match_analyzer=match_analyzer,
    )

    matches = match_repository.get_by_round(
        competition="LaLiga",
        season="2026-2027",
        round_number=1,
    )

    analyses = round_analyzer.analyze(matches)

    show_round_analysis(analyses)


if __name__ == "__main__":
    main()