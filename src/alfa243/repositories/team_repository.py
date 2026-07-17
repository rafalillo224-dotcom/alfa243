import csv
from pathlib import Path

from alfa243.domain.team_statistics import TeamStatistics


class TeamRepository:
    """Carga estadísticas de equipos desde un archivo CSV."""

    def __init__(self, csv_path: str | Path) -> None:
        self.csv_path = Path(csv_path)

    def get(self, team_name: str) -> TeamStatistics:
        if not self.csv_path.exists():
            raise FileNotFoundError(
                f"No se encontró el archivo: {self.csv_path}"
            )

        normalized_name = team_name.strip().casefold()

        with self.csv_path.open(
            mode="r",
            encoding="utf-8",
            newline="",
        ) as csv_file:
            reader = csv.DictReader(csv_file)

            for row in reader:
                current_name = row["team"].strip()

                if current_name.casefold() == normalized_name:
                    return TeamStatistics(
                        goals_for=float(row["goals_for"]),
                        goals_against=float(row["goals_against"]),
                    )

        raise KeyError(f"Equipo no encontrado: {team_name}")