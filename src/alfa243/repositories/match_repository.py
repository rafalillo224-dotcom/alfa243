import csv
from datetime import date
from pathlib import Path

from alfa243.domain.match_data import MatchData


class MatchRepository:
    """Carga partidos desde un archivo CSV."""

    def __init__(self, csv_path: str | Path) -> None:
        self.csv_path = Path(csv_path)

    def get_all(self) -> list[MatchData]:
        if not self.csv_path.exists():
            raise FileNotFoundError(
                f"No se encontró el archivo: {self.csv_path}"
            )

        matches: list[MatchData] = []

        with self.csv_path.open(
            mode="r",
            encoding="utf-8",
            newline="",
        ) as csv_file:
            reader = csv.DictReader(csv_file)

            for row in reader:
                matches.append(self._build_match(row))

        return matches

    def get_by_round(
        self,
        competition: str,
        season: str,
        round_number: int,
    ) -> list[MatchData]:
        normalized_competition = competition.strip().casefold()
        normalized_season = season.strip().casefold()

        return [
            match
            for match in self.get_all()
            if match.competition.casefold() == normalized_competition
            and match.season.casefold() == normalized_season
            and match.round_number == round_number
        ]

    @staticmethod
    def _build_match(row: dict[str, str]) -> MatchData:
        return MatchData(
            competition=row["competition"].strip(),
            season=row["season"].strip(),
            round_number=int(row["round_number"]),
            kickoff=date.fromisoformat(row["kickoff"].strip()),
            home_team=row["home_team"].strip(),
            away_team=row["away_team"].strip(),
            home_odds=float(row["home_odds"]),
            draw_odds=float(row["draw_odds"]),
            away_odds=float(row["away_odds"]),
        )