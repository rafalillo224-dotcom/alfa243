from dataclasses import dataclass

from alfa243.domain.classified_match import ClassifiedMatch
from alfa243.domain.match_category import MatchCategory


@dataclass(slots=True, frozen=True)
class AlfaSelection:
    """Selección base de doce partidos para ALFA-243."""

    favorites: tuple[ClassifiedMatch, ...]
    balanced: tuple[ClassifiedMatch, ...]

    def __post_init__(self) -> None:
        if len(self.favorites) != 6:
            raise ValueError(
                "La selección debe contener exactamente 6 favoritos."
            )

        if len(self.balanced) != 6:
            raise ValueError(
                "La selección debe contener exactamente 6 igualados."
            )

        if any(
            match.category != MatchCategory.FAVORITE
            for match in self.favorites
        ):
            raise ValueError(
                "Todos los partidos favoritos deben estar "
                "clasificados como favoritos."
            )

        if any(
            match.category != MatchCategory.BALANCED
            for match in self.balanced
        ):
            raise ValueError(
                "Todos los partidos igualados deben estar "
                "clasificados como igualados."
            )

        match_keys = [
            self._match_key(classified)
            for classified in self.all_matches
        ]

        if len(match_keys) != len(set(match_keys)):
            raise ValueError(
                "La selección no puede contener partidos duplicados."
            )

    @property
    def all_matches(self) -> tuple[ClassifiedMatch, ...]:
        return self.favorites + self.balanced

    @staticmethod
    def _match_key(
        classified: ClassifiedMatch,
    ) -> tuple[str, str, str, str, int]:
        match = classified.analysis.match

        return (
            match.competition.casefold(),
            match.season.casefold(),
            match.home_team.casefold(),
            match.away_team.casefold(),
            match.round_number,
        )