from alfa243.domain.alfa_combination import AlfaCombination
from alfa243.domain.combination_analysis import CombinationAnalysis
from alfa243.domain.combination_portfolio import CombinationPortfolio


class CombinationAnalyzer:
    """Analiza el ranking y la cobertura de las combinaciones."""

    def analyze(
        self,
        selected: list[AlfaCombination],
        valid_universe: list[AlfaCombination],
    ) -> CombinationPortfolio:
        if not selected:
            raise ValueError(
                "Debe existir al menos una combinación seleccionada."
            )

        if not valid_universe:
            raise ValueError(
                "El universo válido no puede estar vacío."
            )

        self._validate_unique(selected)
        self._validate_unique(valid_universe)
        self._validate_selected_belongs_to_universe(
            selected=selected,
            valid_universe=valid_universe,
        )

        ordered_selected = sorted(
            selected,
            key=lambda combination: combination.probability,
            reverse=True,
        )

        selected_probability = sum(
            combination.probability
            for combination in ordered_selected
        )

        valid_universe_probability = sum(
            combination.probability
            for combination in valid_universe
        )

        cumulative_probability = 0.0
        analyses: list[CombinationAnalysis] = []

        for rank, combination in enumerate(
            ordered_selected,
            start=1,
        ):
            cumulative_probability += combination.probability

            if valid_universe_probability == 0.0:
                cumulative_coverage = 0.0
            else:
                cumulative_coverage = (
                    cumulative_probability
                    / valid_universe_probability
                )

            analyses.append(
                CombinationAnalysis(
                    rank=rank,
                    combination=combination,
                    cumulative_probability=cumulative_probability,
                    cumulative_coverage=cumulative_coverage,
                )
            )

        return CombinationPortfolio(
            analyses=tuple(analyses),
            selected_probability=selected_probability,
            valid_universe_probability=valid_universe_probability,
        )

    @staticmethod
    def _validate_unique(
        combinations: list[AlfaCombination],
    ) -> None:
        codes = [
            combination.code
            for combination in combinations
        ]

        if len(codes) != len(set(codes)):
            raise ValueError(
                "La lista contiene combinaciones duplicadas."
            )

    @staticmethod
    def _validate_selected_belongs_to_universe(
        selected: list[AlfaCombination],
        valid_universe: list[AlfaCombination],
    ) -> None:
        universe_codes = {
            combination.code
            for combination in valid_universe
        }

        missing_codes = [
            combination.code
            for combination in selected
            if combination.code not in universe_codes
        ]

        if missing_codes:
            raise ValueError(
                "Todas las combinaciones seleccionadas deben "
                "pertenecer al universo válido."
            )