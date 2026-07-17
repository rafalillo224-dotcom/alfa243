from pathlib import Path

import pytest

from alfa243.repositories.team_repository import TeamRepository


def test_repository_returns_team_statistics(
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

    statistics = repository.get("Real Madrid")

    assert statistics.goals_for == 2.10
    assert statistics.goals_against == 0.90


def test_repository_search_is_case_insensitive(
    tmp_path: Path,
) -> None:
    csv_path = tmp_path / "teams.csv"

    csv_path.write_text(
        "team,goals_for,goals_against\n"
        "Real Madrid,2.10,0.90\n",
        encoding="utf-8",
    )

    repository = TeamRepository(csv_path)

    statistics = repository.get("real madrid")

    assert statistics.goals_for == 2.10


def test_repository_rejects_unknown_team(
    tmp_path: Path,
) -> None:
    csv_path = tmp_path / "teams.csv"

    csv_path.write_text(
        "team,goals_for,goals_against\n"
        "Real Madrid,2.10,0.90\n",
        encoding="utf-8",
    )

    repository = TeamRepository(csv_path)

    with pytest.raises(KeyError):
        repository.get("Sevilla")


def test_repository_rejects_missing_file(
    tmp_path: Path,
) -> None:
    repository = TeamRepository(
        tmp_path / "missing.csv"
    )

    with pytest.raises(FileNotFoundError):
        repository.get("Real Madrid")