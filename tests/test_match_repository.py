from pathlib import Path

import pytest

from alfa243.repositories.match_repository import MatchRepository


def create_matches_csv(tmp_path: Path) -> Path:
    csv_path = tmp_path / "matches.csv"

    csv_path.write_text(
        "competition,season,round_number,kickoff,"
        "home_team,away_team,home_odds,draw_odds,away_odds\n"
        "LaLiga,2026-2027,1,2026-08-15,"
        "Real Madrid,Barcelona,2.10,3.40,3.20\n"
        "LaLiga,2026-2027,1,2026-08-16,"
        "Sevilla,Betis,2.45,3.20,2.95\n"
        "LaLiga,2026-2027,2,2026-08-22,"
        "Barcelona,Sevilla,1.70,3.80,4.80\n",
        encoding="utf-8",
    )

    return csv_path


def test_repository_loads_all_matches(
    tmp_path: Path,
) -> None:
    csv_path = create_matches_csv(tmp_path)
    repository = MatchRepository(csv_path)

    matches = repository.get_all()

    assert len(matches) == 3
    assert matches[0].home_team == "Real Madrid"
    assert matches[0].away_team == "Barcelona"


def test_repository_filters_by_round(
    tmp_path: Path,
) -> None:
    csv_path = create_matches_csv(tmp_path)
    repository = MatchRepository(csv_path)

    matches = repository.get_by_round(
        competition="LaLiga",
        season="2026-2027",
        round_number=1,
    )

    assert len(matches) == 2
    assert all(match.round_number == 1 for match in matches)


def test_repository_filter_is_case_insensitive(
    tmp_path: Path,
) -> None:
    csv_path = create_matches_csv(tmp_path)
    repository = MatchRepository(csv_path)

    matches = repository.get_by_round(
        competition="laliga",
        season="2026-2027",
        round_number=1,
    )

    assert len(matches) == 2


def test_repository_returns_empty_list_for_unknown_round(
    tmp_path: Path,
) -> None:
    csv_path = create_matches_csv(tmp_path)
    repository = MatchRepository(csv_path)

    matches = repository.get_by_round(
        competition="LaLiga",
        season="2026-2027",
        round_number=99,
    )

    assert matches == []


def test_repository_rejects_missing_file(
    tmp_path: Path,
) -> None:
    repository = MatchRepository(
        tmp_path / "missing.csv"
    )

    with pytest.raises(FileNotFoundError):
        repository.get_all()