from alfa243.domain.alfa_selection import AlfaSelection
from alfa243.domain.classified_match import ClassifiedMatch
from alfa243.domain.match_category import MatchCategory


class AlfaSelector:
    """Selecciona los seis favoritos y seis igualados de ALFA-243."""

    FAVORITES_REQUIRED = 6
    BALANCED_REQUIRED = 6

    def select(
        self,
        classified_matches: list[ClassifiedMatch],
    ) -> AlfaSelection:
        self._validate_no_duplicates(classified_matches)

        favorites = [
            match
            for match in classified_matches
            if match.category == MatchCategory.FAVORITE
        ]

        balanced = [
            match
            for match in classified_matches
            if match.category == MatchCategory.BALANCED
        ]

        if len(favorites) < self.FAVORITES_REQUIRED:
            raise ValueError(
                "No hay suficientes favoritos: "
                f"se necesitan {self.FAVORITES_REQUIRED} "
                f"y solo hay {len(favorites)}."
            )

        if len(balanced) < self.BALANCED_REQUIRED:
            raise ValueError(
                "No hay suficientes partidos igualados: "
                f"se necesitan {self.BALANCED_REQUIRED} "
                f"y solo hay {len(balanced)}."
            )

        selected_favorites = sorted(
            favorites,
            key=lambda match: (
                match.selected_probability,
                match.probability_gap,
            ),
            reverse=True,
        )[:self.FAVORITES_REQUIRED]

        selected_balanced = sorted(
            balanced,
            key=lambda match: (
                match.probability_gap,
                -match.selected_probability,
            ),
        )[:self.BALANCED_REQUIRED]

        return AlfaSelection(
            favorites=tuple(selected_favorites),
            balanced=tuple(selected_balanced),
        )

    @staticmethod
    def _validate_no_duplicates(
        classified_matches: list[ClassifiedMatch],
    ) -> None:
        match_keys: list[tuple[str, str, str, str, int]] = []

        for classified in classified_matches:
            match = classified.analysis.match

            match_keys.append(
                (
                    match.competition.casefold(),
                    match.season.casefold(),
                    match.home_team.casefold(),
                    match.away_team.casefold(),
                    match.round_number,
                )
            )

        if len(match_keys) != len(set(match_keys)):
            raise ValueError(
                "La lista contiene partidos duplicados."
            )