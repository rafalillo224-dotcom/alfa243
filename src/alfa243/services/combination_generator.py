from itertools import product

from alfa243.domain.alfa_combination import AlfaCombination
from alfa243.domain.alfa_selection import AlfaSelection
from alfa243.domain.classified_match import ClassifiedMatch
from alfa243.domain.combination_pick import CombinationPick


class CombinationGenerator:
    """Genera y prioriza las combinaciones del sistema ALFA-243."""

    OUTCOMES = ("1", "X", "2")

    def __init__(
        self,
        maximum_combinations: int = 243,
        minimum_draws: int = 1,
        maximum_draws: int = 4,
        exclude_all_away: bool = True,
    ) -> None:
        if maximum_combinations <= 0:
            raise ValueError(
                "El máximo de combinaciones debe ser positivo."
            )

        if not 0 <= minimum_draws <= 6:
            raise ValueError(
                "El mínimo de empates debe estar entre 0 y 6."
            )

        if not 0 <= maximum_draws <= 6:
            raise ValueError(
                "El máximo de empates debe estar entre 0 y 6."
            )

        if minimum_draws > maximum_draws:
            raise ValueError(
                "El mínimo de empates no puede superar al máximo."
            )

        self.maximum_combinations = maximum_combinations
        self.minimum_draws = minimum_draws
        self.maximum_draws = maximum_draws
        self.exclude_all_away = exclude_all_away

    def generate(
        self,
        selection: AlfaSelection,
    ) -> list[AlfaCombination]:
        """Devuelve únicamente las combinaciones prioritarias."""

        combinations = self.generate_all(selection)

        return combinations[:self.maximum_combinations]

    def generate_all(
        self,
        selection: AlfaSelection,
    ) -> list[AlfaCombination]:
        """Devuelve todo el universo de patrones válidos."""

        favorite_picks = tuple(
            self._build_favorite_pick(classified)
            for classified in selection.favorites
        )

        combinations: list[AlfaCombination] = []

        for pattern in product(
            self.OUTCOMES,
            repeat=len(selection.balanced),
        ):
            if not self._pattern_is_allowed(pattern):
                continue

            balanced_picks = tuple(
                self._build_balanced_pick(
                    classified=classified,
                    outcome=outcome,
                )
                for classified, outcome in zip(
                    selection.balanced,
                    pattern,
                    strict=True,
                )
            )

            combinations.append(
                AlfaCombination(
                    favorites=favorite_picks,
                    balanced=balanced_picks,
                )
            )

        combinations.sort(
            key=lambda combination: combination.probability,
            reverse=True,
        )

        return combinations

    def count_valid_patterns(
        self,
        balanced_match_count: int = 6,
    ) -> int:
        if balanced_match_count <= 0:
            raise ValueError(
                "Debe existir al menos un partido igualado."
            )

        return sum(
            self._pattern_is_allowed(pattern)
            for pattern in product(
                self.OUTCOMES,
                repeat=balanced_match_count,
            )
        )

    def _pattern_is_allowed(
        self,
        pattern: tuple[str, ...],
    ) -> bool:
        draw_count = pattern.count("X")

        if not (
            self.minimum_draws
            <= draw_count
            <= self.maximum_draws
        ):
            return False

        if (
            self.exclude_all_away
            and all(outcome == "2" for outcome in pattern)
        ):
            return False

        return True

    @staticmethod
    def _build_favorite_pick(
        classified: ClassifiedMatch,
    ) -> CombinationPick:
        return CombinationPick(
            classified_match=classified,
            outcome=classified.selected_outcome,
            probability=classified.selected_probability,
            is_fixed=True,
        )

    @staticmethod
    def _build_balanced_pick(
        classified: ClassifiedMatch,
        outcome: str,
    ) -> CombinationPick:
        prediction = classified.analysis.fusion_prediction

        probabilities = {
            "1": prediction.home,
            "X": prediction.draw,
            "2": prediction.away,
        }

        return CombinationPick(
            classified_match=classified,
            outcome=outcome,
            probability=probabilities[outcome],
            is_fixed=False,
        )