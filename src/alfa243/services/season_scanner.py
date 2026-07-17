import re
from pathlib import Path

from alfa243.domain.data_scan_result import DataScanResult
from alfa243.domain.season_data import SeasonData


class SeasonScanner:
    """Descubre temporadas y archivos CSV históricos."""

    REQUIRED_LEAGUES = (
        "E0",
        "SP1",
        "D1",
        "I1",
        "F1",
    )

    SEASON_DIRECTORY_PATTERN = re.compile(
        r"^data[\s_-]*(\d{2})[\s_-]+(\d{2})$",
        flags=re.IGNORECASE,
    )

    def __init__(
        self,
        root_directory: str | Path,
        required_leagues: tuple[str, ...] | None = None,
    ) -> None:
        self.root_directory = Path(root_directory)

        if required_leagues is None:
            required_leagues = self.REQUIRED_LEAGUES

        normalized_leagues = tuple(
            league.strip().upper()
            for league in required_leagues
            if league.strip()
        )

        if not normalized_leagues:
            raise ValueError(
                "Debe existir al menos una liga obligatoria."
            )

        if len(normalized_leagues) != len(set(normalized_leagues)):
            raise ValueError(
                "Las ligas obligatorias no pueden estar duplicadas."
            )

        self.required_leagues = normalized_leagues

    def scan(self) -> DataScanResult:
        if not self.root_directory.exists():
            raise FileNotFoundError(
                f"No existe la carpeta de datos: "
                f"{self.root_directory}"
            )

        if not self.root_directory.is_dir():
            raise NotADirectoryError(
                f"La ruta no es una carpeta: "
                f"{self.root_directory}"
            )

        seasons: list[SeasonData] = []

        for directory in self.root_directory.iterdir():
            if not directory.is_dir():
                continue

            season = self._parse_season_directory(
                directory.name
            )

            if season is None:
                continue

            csv_files = tuple(
                sorted(
                    (
                        file
                        for file in directory.iterdir()
                        if file.is_file()
                        and file.suffix.casefold() == ".csv"
                    ),
                    key=lambda file: file.name.casefold(),
                )
            )

            available_leagues = {
                file.stem.upper()
                for file in csv_files
            }

            missing_required_leagues = tuple(
                league
                for league in self.required_leagues
                if league not in available_leagues
            )

            seasons.append(
                SeasonData(
                    season=season,
                    directory=directory,
                    csv_files=csv_files,
                    missing_required_leagues=(
                        missing_required_leagues
                    ),
                )
            )

        seasons.sort(
            key=lambda season_data: season_data.season
        )

        return DataScanResult(
            root_directory=self.root_directory,
            seasons=tuple(seasons),
        )

    @classmethod
    def _parse_season_directory(
        cls,
        directory_name: str,
    ) -> str | None:
        match = cls.SEASON_DIRECTORY_PATTERN.fullmatch(
            directory_name.strip()
        )

        if match is None:
            return None

        start_short = int(match.group(1))
        end_short = int(match.group(2))

        start_year = cls._expand_year(start_short)
        end_year = cls._expand_year(end_short)

        if end_year != start_year + 1:
            return None

        return f"{start_year}-{end_year}"

    @staticmethod
    def _expand_year(short_year: int) -> int:
        if short_year >= 70:
            return 1900 + short_year

        return 2000 + short_year