from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True, frozen=True)
class SeasonData:
    """Información encontrada para una temporada histórica."""

    season: str
    directory: Path
    csv_files: tuple[Path, ...]
    missing_required_leagues: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.season.strip():
            raise ValueError(
                "La temporada no puede estar vacía."
            )

        if not self.directory.is_dir():
            raise ValueError(
                f"La ruta no es una carpeta válida: {self.directory}"
            )

    @property
    def csv_count(self) -> int:
        return len(self.csv_files)

    @property
    def league_codes(self) -> tuple[str, ...]:
        return tuple(
            csv_file.stem.upper()
            for csv_file in self.csv_files
        )

    @property
    def is_complete(self) -> bool:
        return not self.missing_required_leagues