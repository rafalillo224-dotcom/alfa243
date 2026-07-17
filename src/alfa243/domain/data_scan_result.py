from dataclasses import dataclass
from pathlib import Path

from alfa243.domain.season_data import SeasonData


@dataclass(slots=True, frozen=True)
class DataScanResult:
    """Resultado completo de explorar el histórico de ligas."""

    root_directory: Path
    seasons: tuple[SeasonData, ...]

    def __post_init__(self) -> None:
        if not self.root_directory.is_dir():
            raise ValueError(
                "La raíz de datos debe ser una carpeta válida."
            )

    @property
    def season_count(self) -> int:
        return len(self.seasons)

    @property
    def total_csv_count(self) -> int:
        return sum(
            season.csv_count
            for season in self.seasons
        )

    @property
    def incomplete_seasons(self) -> tuple[SeasonData, ...]:
        return tuple(
            season
            for season in self.seasons
            if not season.is_complete
        )

    @property
    def is_complete(self) -> bool:
        return bool(self.seasons) and not self.incomplete_seasons