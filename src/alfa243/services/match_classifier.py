from alfa243.domain.classified_match import ClassifiedMatch
from alfa243.domain.match_analysis import MatchAnalysis
from alfa243.domain.match_category import MatchCategory


class MatchClassifier:
    """Clasifica partidos según la predicción fusionada."""

    def __init__(
        self,
        favorite_probability: float = 0.55,
        favorite_gap: float = 0.15,
        balanced_gap: float = 0.10,
    ) -> None:
        values = (
            favorite_probability,
            favorite_gap,
            balanced_gap,
        )

        if any(value < 0.0 or value > 1.0 for value in values):
            raise ValueError(
                "Los límites deben estar entre 0 y 1."
            )

        if balanced_gap > favorite_gap:
            raise ValueError(
                "El límite igualado no puede superar "
                "el límite de favorito."
            )

        self.favorite_probability = favorite_probability
        self.favorite_gap = favorite_gap
        self.balanced_gap = balanced_gap

    def classify(
        self,
        analysis: MatchAnalysis,
    ) -> ClassifiedMatch:
        prediction = analysis.fusion_prediction

        probabilities = {
            "1": prediction.home,
            "X": prediction.draw,
            "2": prediction.away,
        }

        ordered = sorted(
            probabilities.items(),
            key=lambda item: item[1],
            reverse=True,
        )

        selected_outcome, selected_probability = ordered[0]
        second_probability = ordered[1][1]

        probability_gap = (
            selected_probability - second_probability
        )

        if (
            selected_probability >= self.favorite_probability
            and probability_gap >= self.favorite_gap
        ):
            category = MatchCategory.FAVORITE

        elif probability_gap <= self.balanced_gap:
            category = MatchCategory.BALANCED

        else:
            category = MatchCategory.NEUTRAL

        return ClassifiedMatch(
            analysis=analysis,
            category=category,
            selected_outcome=selected_outcome,
            selected_probability=selected_probability,
            probability_gap=probability_gap,
        )

    def classify_all(
        self,
        analyses: list[MatchAnalysis],
    ) -> list[ClassifiedMatch]:
        return [
            self.classify(analysis)
            for analysis in analyses
        ]

    def favorites(
        self,
        analyses: list[MatchAnalysis],
    ) -> list[ClassifiedMatch]:
        classified = self.classify_all(analyses)

        favorites = [
            match
            for match in classified
            if match.category == MatchCategory.FAVORITE
        ]

        return sorted(
            favorites,
            key=lambda match: match.selected_probability,
            reverse=True,
        )

    def balanced(
        self,
        analyses: list[MatchAnalysis],
    ) -> list[ClassifiedMatch]:
        classified = self.classify_all(analyses)

        balanced_matches = [
            match
            for match in classified
            if match.category == MatchCategory.BALANCED
        ]

        return sorted(
            balanced_matches,
            key=lambda match: match.probability_gap,
        )