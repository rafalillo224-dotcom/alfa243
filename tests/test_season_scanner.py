from pathlib import Path

import pytest

from alfa243.services.season_scanner import SeasonScanner


REQUIRED_LEAGUES = (
    "E0",
    "SP1",
    "D1",
    "I1",
    "F1",
)


def create_csv_files(
    directory: Path,
    league_codes: tuple[str, ...],
) -> None:
    for league_code in league_codes:
        file_path = directory / f"{league_code}.csv"
        file_path.write_text(
            "Date,HomeTeam,AwayTeam,FTHG,FTAG,FTR\n",
            encoding="utf-8",
        )


def test_scanner_detects_and_orders_seasons(
    tmp_path: Path,
) -> None:
    season_2025 = tmp_path / "data 25 26"
    season_2025.mkdir()
    create_csv_files(
        season_2025,
        REQUIRED_LEAGUES,
    )

    season_2016 = tmp_path / "data 16 17"
    season_2016.mkdir()
    create_csv_files(
        season_2016,
        REQUIRED_LEAGUES,
    )

    result = SeasonScanner(tmp_path).scan()

    assert result.season_count == 2

    assert tuple(
        season.season
        for season in result.seasons
    ) == (
        "2016-2017",
        "2025-2026",
    )


def test_scanner_detects_csv_files_and_ignores_others(
    tmp_path: Path,
) -> None:
    season_directory = tmp_path / "data 24 25"
    season_directory.mkdir()

    create_csv_files(
        season_directory,
        REQUIRED_LEAGUES,
    )

    (season_directory / "notes.txt").write_text(
        "Archivo auxiliar",
        encoding="utf-8",
    )

    result = SeasonScanner(tmp_path).scan()
    season = result.seasons[0]

    assert season.csv_count == 5
    assert season.league_codes == (
        "D1",
        "E0",
        "F1",
        "I1",
        "SP1",
    )


def test_scanner_reports_missing_required_leagues(
    tmp_path: Path,
) -> None:
    season_directory = tmp_path / "data 23 24"
    season_directory.mkdir()

    create_csv_files(
        season_directory,
        (
            "E0",
            "SP1",
            "D1",
        ),
    )

    result = SeasonScanner(tmp_path).scan()
    season = result.seasons[0]

    assert season.missing_required_leagues == (
        "I1",
        "F1",
    )

    assert season.is_complete is False
    assert result.is_complete is False
    assert result.incomplete_seasons == (season,)


def test_scanner_ignores_invalid_directory_names(
    tmp_path: Path,
) -> None:
    valid_directory = tmp_path / "data 22 23"
    valid_directory.mkdir()
    create_csv_files(
        valid_directory,
        REQUIRED_LEAGUES,
    )

    invalid_directory = tmp_path / "copias antiguas"
    invalid_directory.mkdir()
    create_csv_files(
        invalid_directory,
        REQUIRED_LEAGUES,
    )

    invalid_season = tmp_path / "data 22 24"
    invalid_season.mkdir()
    create_csv_files(
        invalid_season,
        REQUIRED_LEAGUES,
    )

    result = SeasonScanner(tmp_path).scan()

    assert result.season_count == 1
    assert result.seasons[0].season == "2022-2023"


def test_scanner_rejects_missing_root_directory(
    tmp_path: Path,
) -> None:
    missing_directory = tmp_path / "no-existe"

    with pytest.raises(FileNotFoundError):
        SeasonScanner(missing_directory).scan()


def test_scanner_rejects_duplicate_required_leagues(
    tmp_path: Path,
) -> None:
    with pytest.raises(
        ValueError,
        match="no pueden estar duplicadas",
    ):
        SeasonScanner(
            tmp_path,
            required_leagues=(
                "E0",
                "e0",
            ),
        )